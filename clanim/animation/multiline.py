# -*- coding: utf-8 -*-
"""
.. module: multiline
    :platform: Unix
    :synopsis: Multiline animations.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
from .animation import _Animation, _raise_value_error_if_width_is_too_small
from .singleline import arrow, char_wave, spinner
from .alnum import big_message
from ..util import concatechain

@_Animation
def char_waves(char='#', width=10, height=3):
    """Multi line version of the char_wave animation.

    Args:
        char (str): The character.
        width (int): The width of the animation.
        height (int): The height of the animation.
    Returns:
        generator: A generator that cycles a multi-line animation forever.
    """
    return _multi_line_animation(height, char_wave, width=width, char=char)

@_Animation
def arrows(width=10, height=3):
    """Multi line version of the arrow animation.

    Args:
        width (int): The width of the animation.
        height (int): The height of the animation.
    Returns:
        generator: A generator that cycles a multi-line animation forever.
    """
    return _multi_line_animation(height, arrow, width=width)

@_Animation
def spinners(width=10, height=3):
    """Multi line version of the spinner animation.

    Args:
        width (int): The width of the animation.
        height (int): The height of the animation.
    Returns:
        generator: A generator that cycles a multi-line animation forever.
    """
    return _multi_line_animation(height, spinner, width=width)

@_Animation
def scrolling_text(msg, width=50):
    """Animates the given message with big, friendly scrolling characters that
    are 5x5 cells large.

    Args:
        msg (str): The message to animate.
        width (int): Width (in cells) of the animation.
    """
    _raise_value_error_if_width_is_too_small(width, limit=9)
    yield from big_message(msg, width=width)


def _multi_line_animation(height, animation_, *args, **kwargs):
    """Take a single line animation and multiline it!

    Args:
        height (int): The amount of lines to animate.
        animation_ (function): A function that returns an animation generator.
        args (tuple): Arguments for the animation function.
        kwargs (dict): Keyword arguments for the animation function.
    """
    animations = []
    for i in range(height):
        animations.append(animation_(*args, **kwargs))
        for _ in range(i): # advance animation
            next(animations[i])
    animation_gen = concatechain(*animations, separator='\n')
    yield from animation_gen
