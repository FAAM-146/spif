import glob
import json
import shutil
from typing import Mapping
import os
import sys


import pdb

from rstproc import *
import preprocessor as prep

# Filename of mandatory definition/product file/s
DEFAULT_MANDATORY_DEFINITION = 'spif_example'

# Filename for minimal example definition, ie only mandatory vocabulary
# Used to create dynamic documentation for mandatory only
DEFAULT_MINIMAL_FILENAME = DEFAULT_MANDATORY_DEFINITION

# Path to spif standard dir
spif_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', '..', 'standard')
        )

# Path to dynamically generated rst files
source_dir = os.path.dirname(__file__)

# Path to templates
template_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'templates')
        )

dynamic_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), 'dynamic_content')
        )


def populate_group_rst(data: dict,
                       filename: str,
                       level: int=0,
                       **kwargs) -> None:
    """Creates rst file describing vocabulary of group"""

    # Create a filename for each group
    if data['meta']['path'] in ['/', 'root']:
        # Is root group
        grp_filename = (
                f'{os.path.splitext(filename)[0]}.root.rst')
    else:
        grp_filename = filename.replace(".rst", f'.{data["meta"]["name"]}.rst')

    # Include reference to the new file in the main rst file
    with open(filename, 'a') as f:
        f.write(f'\n\n.. include:: {os.path.basename(grp_filename)}')

    # Write the new file
    with open(grp_filename, 'w') as f:
        f.write(rst_grp(data, level=level))

    try:
        groups = data['groups']
    except KeyError as err:
        # No sub-groups
        return

    for group in groups:
        group['meta']['path'] = os.path.join(data['meta']['path'],
                                             group['meta']['name'])
        populate_group_rst(group, grp_filename, level, **kwargs)

    return


def populate_vocab_rst(definition,
                       vocab_example_filename: str=None,
                       incl_required: bool=True,
                       incl_optional: bool=False) -> str:
    """Create vocabulary description rst file"""

    with open(definition, 'r') as f:
        data = json.load(f)

    # Add a path meta key to data
    data['meta']['path'] = '/'

    # Create a filename to save the rst text into
    # Filenames will be created for each group based on the group name/s
    if vocab_example_filename:
        basename = vocab_example_filename
    else:
        basename = os.path.splitext(os.path.basename(definition))[0]

    with open(os.path.join(template_dir, 'vocabulary_template.rst'), 'r') as f:
        rst = f.read()

    vocab_types = []
    if incl_required:
        vocab_types.append('Mandatory')
    if incl_optional:
        vocab_types.append('Optional')
    vocab_types = ' and '.join(vocab_types)

    rst = rst.replace('TAG_PRODUCT_NAME', basename)
    rst = rst.replace('TAG_VOCAB_TYPES', vocab_types)
    rst += '\n\n'

    rst_file = os.path.join(dynamic_dir, basename + '.rst')

    with open(rst_file, 'w') as f:
        f.write(rst)

    populate_group_rst(data, rst_file,
                       incl_required=incl_required,
                       incl_optional=incl_optional)

    return rst_file


