""" File of dynamic rst substitutions """

from numpy import clip

__all__ = ['rst_substitutions']


# Section heading indicators
section_markers = ['=', '-', '^', '"']


def _level_rst(level=0, **kwargs) -> str:

    return section_markers[clip(level, 0, 3)]


def _level_subs(level=0, **kwargs) -> str:

    text = ""

    text += f'.. |tab|: replace:: {"  " * level}\n'
    text += f'.. |sec|: replace:: {_level_rst(level)}\n'

    return text


def rst_substitutions(level=0, **kwargs) -> str:

    text = ""
    text += _level_subs(level)

    return text

