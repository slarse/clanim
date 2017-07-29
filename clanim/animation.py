# -*- coding: utf-8 -*-
"""
.. module: animation
    :platform: Unix
    :synopsis: Animation decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import itertools

def char_wave(char='#', size=10):
    """Create a generator that cycles a wave of the given char. The animation is
    padded with whitespace to make its width constant. As an example if the char
    given is '#', and the size is 4, then the animation will look like this
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
        size (int): Total width of the animation (this is constant). This must
        be greater than 1.
    Returns:
        generator: A generator that cycles the animation forever.
    Raises:
        ValueError
    """
    if len(char) != 1:
        raise ValueError("The argument 'char' must be a single character, and "
                         "not a string of length {}".format(len(char)))
    raise_value_error_if_size_is_too_small(size)
    increasing = ((char*n).ljust(size) for n in range(1, size))
    decreasing = ((char*n).ljust(size) for n in range(size, 1, -1))
    wave = itertools.chain(increasing, decreasing)
    return itertools.cycle(wave)

def arrow(size=5):
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
        char (str): A single character, the character to make up the animation.
        size (int): Total width of the animation (this is constant). This must
        be greater than 1.
    Returns:
        generator: A generator that cycles the animation forever.
    """
    raise_value_error_if_size_is_too_small(size)
    padding = size - 1
    right_arrows = (' '*i + '>' + ' '*(padding - i) for i in range(padding))
    left_arrows = (' '*(padding - i) + '<' + ' '*i for i in range(padding))
    return itertools.cycle(itertools.chain(right_arrows, left_arrows))

def raise_value_error_if_size_is_too_small(size, limit=1):
    """Raise size error if the size is less than the limit.

    Args:
        size: Any size that is orderable, but must be of the same type as
        limit.
        limit: Any size that is orderable, but must be of the same type
        as size.
    Raises:
        sizeError
    """
    if size <= limit:
        raise ValueError("Argument 'size' must be greater than {}"
                         .format(str(limit)))
