import glob
import json
import shutil
from typing import Mapping
import os
import sys

<<<<<<< HEAD:docs/preproc.py
import pdb

# Preprocessor information
__version__ = 20240326


=======

def setup(app):
    return

__version__ = '20240315'
__all__ = ['docs_conf']

# Default variables that can be passed from Sphinx to conf.py to this script
# Version of the spif standard. Default is highest version number
STD_VERSION = 'latest'
# Version of the product. Default is "latest"
PRODUCT_VERSION = 'latest'
# Type of vocabulary to include in docs. Default is mandatory and optional
VOCAB_TYPES = 'all'


def docs_conf(std_path: str='.',
              std_version: str=None,
              product_version: str=None,
              vocab_types: [str, list]=None) -> list[tuple, tuple, dict]:

    """Determine code source for documentation.

    Args:
        std_path: Path, absolute or relative to docs/, to the standard code
            directory.
        std_version: Version of the spif standard. Default is highest version
            number found relative to ``home_path``.
        product_version: Version of the product. Default is "latest".
        vocab_types: Type of vocabulary entries to include in documentation.
            May be one or more of "all" [default] or "both", "required" or
            "mandatory", or "optional". May be a list of more than one or a
            single string.

    Returns:
        A list of three elements which give the standard version and path, the
        product version and path, and a dictionary of vocabulary types to
        include in the documentation. For example:

        [(std_version, std_path),
         (product_version, product_path),
         {'incl_required': incl_required, 'incl_optional': incl_optional},
        ]
    """


    if not os.path.isdir(std_path):
        std_path = '.'

    import pdb
    pdb.set_trace()

    if not std_version:
        std_version = STD_VERSION
    if not product_version:
        product_version = PRODUCT_VERSION
    if not vocab_types:
        vocab_types = VOCAB_TYPES

    # Find required version of the standard. Assume directories are v1, v2, etc
    std_version = str(std_version).lower()
    std_version = std_version if std_version.startswith('v') else 'v'+std_version
    if not glob.glob(std_version, std_path):
        # If requested std does not exist then default to the latest one
        std_path = sorted(glob.glob('v*', std_path))[-1]
        std_version = os.path.basename(std_path)
    else:
        std_path = glob.glob(std_version, std_path)

    # Find required version of the product.
    # Assume directory names are 'v' num or 'latest'
    product_version = str(product_version).lower()
    if product_version != PRODUCT_VERSION and not product_version.startswith('v'):
        product_version = 'v' + product_version

    # Find required product directory
    product_path = os.path.join(std_path, '..', 'products', product_version)
    if not os.path.isdir(product_path):
        product_path = os.path.join(std_path, '..', 'products', PRODUCT_VERSION)
        product_version = PRODUCT_VERSION

    # Determine what type of vocabulary to include in docs
    vocab_types = [s.lower() for s in list(vocab_types)]
    incl_required = True
    incl_optional = False

    if set('all', 'both').union(vocab_types):
        incl_required = True
        incl_optional = True
    else:
        if set(['required', 'mandatory']).union(vocab_types):
            incl_required = True
        elif set(['optional']).union(vocab_types):
            incl_optional = True
        elif not set(['required', 'mandatory']).union(vocab_types):
            incl_required = False


    return [(std_version, std_path),
            (product_version, product_path),
            {'incl_required': incl_required, 'incl_optional': incl_optional},
            ]



