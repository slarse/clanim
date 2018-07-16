# -*- coding: utf-8 -*-
"""
.. module: multiline
    :synopsis: Multiline animations.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
from clanimtk import animation
from clanimtk import types
from clanimtk.util import concatechain
from clanimtk.decorator import multiline_frame_function
from clanim.singleline import arrow, char_wave, spinner
from clanim.alnum import big_message


@animation
def char_waves(char:str=  '#', width: int =10, height: int =3) -> types.FrameFunction:
    """Multi line version of the char_wave animation.

    Args:
        char: The character.
        width: The width of the animation.
        height: The height of the animation.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    return char_wave


@animation
def arrows(height: int=5, width: int=10) -> types.FrameFunction:
    """Multi line version of the arrow animation.

    Args:
        width: The width of the animation.
        height: The height of the animation.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    return multiline_frame_function(arrow, height, offset=0, width=width)


@animation
def spinners(width: int=10, height: int=3) -> types.FrameFunction:
    """Multi line version of the spinner animation.

    Args:
        width: The width of the animation.
        height: The height of the animation.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    return multiline_frame_function(spinner, height, offset=0, width=width)


@animation
def scrolling_text(msg: str, width: int=50) -> types.FrameFunction:
    """Animates the given message with big, friendly scrolling characters that
    are 5x5 cells large. See  for available
    characters!

    .. :py:module:: clanimtk.big_char

    Args:
        msg: The message to animate.
        width: Width (in cells) of the animation.
    Returns:
        a FrameFunction (or an Animation if annotated with ``@animation``)
    """
    if width < 9:
        raise ValueError("width must be at least 9")
    yield from big_message(msg, width=width)
