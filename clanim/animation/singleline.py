# -*- coding: utf-8 -*-
"""
.. module: singleline
    :platform: Unix
    :synopsis: Singleline animations.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import itertools
from .animation import (_Animation, _raise_value_error_if_width_is_too_small)

@_Animation
def char_wave(char='#', width=10):
    """Create a generator that cycles a wave of the given char. The animation is
    padded with whitespace to make its width constant. As an example if the char
    given is '#', and the width is 4, then the animation will look like this
    (note that underscores signify whitespace):
        #___
        ##__
        ###_
        ####
        ###_
        ##__
        #___

    Args:
        char (str): A single character, the character to make up the animation.
        width (int): Total width of the animation (this is constant). This must
        be greater than 1.
    Returns:
        generator: A generator that cycles the animation forever.
    Raises:
        ValueError
    """
    if len(char) != 1:
        raise ValueError("The argument 'char' must be a single character, and "
                         "not a string of length {}".format(len(char)))
    _raise_value_error_if_width_is_too_small(width)
    increasing = ((char*n).ljust(width) for n in range(1, width))
    decreasing = ((char*n).ljust(width) for n in range(width, 1, -1))
    wave = itertools.chain(increasing, decreasing)
    return itertools.cycle(wave)

@_Animation
def arrow(width=5):
    """Create a generator that cycles an arrow moving back and forth. The
    animation is padded with whitespace to make the width constant. As an
    example, if the width is 4, the animation looks like this (note that
    underscores signify whitespace):
        >___
        _>__
        __>_
        ___>
        __<_
        _<__

    Args:
        width (int): Total width of the animation (this is constant). This must
        be greater than 1.
    Returns:
        generator: A generator that cycles the animation forever.
    """
    _raise_value_error_if_width_is_too_small(width)
    padding = width - 1
    right_arrows = (' '*i + '>' + ' '*(padding - i) for i in range(padding))
    left_arrows = (' '*(padding - i) + '<' + ' '*i for i in range(padding))
    return itertools.cycle(itertools.chain(right_arrows, left_arrows))

@_Animation
def spinner(width=10):
    r"""Create a generator that yields strings for a spinner animation. The
    strings are padded with whitespace to make the width constant. A spinner
    of width 4 will look like this:
        \___
        |___
        /___
        -___
        _\__
        _|__
        _/__
        _-__
        __\_
        __|_
        __/_
        __-_
        ___\

    Args:
        width (int): The width of the animation.
    """
    _raise_value_error_if_width_is_too_small(width, limit=0)
    spinner_ = itertools.cycle(['\\', '|', '/', '-'])
    spinner_pos = 0
    padding = width - 1
    while True:
        left_padding = ' '*(spinner_pos//4)
        right_padding = ' '*(padding - spinner_pos//4)
        frame = left_padding + next(spinner_) + right_padding
        spinner_pos = (spinner_pos + 1) % (width*4)
        yield frame
