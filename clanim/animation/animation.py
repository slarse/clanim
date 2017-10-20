# -*- coding: utf-8 -*-
"""
.. module: animation
    :platform: Unix
    :synopsis: _Animation decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import itertools
import functools
from ..util import concatechain, BACKSPACE_GEN, BACKLINE_GEN
from ..cli import BACKLINE, BACKSPACE
from .alnum import big_message

class _Animation:
    """A wrapper class for animation generators. It automatically backs up
    the cursor after each frame, and provides reset and erase functionality.

    Should only ever be used internally in the clanim package, and only
    as an argumentless decorator.
    """
    def __init__(self, animation_func, current_generator=None,
                 back_up_generator=None, animation_args=None,
                 animation_kwargs=None):
        self._animation_func = animation_func
        self._current_generator = current_generator
        self._back_up_generator = back_up_generator
        self._animation_args = animation_args
        self._animation_kwargs = animation_kwargs
        self._current_frame = ""
        functools.update_wrapper(self, self._animation_func)

    def reset(self):
        """Reset the current animation generator."""
        animation_gen = self._animation_func(
            *self._animation_args, **self._animation_kwargs)
        self._current_generator = itertools.cycle(
            concatechain(animation_gen, self._back_up_generator))

    def get_erase_frame(self):
        """Return a frame that completely erases the current frame, and then
        backs up.

        Assumes that the current frame is of constant width."""
        lines = self._current_frame.split('\n')
        width = len(lines[0])
        height = len(lines)
        line = ' '*width
        if height == 1:
            frame = line + BACKSPACE*width
        else:
            frame = '\n'.join([line]*height) + BACKLINE*(height - 1)
        return frame

    def __next__(self):
        self._current_frame = next(self._current_generator)
        return self._current_frame

    def __call__(self, *args, **kwargs):
        cls = self.__class__
        self._animation_args = args
        self._animation_kwargs = kwargs
        self._back_up_generator = _get_back_up_generator(self._animation_func,
                                                         *args, **kwargs)
        self.reset()
        return cls(self._animation_func, self._current_generator,
                   self._back_up_generator, args, kwargs)

    def __iter__(self):
        return iter(self._current_generator)

def _get_back_up_generator(animation_func, *args, **kwargs):
    """Create a generator for the provided animation function that backs up
    the cursor after a frame. Assumes that the animation function provides
    a generator that yields strings of constant width and height.

    Args:
        animation_func (function): A function that returns an animation generator.
        args (tuple): Arguments for animation_func.
        kwargs (dict): Keyword arguments for animation_func.
    Returns:
        generator: A generator that generates backspace/backline characters for
        the animation func generator.
    """
    lines = next(animation_func(*args, **kwargs)).split('\n')
    width = len(lines[0])
    height = len(lines)
    if height == 1:
        return BACKSPACE_GEN(width)
    else:
        return BACKLINE_GEN(height)

def _backspaced_single_line_animation(animation, *args, **kwargs):
    """Turn an animation into an automatically backspaced animation.

    Args:
        animation (func): A function that returns a generator that yields
        strings for animation frames.
        args (tuple): Arguments for the animation function.
        kwargs (dict): Keyword arguments for the animation function.
    Returns:
        The animation generator, with backspaces applied to each but the first
        frame.
    """
    animation_gen = animation(*args, **kwargs)
    yield next(animation_gen)
    yield from concatechain(BACKSPACE_GEN(kwargs['width']), animation_gen)

def _raise_value_error_if_width_is_too_small(width, limit=1):
    """Raise width error if the width is less than the limit.

    Args:
        width: Any width that is orderable, but must be of the same type as
        limit.
        limit: Any width that is orderable, but must be of the same type
        as width.
    Raises:
        ValueError
    """
    if width <= limit:
        raise ValueError("Argument 'width' must be greater than {}"
                         .format(str(limit)))
