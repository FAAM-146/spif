import glob
import json
import shutil
from typing import Mapping
import os
import sys

# Path to spif standard dir
spif_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..',
                                        'standard')
                                        )

# Default variables that can be passed from Sphinx to this script
STD = 'latest'      # Version of the spif standard. Default is highest v number
VERSION = 'latest'  # Version of the product. Default is latest
DOC_TYPES = 'all'   # Type of vocabulary to include in documentation

# To modify the defaults when building with Sphinx;
# shinx-build -D std=1 -D version=1.2 -D doc_types=required,optional source/ build/
#
# This will build html output (the default) for v1 of the standard with v1.2
# products (will fall back to latest if v1.2 does not exist) and include
# information on required and optional vocabulary.
if not std:
    std = STD
if not version:
    version = VERSION
if not doc_types:
    doc_types = DOC_TYPES

# Find required version of the standard. Assume directories are v1, v2, etc
std = str(std).lower()
std += 'v' if not std.startswith('v'):
if not glob.glob(std, std_dir):
    # If requested std does not exist then default to the latest one
    std_dir = sorted(glob.glob('v*', std_dir))[-1]
    std = os.path.basename(std_dir)
else:
    std_dir = glob.glob(std, std_dir)

# Find required version of the standard.
# Assume directory names are 'v' num or 'latest'
version = str(version).lower()
if version != VERSION and not version.startswith('v'):
    version += 'v'

# Find required version
ver_dir = os.path.join(spif_dir, 'products', version)
if not os.path.isdir(ver_dir):
    ver_dir = os.path.join(spif_dir, 'products', VERSION)





# Determine what type of vocabulary to include in docs
doc_types = [s.lower() for s in list(doc_types)]
incl_required = True
incl_optional = False

if set('all', 'both').union(doc_types):
    incl_required = True
    incl_optional = True
else:
    if set(['required', 'mandatory']).union(doc_types):
        incl_required = True
    elif set(['optional']).union(doc_types):
        incl_optional = True
    elif not set(['required', 'mandatory']).union(doc_types):
        incl_required = False




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

    parser = argparse.ArgumentParser(usage=usage,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description=description,
            epilog=epilog)

    # Optional arguments
    parser.add_argument('-v', '--version',
                        action='store',
                        dest='version',
                        default='latest',
                        type=str,
                        help=("Version of the product that will be used "
                              "to create the documentation. If the version "
                              "given does not exist then will default "
                              "to 'latest'."))
    parser.add_argument('--process',
                        action='store',
                        dest='process_type',
                        choices=['all', 'both',
                                 'required', 'mandatory',
                                 'optional'],
                        default='all',
                        type=str,
                        help=("Designates what types of vocabulary to include "
                              "in documentation; required, optional, or both. "
                              "Default is 'all' so both required and optional "
                              "vocabulary are included in documentation."))


    definition = os.environ['FAAM_PRODUCT'] #/home/dave/vcs/faam-data/products/latest/core_faam_YYYYmmdd_v005_rN_xNNN.json'
    copy_introduction()
    populate_introduction(definition)
    copy_global_attrs()
    populate_global_attrs(definition)
    copy_variables()
    populate_variables(definition)


