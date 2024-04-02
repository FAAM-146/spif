
import glob
import json
import shutil
from typing import Mapping
import os
import sys


import pdb


__all__ = ['get_std',
           'get_product',
           'get_vocab',
           'get_definition']



# Default variables that can be passed from Sphinx to conf.py to this script
# Version of the spif standard. Default is highest version number
STD_VERSION = 'latest'
# Version of the product. Default is "latest"
PRODUCT_VERSION = 'latest'
PRODUCT_IGNORE = ['dataset_schema.json']
# Type of vocabulary to include in docs. Default is mandatory and optional
VOCAB_TYPES = 'all'


def get_std(std_path: str='.',std_version: str=None) -> tuple:
    """Determine spif standard version.

    Args:
        std_path: Path, absolute or relative to docs/, to the standard code
            directory.
        std_version: Version of the spif standard. Default is highest version
            number found relative to ``home_path``.

    Returns:
        Tuple of the standard version string and the appropriate path.

    """

    _pathnotfound = lambda p: IndexError(
            f'No standard versions could not be found at {p}')

    if not os.path.isdir(std_path):
        std_path = '.'

    if not std_version:
        std_version = STD_VERSION

    # Find required version of the standard. Assume directories are v1, v2, etc
    std_version = str(std_version).lower()
    std_version = std_version if std_version.startswith('v') else 'v'+std_version
    if not glob.glob(os.path.join(std_path, std_version)):
        # If requested std does not exist then default to the latest one
        try:
            std_path = sorted(glob.glob(os.path.join(std_path, 'v*')))[-1]
        except IndexError as err:
            _pathnotfound(std_path)
        std_version = os.path.basename(std_path)
    else:
        try:
            std_path = glob.glob(os.path.join(std_path, std_version))[0]
        except IndexError as err:
            _pathnotfound(std_path)

    return (std_version, std_path)


def get_product(std_path: str='.', product_version: str=None) -> tuple:
    """Determine product version.

    Args:
        std_path: Path, absolute or relative to docs/, to the standard code
            directory.
        product_version: Version of the product. Default is "latest".

    Returns:
        Tuple of the product version string and the appropriate path.
    """

    if not os.path.isdir(std_path):
        std_path = '.'
    
    if not product_version:
        product_version = PRODUCT_VERSION

    # Find required version of the product.
    # Assume directory names are 'v' num or 'latest'
    product_version = str(product_version).lower()
    if product_version != PRODUCT_VERSION and not product_version.startswith('v'):
        product_version = 'v' + product_version

    # Find required product directory
    product_path = os.path.abspath(
            os.path.join(std_path, 'products', product_version)
            )
    if not os.path.isdir(product_path):
        product_path = os.path.abspath(
            os.path.join(std_path, 'products', PRODUCT_VERSION)
            )
        product_version = PRODUCT_VERSION

    return (product_version, product_path)


def get_vocab(vocab_types: [str, list]=None) -> Mapping:
    """Determine which vocabulary types to include in documentation.

    Args:
        std_path: Path, absolute or relative to docs/, to the standard code
            directory.
        vocab_types: Type of vocabulary entries to include in documentation.
            May be one or more of "all" [default] or "both", "required" or
            "mandatory", or "optional". May be a list of more than one or a
            single string.

    Returns:
        Dictionary of vocabulary types to include in the documentation.
    """

    if not vocab_types:
        vocab_types = VOCAB_TYPES

    if type(vocab_types) not in [list, tuple]:
        vocab_types = [vocab_types]

    # Determine what type of vocabulary to include in docs
    vocab_types = [s.lower() for s in vocab_types]
    incl_required = True
    incl_optional = False

    if set(['all', 'both']).intersection(vocab_types):
        incl_required = True
        incl_optional = True
    else:
        if set(['required', 'mandatory']).intersection(vocab_types):
            incl_required = True
        elif set(['optional']).intersection(vocab_types):
            incl_optional = True
        elif not set(['required', 'mandatory']).intersection(vocab_types):
            incl_required = False

    return {'incl_required': incl_required, 'incl_optional': incl_optional}


def get_definition(
              std_path: str='.',
              definition_filename: str=None,
              std_version: str=None,
              product_version: str=None,
              vocab_types: [str, list]=None) -> Mapping:
    """Determine code source for documentation

    """

    _d = lambda t: {k:v for k, v in zip(('version', 'path'), t)}

    def_dict = {'standard': _d(get_std(std_path, std_version)),
                'product': _d(get_product(std_path, product_version)),
                'vocab': get_vocab(vocab_types),
                }

    def_basename, _ = os.path.splitext(definition_filename)
    files = []
    for _path in [def_dict['standard']['path'], def_dict['product']['path']]:
        files.extend(glob.glob(os.path.join(_path, '**', def_basename+'.*'),
                               recursive=True)
                    )

    if len(files) != 2:
        raise FileNotFoundError('Definition and/or Product files not found '
                                'for this standard version.')

    def_dict['standard']['path'] = files[0]
    def_dict['product']['path'] = files[1]

    return def_dict