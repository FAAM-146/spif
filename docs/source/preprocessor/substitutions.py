""" File of dynamic rst substitutions """

from numpy import clip

__all__ = ['rst_substitutions']


# Section heading indicators
section_markers = ['=', '-', '^', '"']


def _level_rst(level=0) -> str:

    return section_markers[clip(level, 0, 3)]


def _level_subs(level=0) -> str:

    text = ""

    text += f".. |tab|: replace:: {'  ' * level}"
    text += f".. |sec|: replace:: {_level_rst(level)}"

    return text


def rst_substitutions(**kwargs) -> str:

    text = ""

    text += _level_subs(kwargs.get(level, None))

    return text

