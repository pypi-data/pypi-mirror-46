# -*- coding: utf-8 -*-

STYLED_VERSION = '0.2.0'

try:
    from styled import Styled, StyleError
    from assets import STYLE_NAMES, FG_COLOURS, BG_COLOURS, ESC, END, COLOURS
except ImportError:
    from .styled import Styled, StyleError
    from .assets import STYLE_NAMES, FG_COLOURS, BG_COLOURS, ESC, END, COLOURS


__all__ = ['Styled', 'StyleError', 'STYLE_NAMES', 'FG_COLOURS', 'BG_COLOURS', 'END', 'ESC', 'COLOURS']