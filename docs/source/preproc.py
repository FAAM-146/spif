import glob
import json
import shutil
from typing import Mapping
import os
import sys


import pdb

import preprocessor as prep

pdb.set_trace()


# Path to spif standard dir
spif_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                        '..', '..',
                                        'standard')
                                        )

# Path to templates
template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            'templates')
                                            )


# Add standard
#sys.path.append('../../')
#from attributes import GlobalAttributes


def init() -> None:
    pass


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


def rst_attributes(attributes: dict=None) -> str:
    """Create restructured text string of attributes"""

    text = ''

    if not attributes:
        return text

    for attr_key, attr_value in attributes.items():
            text += f'* ``{attr_key}`` : {str(attr_value)}\n'

    return text


def rst_variables(variables: dict=None,
                  incl_required: bool=True,
                  incl_optional: bool=False) -> str:
    """Create restructured text string of variables"""

    text = ''

    if not variables:
        return text

    for var in variables:

        if incl_required and incl_optional:
            pass
        elif incl_required and var["meta"]["required"]:
            pass
        elif incl_optional and not var["meta"]["required"]:
            pass
        else:
            continue

        _name =  f'{var["meta"]["name"]}'
        text += _name + '\n'
        text = text + ':rubric:`REQUIRED`\n' if var["meta"]["required"] else text
        text += '-' * (len(_name)) + '\n'
        text += f':Datatype: `{var["meta"]["datatype"]}`\n'
        text += f':Dimensions: {", ".join(var["dimensions"])}\n'
        text += (f':Description: {var["meta"]["description"]}\n\n'
                 if var["meta"].get("description")
                 else '\n')

        text += rst_attributes(var.get('attributes', None))
        text += '\n'

    return text


def populate_vocab_rst(definition,
                       incl_required: bool=True,
                       incl_optional: bool=False) -> None:
    """Create vocabulary description rst file"""

    pdb.set_trace()

    with open(definition, 'r') as f:
        data = json.load(f)


    variables = sorted(data['variables'], key=lambda x: x['meta']['name'])
    text = ''


    with open(os.path.join(dynamic_dir, 'variables.rst'), 'r') as f:
        rst = f.read()

    rst = rst.replace('TAG_PRODUCT_VARIABLES', text)


    with open(os.path.join(dynamic_dir, 'variables.rst'), 'w') as f:
        f.write(rst)


if __name__ == '__main__':

    import argparse

    # Define commandline options
    usage = ("make <build> FILEOPT=definition_filename "
             "STDOPT=std_version PRODOPT=product_version "
             "VOCABOPT=vocab_types")
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
                        default=None,
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

    pdb.set_trace()

    args_dict = vars(parser.parse_args())
    #args, unknown = parser.parse_known_args()

    def_dict = prep.get_definition(spif_dir, **args_dict)
    definition = def_dict['product']['path']
    populate_vocab_rst(definition, **def_dict['vocab'])

    pdb.set_trace()

    definition = os.environ['FAAM_PRODUCT'] #/home/dave/vcs/faam-data/products/latest/core_faam_YYYYmmdd_v005_rN_xNNN.json'
    copy_introduction()
    populate_introduction(definition)
    copy_global_attrs()
    populate_global_attrs(definition)
    copy_variables()
    populate_variables(definition)
