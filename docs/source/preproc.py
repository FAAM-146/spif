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

if not os.path.exists(dynamic_dir):
    os.makedirs(dynamic_dir)

def init() -> None:
    for f in os.listdir(dynamic_dir):
        os.remove(f)

def populate_introduction(definition) -> None:
    with open(definition, 'r') as f:
        data = json.load(f)

    name = os.path.basename(definition.replace('.json', ''))
    description = data['meta']['description']
    pattern = data['meta']['file_pattern']
    references = data['meta']['references']

    references = ' | '.join([f'`{i[0]} <{i[1]}>`_' for i in references])

    with open(os.path.join(dynamic_dir, 'introduction.rst'), 'r') as f:
        rst = f.read()

    rst = rst.replace('TAG_PRODUCT_NAME', name)
    rst = rst.replace('TAG_PRODUCT_DESCRIPTION', description)
    rst = rst.replace('TAG_PRODUCT_FILE_PATTERN', pattern)
    rst = rst.replace('TAG_PRODUCT_REFERENCES', references)

    with open(os.path.join(dynamic_dir, 'introduction.rst'), 'w') as f:
        f.write(rst)


def populate_global_attrs(definition) -> None:
    
    with open(definition, 'r') as f:
        data = json.load(f)
    attributes = data['attributes']

    text = ''
    for key, value in attributes.items():
        text += f'* ``{key}``: '
        text += f'**{value}** - '
        desc =  GlobalAttributes.model_json_schema()['properties'][key]['description']
        print(desc)
        text += desc + '\n'
    text += '\n'

    with open(os.path.join(dynamic_dir, 'global_attributes.rst'), 'r') as f:
        rst = f.read()

    rst = rst.replace('TAG_PRODUCT_GLOBAL_ATTRIBUTES', text)


    with open(os.path.join(dynamic_dir, 'global_attributes.rst'), 'w') as f:
        f.write(rst)




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
        populate_group_rst(group, grp_filename, level+1, **kwargs)

    return


def populate_vocab_rst(definition,
                       vocab_example_filename: str=None,
                       incl_required: bool=True,
                       incl_optional: bool=False) -> None:
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

# ----------------------------------------------------------------------
# ----------------------------------------------------------------------
if __name__ == '__main__':

    import argparse

    # Define commandline options
    usage = ("make <build> FILEOPT=definition_filename "
             "STDOPT=std_version PRODOPT=product_version "
             "PRODDIR=product_path VOCABOPT=vocab_types")
    version = f"version: {prep.__version__}"
    description = ("Preprocessor for sphinx generation of SPIF "
                   f"documentation.\n {version}")

    parser = argparse.ArgumentParser(usage=usage,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description)

    # Optional arguments
    parser.add_argument('-f', '--filename',
                        action='store',
                        dest='definition_filename',
                        default=DEFAULT_MANDATORY_DEFINITION,
                        type=str,
                        help=("Filename or part thereof, of the definition "
                              "file of the standard (ie the .yaml). If the "
                              "filename does not exist within the required "
                              "standard version and product the documentation "
                              "build will fail."))
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

    def_dict = prep.get_definition(spif_dir, **args_dict)
    definition = def_dict['product']['path']

    subs_rst = '..\n  Substitution links to dynamic content\n\n'
    example_files = {'MandatorySpifFile': '', 'OptionalSpifFile': ''}
    example = populate_vocab_rst(definition,
                                 vocab_example_filename = 'minimal_example',
                                 incl_required = True,
                                 incl_optional = False
                                 )
    example_files['MandatorySpifFile'] = os.path.relpath(
                                example, os.path.dirname(__file__))

    if def_dict['vocab']['incl_optional'] is True:
        example = populate_vocab_rst(definition, **def_dict['vocab'])
        example_files['OptionalSpifFile'] = os.path.relpath(
                                example, os.path.dirname(__file__))

    subs_rst += '\n'.join(
        [f'.. |{f}| replace:: {k}' for f,k in example_files.items() if k]
        )

    subs_file = os.path.join(os.path.dirname(__file__),
                             "filename_substitutions.rst")

    with open(subs_file, 'w') as f:
        f.write(subs_rst)