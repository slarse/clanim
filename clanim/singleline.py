# -*- coding: utf-8 -*-
"""
.. module: singleline
    :platform: Unix
    :synopsis: Singleline animations.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import itertools
from clanimtk import animation
from clanimtk import types


@animation
def char_wave(char: str = '#', width: int = 10) -> types.FrameFunction:
    """Create a generator that cycles a wave of the given char. The animation is
    padded with whitespace to make its width constant. As an example if the char
    given is '#', and the width is 4, then the animation will look like this
    (note that underscores signify whitespace):

    .. code-block:: bash

        #___
        ##__
        ###_
        ####
        ###_
        ##__
        #___

    Args:
        char: A single character, the character to make up the animation.
        width: Total width of the animation (this is constant). This must
        be greater than 1.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    if len(char) != 1:
        raise ValueError("The argument 'char' must be a single character, and "
                         "not a string of length {}".format(len(char)))
    if width <= 1:
        raise ValueError("width must be greater than 1")
    increasing = ((char * n).ljust(width) for n in range(1, width))
    decreasing = ((char * n).ljust(width) for n in range(width, 1, -1))
    wave = itertools.chain(increasing, decreasing)
    return itertools.cycle(wave)


@animation
def arrow(width: int = 5) -> types.FrameFunction:
    """Create a generator that cycles an arrow moving back and forth. The
    animation is padded with whitespace to make the width constant. As an
    example, if the width is 4, the animation looks like this (note that
    underscores signify whitespace):

    .. code-block:: bash

        >___
        _>__
        __>_
        ___>
        __<_
        _<__

    Args:
        width: Total width of the animation (this is constant). This must
        be greater than 1.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    if width <= 1:
        raise ValueError("width must be greater than 1")
    padding = width - 1
    right_arrows = (' ' * i + '>' + ' ' * (padding - i)
                    for i in range(padding))
    left_arrows = (' ' * (padding - i) + '<' + ' ' * i for i in range(padding))
    return itertools.cycle(itertools.chain(right_arrows, left_arrows))


@animation
def spinner(width: int = 10) -> types.FrameFunction:
    r"""Create a generator that yields strings for a spinner animation. The
    strings are padded with whitespace to make the width constant. A spinner
    of width 4 will look like this:

    .. code-block:: bash

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
        width: The width of the animation.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    if width <= 0:
        raise ValueError("width must be greater than 0")
    spinner_ = itertools.cycle(['\\', '|', '/', '-'])
    spinner_pos = 0
    padding = width - 1
    while True:
        left_padding = ' ' * (spinner_pos // 4)
        right_padding = ' ' * (padding - spinner_pos // 4)
        frame = left_padding + next(spinner_) + right_padding
        spinner_pos = (spinner_pos + 1) % (width * 4)
        yield frame