"""
>>>>>>> d838fe998a0ceb77139a5083f71becc8255e90be:docs/source/preproc.py
# Path to spif standard dir
spif_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..',
                                        'standard')
                                        )

<<<<<<< HEAD:docs/preproc.py
# Default variables that can be passed from Sphinx to this script
STD = 'latest'      # Version of the spif standard. Default is highest v number
PRODUCT = 'latest'  # Version of the product. Default is latest
VOCAB_TYPES = 'all' # Type of vocabulary to include in documentation

# To modify the defaults when building with Sphinx;
# shinx-build -D std=1 -D version=1.2 -D doc_types=required,optional source/ build/
#
# This will build html output (the default) for v1 of the standard with v1.2
# products (will fall back to latest if v1.2 does not exist) and include
# information on required and optional vocabulary.
=======
>>>>>>> d838fe998a0ceb77139a5083f71becc8255e90be:docs/source/preproc.py





<<<<<<< HEAD:docs/preproc.py



def get_std(std=None):
    """Determine the version of the standard to include in the preprocessing

    """
    if not std:
        std = STD

    # Find required version of the standard. Assume directories are v1, v2, etc
    std = str(std).lower()
    std = std if std.startswith('v') else 'v' + std
    if not glob.glob(std, std_dir):
        # If requested std does not exist then default to the latest one
        std_dir = sorted(glob.glob('v*', std_dir))[-1]
        std = os.path.basename(std_dir)
    else:
        std_dir = glob.glob(std, std_dir)

    return std, std_dir

def get_product(product=None):
    """Determine the version of the product to include in the preprocessing

    """

    if not product:
        product = PRODUCT

    # Find required version of the standard.
    # Assume directory names are 'v' num or 'latest'
    product = str(product).lower()
    if product != PRODUCT and not product.startswith('v'):
        product += 'v'

    # Find required version
    product_dir = os.path.join(spif_dir, 'products', product)
    if not os.path.isdir(product_dir):
        product_dir = os.path.join(spif_dir, 'products', PRODUCT)

    return product, product_dir


def get_incvocab(vocab=None):
    """Determine the vocabulary types to include in the preprocessing

    """

    if not vocab:
        vocab = VOCAB_TYPES

    # Determine what type of vocabulary to include in docs
    vocab = [s.lower() for s in list(vocab)]
    incl_required = True
    incl_optional = False

    if set('all', 'both').union(vocab):
        incl_required = True
        incl_optional = True
    else:
        if set(['required', 'mandatory']).union(vocab):
            incl_required = True
        elif set(['optional']).union(vocab):
            incl_optional = True
        elif not set(['required', 'mandatory']).union(vocab):
            incl_required = False

    return {'incl_required': incl_required, 'incl_optional': incl_optional}


def get_definition(std, product, vocab):
    """Determine arguments to apply to preprocessor

    """

    _d = lambda t: {k:v for k, v in zip(('version', 'path'), t)}

    return {'standard': _d(get_std(std)),
            'product': _d(get_product(product)),
            'vocab': get_incvocab(vocab),
            }


=======
>>>>>>> d838fe998a0ceb77139a5083f71becc8255e90be:docs/source/preproc.py

# Add standard
sys.path.append('../../')
from attributes import GlobalAttributes


template_dir = os.path.join(
    os.path.dirname(__file__),
    'templates'
)
dynamic_dir = os.path.join(
    os.path.dirname(__file__),
    'dynamic_content'
)

if not os.path.exists(dynamic_dir):
    os.makedirs(dynamic_dir)

def init() -> None:
    for f in os.listdir(dynamic_dir):
        os.remove(f)

def copy_introduction() -> None:
    shutil.copy2(
        os.path.join(template_dir, 'introduction.rst'),
        os.path.join(dynamic_dir, 'introduction.rst'),
    )

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

def copy_global_attrs() -> None:
    shutil.copy(
        os.path.join(template_dir, 'global_attributes.rst'),
        os.path.join(dynamic_dir, 'global_attributes.rst'),
    )

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

def copy_variables() -> None:
    shutil.copy(
        os.path.join(template_dir, 'variables.rst'),
        os.path.join(dynamic_dir,  'variables.rst'),
    )

def populate_variables(definition,
                       incl_required: bool=True,
                       incl_optional: bool=False) -> None:
    with open(definition, 'r') as f:
        data = json.load(f)
    variables = sorted(data['variables'], key=lambda x: x['meta']['name'])
    text = ''
    for var in variables:

        if incl_required and incl_optional:
            pass
        elif incl_required and var["meta"]["required"]:
            pass
        elif incl_optional and not var["meta"]["required"]:
            pass
        else:
            continue

        _name =  f'{var["meta"]["name"]}'#' `{var["meta"]["datatype"]}`'
        text += _name + '\n'
        text += '-' * (len(_name)) + '\n'
        # text += f'* **{var["meta"]["name"]}** `{var["meta"]["datatype"]}`\n\n'
        text += f':Datatype: `{var["meta"]["datatype"]}`\n'
        text += f':Dimensions: {", ".join(var["dimensions"])}\n'
        text += (f':Description: {var["meta"]["description"]}\n\n'
                 if var["meta"].get("description")
                 else '\n')
        #text += '\nAttributes\n'
        #text += '='* len('Attributes') + '\n\n'
        for attr_key, attr_value in var['attributes'].items():
            text += f'* ``{attr_key}`` : {str(attr_value)}\n'
        text += '\n'

    with open(os.path.join(dynamic_dir, 'variables.rst'), 'r') as f:
        rst = f.read()

    rst = rst.replace('TAG_PRODUCT_VARIABLES', text)


    with open(os.path.join(dynamic_dir, 'variables.rst'), 'w') as f:
        f.write(rst)


if __name__ == '__main__':

    import argparse

    # Define commandline options
    usage = "make <build> PROCOPTS='std_version product_version vocab_type'"
    version = f"version: {__version__}"
    description = ("Preprocessor for sphinx generator of spif "
                   "documentation.\n {version}")

    parser = argparse.ArgumentParser(usage=usage,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description)

    # Optional arguments
    parser.add_argument('-v', '--version',
                        action='store',
                        dest='std_version',
                        default='latest',
                        type=str,
                        help=("Version of the standard that will be used "
                              "to create the documentation. If the version "
                              "given does not exist then will default "
                              "to the most recent version."))
    parser.add_argument('-p, --product',
                        action='store',
                        dest='product_version',
                        default='latest',
                        type=str,
                        help=("Version of the product that will be used "
                              "to create the documentation. If the version "
                              "given does not exist then will default "
                              "to 'latest'."))
    parser.add_argument('--vocab',
                        action='store',
                        dest='vocab_type',
                        choices=['all', 'both',
                                 'required', 'mandatory',
                                 'optional'],
                        default='all',
                        type=str,
                        help=("Designates what types of vocabulary to include "
                              "in documentation; required, optional, or both. "
                              "Default is 'all' so both required and optional "
                              "vocabulary are included in documentation."))

    pdb.set_trace()

    args_dict = vars(parser.parse_args())

    definition = os.environ['FAAM_PRODUCT'] #/home/dave/vcs/faam-data/products/latest/core_faam_YYYYmmdd_v005_rN_xNNN.json'
    copy_introduction()
    populate_introduction(definition)
    copy_global_attrs()
    populate_global_attrs(definition)
    copy_variables()
    populate_variables(definition)


"""