# -*- coding: utf-8 -*-
"""
.. module: animation
    :platform: Unix
    :synopsis: _Animation decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import itertools
import functools
from .util import concatechain, BACKSPACE_GEN, BACKLINE_GEN, BACKSPACE, BACKLINE
from .alnum import big_message

class _Animation:
    """A wrapper class for animation generators making them resettable.

    This class is only to be used internally in the clanim package!"""
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
    yield from concatechain(BACKSPACE_GEN(kwargs['size']), animation_gen)


@_Animation
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

@_Animation
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

def _multi_line_animation(lines, animation_, *args, **kwargs):
    """Take any of the _single_line_<animatno> and turn them into multi line
    animations!

    Args:
        lines (int): The amount of lines to animate.
        animation_ (function): A function that returns an animation generator.
        args (tuple): Arguments for the animation function.
        kwargs (dict): Keyword arguments for the animation function.
    """
    animations = []
    for i in range(lines):
        animations.append(animation_(*args, **kwargs))
        for _ in range(i): # advance spinners
            next(animations[i])
    animation_gen = concatechain(*animations, separator='\n')
    yield from animation_gen

@_Animation
def char_waves(char='#', size=10, lines=3):
    """Multi line version of the char_wave animation.

    Args:
        char (str): The character.
        size (int): The width of the animation.
        lines (int): The height of the animation.
    Returns:
        generator: A generator that cycles a multi-line animation forever.
    """
    return _multi_line_animation(lines, char_wave, size=size, char=char)

@_Animation
def arrows(size=10, lines=3):
    """Multi line version of the arrow animation.

    Args:
        size (int): The width of the animation.
        lines (int): The height of the animation.
    Returns:
        generator: A generator that cycles a multi-line animation forever.
    """
    return _multi_line_animation(lines, arrow, size=size)

@_Animation
def spinners(size=10, lines=3):
    """Multi line version of the spinner animation.
    
    Args:
        size (int): The width of the animation.
        lines (int): The height of the animation.
    Returns:
        generator: A generator that cycles a multi-line animation forever.
    """
    return _multi_line_animation(lines, spinner, size=size)
        
@_Animation
def spinner(size=10):
    r"""Create a generator that yields strings for a spinner animation. The
    strings are padded with whitespace to make the width constant. A spinner
    of size 4 will look like this:
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
        size (int): The width of the animation.
    """
    raise_value_error_if_size_is_too_small(size, limit=0)
    spinner_ = itertools.cycle(['\\', '|', '/', '-'])
    spinner_pos = 0
    padding = size - 1
    while True:
        left_padding = ' '*(spinner_pos//4)
        right_padding = ' '*(padding - spinner_pos//4)
        frame = left_padding + next(spinner_) + right_padding
        spinner_pos = (spinner_pos + 1) % (size*4)
        yield frame

@_Animation
def scrolling_text(msg, width=50):
    yield from big_message(msg, width=width)

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