def call(args_dict: dict) -> None:
    """Main script call

    Function loops through each definition file given. The first is used as
    the primary to create documentation that covers only the mandatory
    vocabulary. Each subsequent file is used to illustrate extended/optional
    vocabulary.

    A substitutions file is created to be used in index.rst and spif-doc.rst
    so that links to the dynamically generated docs work correctly.
    """

    if not os.path.exists(dynamic_dir):
        os.makedirs(dynamic_dir)
    else:
        pdb.set_trace()

        for f in os.listdir(dynamic_dir):
            try:
                os.remove(os.path.join(dynamic_dir, f))
            except OSError as err:
                shutil.rmtree(os.path.join(dynamic_dir, f))

    example_files = []

    _args_dict = args_dict.copy()
    _ = _args_dict.pop('definition_filenames', None)

    # Create minimal example doc first, ie Mandatory vocab only
    minimal = True

    for file in args_dict['definition_filenames']:
        _args_dict['definition_filename'] = file
        def_dict = prep.get_definition(spif_dir, **_args_dict)
        definition = def_dict['product']['path']
        example_files.append(populate_vocab_rst(definition, file))
        minimal = False

    req_example_file = os.path.relpath(example_files[0], dynamic_dir)
    opt_example_files = [os.path.relpath(f, dynamic_dir)
                         for f in example_files[1:]
                         ]

    # Create a substitutions file based on template
    with open(os.path.join(template_dir,
                           'substitutions_template.rst'), 'r') as f:
        rst = f.read()

    rst = rst.replace('REQUIRED_SPIF_EXAMPLE',
                      os.path.splitext(req_example_file)[0])
    rst = rst.replace('OPTIONAL_SPIF_EXAMPLES', '\n'.join(opt_example_files))
    rst += '\n\n'

    subst_file = os.path.join(dynamic_dir, 'substitutions.rst')

    with open(subst_file, 'w') as f:
        f.write(rst)

    # Write versions used to create docs into documentation_versions.py
    with open(os.path.join(template_dir,
                           'documentation_versions.txt'), 'r') as f:
        text = f.read()

    std_ver = def_dict['standard']['version'].lstrip('v')
    prod_ver = def_dict['product']['version'].lstrip('v')
    text = text.replace('STD_VERSION_NUM', std_ver)
    text = text.replace('PROD_VERSION_NUM', prod_ver)

    with open(os.path.join(dynamic_dir, 'versions.py'), 'w') as f:
        f.write(text)

    return


# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == '__main__':

    import argparse

    # Define commandline options
    usage = ("make <build> STDFILE=definition_filename "
             "STDVER=std_version PRODVER=product_version "
             "PRODDIR=product_path")
    version = f"version: {prep.__version__}"
    description = ("Preprocessor for sphinx generation of SPIF "
                   f"documentation.\n {version}")

    parser = argparse.ArgumentParser(usage=usage,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description)

    # Optional arguments
    parser.add_argument('-f', '--file',
                        action='store',
                        nargs='*',
                        dest='definition_filenames',
                        default=[DEFAULT_MANDATORY_DEFINITION],
                        type=str,
                        help=("Space-delineated list of filenames, or part "
                              "thereof, of the definition file/s of a single "
                              "version of the standard, ie the .yaml file/s. "
                              "The first file must *only* contain mandatory "
                              "vocabulary. Any subsequent files given can be "
                              "used to illustrate extended vocabulary. If the "
                              "filenames do not exist within the required "
                              "standard version and product, the "
                              "documentation build will fail."))
    parser.add_argument('-s', '--standard',
                        action='store',
                        dest='std_version',
                        default='latest',
                        type=str,
                        help=("Version of the standard that will be used "
                              "to create the documentation. If the version "
                              "given does not exist then will default "
                              "to the most recent version."))
    parser.add_argument('-p', '--product',
                        action='store',
                        dest='product_version',
                        default='latest',
                        type=str,
                        help=("Version of the product that will be used "
                              "to create the documentation. If the version "
                              "given does not exist then will default "
                              "to 'latest'."))
    parser.add_argument('--product_path',
                        action='store',
                        dest='product_path',
                        default=os.path.abspath('.'),
                        type=str,
                        help=("Path to product files. Default is "
                              f"{os.path.abspath('.')} so used when products "
                              "have been created outside of this repository."))
    parser.add_argument('--vocab',
                        action='store',
                        dest='vocab_types',
                        choices=['all', 'both',
                                 'required', 'mandatory',
                                 'optional'],
                        default='all',
                        type=str,
                        help=("Designates what types of vocabulary to include "
                              "in documentation; required, optional, or both. "
                              "Default is 'all' so both required and optional "
                              "vocabulary are included in documentation."))

    args_dict = vars(parser.parse_args())
    #args, unknown = parser.parse_known_args()

    call(args_dict)
