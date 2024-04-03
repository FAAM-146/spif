
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


def rst_grp(group: dict=None, level: int=0) -> str:
    """Create restructured text string of group"""

    if not group:
        return ''

    pdb.set_trace()

    # Initialise a rst file for this group
    text = prep.rst_substitutions(level=level)
    if group["meta"].get("file_pattern"):
        name = "Global"
    else:
        name = group['meta'].get('name', 'unknown')

    text += f'\n{_esc(name)}\n{"|sec|" * len(name)}\n'

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
    text += '**Group Attributes:**\n' if  group['attributes'] else ''
    text += rst_attrs(group['attributes'], level=level)

    # Add group variables if required
    text += '**Group Variables:**\n' if  group['variables'] else ''
    text += rst_vars(group['varables'], level=level)

    return text


def rst_attrs(attributes: dict=None, level: int=0) -> str:
    """Create restructured text string of attributes"""

    text = ''

    if not attributes:
        return text

    for attr_key, attr_value in attributes.items():
            text += f'* ``{attr_key}`` : {str(attr_value)}\n'

    return text


def rst_vars(variables: dict=None,
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

        name = group['meta'].get('name', 'unknown')
        text += f'{_esc(name)}\n{"~" * len(name)}\n'
        text += ':rubric:`REQUIRED`\n' if var["meta"].get("required") else ''
        text += f':Datatype: `{var["meta"]["datatype"]}`\n'
        text += f':Dimensions: {", ".join(var["dimensions"])}\n'
        text += (f':Description: {var["meta"]["description"]}\n\n'
                 if var["meta"].get("description")
                 else '\n')

        text += rst_attributes(var.get('attributes', None))
        text += '\n'

    return text



