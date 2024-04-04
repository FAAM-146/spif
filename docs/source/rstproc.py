
import re
from typing import Mapping

import pdb

import preprocessor as prep


__all__ = ['rst_grp',
           'rst_attrs',
           'rst_vars',
           ]


def _esc(s):
    """ Include \ in strings to escape rst special characters
    """
    specials = '*_:'
    return re.sub(r'([\*\_\:])', r'\\\1', s)


def rst_grp(group: dict=None, level: int=0, **kwargs) -> str:
    """Create restructured text string of group"""

    if not group:
        return ''

    if group["meta"].get("file_pattern"):
        name = "Global"
        path = name
    else:
        name = group["meta"].get("name", 'unknown')
        path = group["meta"]["path"] if group["meta"].get("path") else name

    # Initialise a rst file for this group
    text = f'..\n  File describing contents of {name} group\n\n'
#    text += prep.rst_substitutions(level=level)


    text += f'\n{_esc(path)}\n{"-" * len(_esc(path))}\n\n'

    text += (f':Description: {_esc(group["meta"]["description"])}\n'
             if group["meta"].get("description") else ''
             )
    text += (f':File Pattern: {_esc(group["meta"]["file_pattern"])}\n'
             if group["meta"].get("file_pattern") else ''
             )
    references = group['meta'].get('references', '')
    references = ' | '.join([f'`{i[0]} <{i[1]}>`_' for i in references])
    text += (f':References: {references}\n'
             if references else ''
             )
    text += '\n\n'

    # Add group attributes if required
    text += f'Group Attributes:\n{"^"*17}\n' if  group['attributes'] else ''
    text += rst_attrs(group['attributes'], level=level, **kwargs)

    # Add group variables if required
    text += f'Group Variables:\n{"^"*16}\n\n' if  group['variables'] else ''
    text += rst_vars(group['variables'], level=level, **kwargs)

    return text


def rst_attrs(attributes: dict=None, level: int=0, **kwargs) -> str:
    """Create restructured text string of attributes"""

    text = ''

    if not attributes:
        return text

    for attr_key, attr_value in attributes.items():
            text += f'  * ``{attr_key}`` : {str(attr_value)}\n'
    text += '\n'

    return text


def rst_vars(variables: dict=None,
             level: int=0,
             incl_required: bool=True,
             incl_optional: bool=False,
             **kwargs) -> str:
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

        name = var["meta"].get("name", 'unknown')
        sec_quote = '"'
        text += f'{_esc(name)}\n{sec_quote * len(_esc(name))}\n'
        text += ':red:`REQUIRED`\n\n' if var["meta"].get("required") else '\n'
        text += f'  :Datatype: `{var["meta"]["datatype"]}`\n'
        text += f'  :Dimensions: {", ".join(var["dimensions"])}\n'
        text += (f'  :Description: {var["meta"]["description"]}\n\n'
                 if var["meta"].get("description")
                 else '\n')

        text += rst_attrs(var.get('attributes', None), level=level, **kwargs)
        text += '\n'

    return text



