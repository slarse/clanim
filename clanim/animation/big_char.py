# -*- coding: utf-8 -*-
"""
.. module:: big_char
    :platform: Unix
    :synopsis: This module contains all big characters for the scrolling text
    animation.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""

CHAR_HEIGHT = 5
CHAR_WIDTH = 5

_A = [' XXX ',
      'X   X',
      'XXXXX',
      'X   X',
      'X   X']

_B = ['XXXX ',
      'X   X',
      'XXXXX',
      'X   X',
      'XXXX ']

_C = ['XXXXX',
      'X    ',
      'X    ',
      'X    ',
      'XXXXX']

_D = ['XXXX ',
      'X   X',
      'X   X',
      'X   X',
      'XXXX ']

_E = ['XXXXX',
      'X    ',
      'XXXXX',
      'X    ',
      'XXXXX']

_F = ['XXXXX',
      'X    ',
      'XXXXX',
      'X    ',
      'X    ']

_G = ['XXXXX',
      'X    ',
      'X  XX',
      'X   X',
      'XXXXX']

_H = ['X   X',
      'X   X',
      'XXXXX',
      'X   X',
      'X   X']

_I = ['XXXXX',
      '  X  ',
      '  X  ',
      '  X  ',
      'XXXXX']

_J = ['XXXXX',
      '    X',
      '    X',
      'x   X',
      'XXXXX']

_K = ['X   X',
      'X  X ',
      'XXX  ',
      'X  X ',
      'X   X']

_L = ['X    ',
      'X    ',
      'X    ',
      'X    ',
      'XXXXX']

_M = [' X X ',
      'X X X',
      'X X X',
      'X   X',
      'X   X']

_N = ['X   X',
      'XX  X',
      'X X X',
      'X  XX',
      'X   X']

_O = [' XXX ',
      'X   X',
      'X   X',
      'X   X',
      ' XXX ']

_P = ['XXXX ',
      'X   X',
      'XXXX ',
      'X    ',
      'X    ']

_Q = [' XXX ',
      'X   X',
      'X   X',
      ' XXX ',
      'XX   ']

_R = ['XXXX ',
      'X   X',
      'XXXX ',
      'X   X',
      'X   X']

_S = ['XXXXX',
      'X    ',
      'XXXXX',
      '    X',
      'XXXXX']

_T = ['XXXXX',
      '  X  ',
      '  X  ',
      '  X  ',
      '  X  ']

_U = ['X   X',
      'X   X',
      'X   X',
      'X   X',
      'XXXXX']

_V = ['X   X',
      'X   X',
      'X   X',
      ' X X ',
      '  X  ']

_W = ['X   X',
      'X   X',
      'X X X',
      'X X X',
      ' X X ',]

_X = ['X   X',
      ' X X ',
      '  X  ',
      ' X X ',
      'X   X']

_Y = ['X   X',
      ' X X ',
      '  X  ',
      '  X  ',
      '  X  ']

_Z = ['XXXXX',
      '   X ',
      '  X  ',
      ' X   ',
      'XXXXX']

_SPACE = ['     ']*5

_COMMA = ['     ',
          '     ',
          '     ',
          '   X ',
          ' XX  ']

_DOT = ['     ',
        '     ',
        '     ',
        '     ',
        '  X  ']

_EXCLAMATION = ['  X  ',
                '  X  ',
                '  X  ',
                '     ',
                '  X  ']

_QUESTION = [' XXX ',
             'X   X',
             '   X ',
             '  X  ',
             '  X  ']

CHARS = {'A': _A, 'B': _B, 'C': _C, 'D': _D, 'E': _E, 'F': _F, 'G': _G, 'H': _H,
         'I': _I, 'J': _J, 'K': _K, 'L': _L, 'M': _M, 'N': _N, 'O': _O, 'P': _P,
         'Q': _Q, 'R': _R, 'S': _S, 'T': _T, 'U': _U, 'V': _V, 'W': _W, 'X': _X,
         'Y': _Y, 'Z': _Z, ' ': _SPACE, '!': _EXCLAMATION, ',': _COMMA,
         '.': _DOT, '?': _QUESTION}
