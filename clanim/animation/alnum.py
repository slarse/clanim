# -*- coding: utf-8 -*-
"""
.. module:: alnum
    :platform: Unix
    :synopsis: This module contains iterables for alphanumerical characters.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
from ..util import BACKLINE_GEN
from .big_char import CHARS

def big_message(msg, width=50):
    """Yields strings that animate large scrolling text, followed by whitespace
    the size of the width of the animation.
    
    Args:
        msg (str): The message to render as scrolling text.
        width (int): Width of the animation.
    """
    chars_per_width = (width - 2)//7
    big_chars = [CHARS[char.upper()] for char in msg]
    char_size = len(big_chars[0])
    num_chars = len(big_chars)
    seq = ['  '.join([big_chars[char][line] for char in range(num_chars)])
           for line in range(char_size)]
    accum = ['  '.join(' '*5)*chars_per_width]*5
    # yield the text
    for i in range(len(seq[0])):
        column = [line[i] for line in seq]
        accum = [accum[j] + column[j] for j in range(len(column))]
        accum = [line[-width:] for line in accum]
        next_ = '\n'.join(accum)
        yield next_
    # yield one width's worth of whitespace
    for _ in range(width):
        column = [' ']*5
        accum = [accum[j] + column[j] for j in range(len(column))]
        accum = [line[-width:] for line in accum]
        next_ = '\n'.join(accum)
        yield next_
