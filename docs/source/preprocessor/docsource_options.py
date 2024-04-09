
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



# Default variable values
# Version of the spif standard. Default is highest version number
STD_VERSION = 'latest'
# Version of the product. Default is "latest"
PRODUCT_VERSION = 'latest'
# Default name of directory that contains product .json files
PRODUCT_DIR = 'product*'
# Product files to ignore (not currently used)
PRODUCT_IGNORE = ['dataset_schema.json']
# Type of vocabulary to include in docs. Default is mandatory and optional
VOCAB_TYPES = 'all'


def _pathnotfound(v: str, p: str) -> None:
    """Raise an error when no appropriate files can be found on this path"""

    raise FileNotFoundError(f'No {v} versions could not be found at {p}')



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
            _pathnotfound('standard', std_path)
        std_version = os.path.basename(std_path)
    else:
        try:
            std_path = glob.glob(os.path.join(std_path, std_version))[0]
        except IndexError as err:
            _pathnotfound('standard', std_path)

    return (std_version, std_path)


def get_product(product_path: str='.',
                product_version: str=None) -> tuple:
    """Determine product version.

    Args:
        product_path: Path, absolute or relative to __file__, to the product
            directory. Default is `PRODUCT_DIR`.
        product_version: Version of the product. Default is "latest".

    Returns:
        Tuple of the product version string and the appropriate path.
    """

    if not os.path.isdir(product_path):
        product_path = os.path.abspath('.')

    if not product_version:
        product_version = PRODUCT_VERSION

    # Find required product directory
    search_path = os.path.abspath(os.path.join(product_path, 'fred'))
    product_dir = []
    loop_cnt = 0
    while len(product_dir) == 0 and loop_cnt < 3:
        # Limit walk as don't want to searchin entire drive!
        search_path = os.path.abspath(os.path.join(search_path, '..'))
        product_dir = glob.glob(os.path.join(search_path, '**', PRODUCT_DIR),
                                recursive=True
                                )
        loop_cnt += 1

    try:
        product_path = product_dir[0]
    except IndexError as err:
            _pathnotfound('product', search_path)

    # Find required version of the product.
    # Assume directory names are 'v' num or 'latest'
    product_version = str(product_version).lower()
    if product_version != PRODUCT_VERSION and not product_version.startswith('v'):
        product_version = 'v' + product_version

    # Find required product directory
    product_path = os.path.join(product_path, product_version)
    if not os.path.isdir(product_path):
        product_path = os.path.join(product_path, PRODUCT_VERSION)
        product_version = PRODUCT_VERSION

    if product_version == PRODUCT_VERSION:
        # Get the actual number of the version
        try:
            product_version = os.path.basename(
                    sorted(glob.glob(os.path.join(product_path, '../v*')))[-1]
                    )
        except IndexError as err:
            # No v numbers so just return the string
            pass

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
              product_path: str='.',
              vocab_types: [str, list]=None) -> Mapping:
    """Determine code source for documentation

    """

    _d = lambda t: {k:v for k, v in zip(('version', 'path'), t)}

    def_dict = {'standard': _d(get_std(std_path, std_version)),
                'product': _d(get_product(product_path, product_version)),
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