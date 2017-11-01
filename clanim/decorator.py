# -*- coding: utf-8 -*-
"""
.. module:: decorator
    :platform: Unix
    :synopsis: This module contains all of the clanim decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import asyncio
import logging
import functools
import sys
import daiquiri
from .animation.singleline import arrow
from .util import get_supervisor

daiquiri.setup(level=logging.ERROR)
LOGGER = daiquiri.getLogger(__name__)

ANNOTATED = '_clanim_annotated'
ASYNC_ANIMATED = '_clanim_asnyc_animated'

class Annotate:
    """A decorator meant for decorating functions that are decorated with the
    Animation decorator. It prints a message to stdout before and/or after the
    function has finished.

    This decorator can also be used standalone, but you should NOT decorate a
    function that is decorated with Annotate with Animate. That is to say,
    the decorator order must be like this:

        @Annotate
        @Animate
        def some_function()
            pass
    """
    def __init__(self, *,start_msg=None, end_msg=None, start_no_nl=False):
        """Note that both arguments are keyword only arguments.

        Args:
            start_msg (str): A message to print before the function runs.
            end_msg (str): A message to print after the function has finished.
            start_no_nl (bool): If True, no newline is appended after the
            start_msg.
        """
        if start_msg is None and end_msg is None:
            raise ValueError(
                "At least one of 'start_msg' and 'end_msg' must be specified.")
        self._start_msg = start_msg
        self._end_msg = end_msg
        self._start_no_nl = start_no_nl

    def _start_print(self):
        """Print the start message with or without newline depending on the
        self._start_no_nl variable.
        """
        if self._start_no_nl:
            sys.stdout.write(self._start_msg)
            sys.stdout.flush()
        else:
            print(self._start_msg)

    def __call__(self, func, *args, **kwargs):
        """
        Args:
            func (function): The annotated function.
            args (tuple): Arguments for func.
            kwargs (dict): Keyword arguments for func.
        """
        if asyncio.iscoroutinefunction(func) or (hasattr(func, ASYNC_ANIMATED) 
                                                 and getattr(func, ASYNC_ANIMATED)):
            return self._async_call(func, *args, **kwargs)
        else:
            return self._sync_call(func, *args, **kwargs)

    def _sync_call(self, func, *args, **kwargs):
        """__call__ function for regular synchronous functions.

        Args:
            func (function): The annotated function.
            args (tuple): Arguments for func.
            kwargs (dict): Keyword arguments for func.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self._start_msg:
                self._start_print()
            result = func(*args, **kwargs)
            if self._end_msg:
                print(self._end_msg)
            return result
        setattr(wrapper, ANNOTATED, True)
        return wrapper

    def _async_call(self, func, *args, **kwargs):
        """__call__ functino for asyncio coroutines.

        Args:
            func (function): The annotated function.
            args (tuple): Arguments for func.
            kwargs (dict): Keyword arguments for func.
        """
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            if self._start_msg:
                print(self._start_msg)
            result = await func(*args, **kwargs)
            if self._end_msg:
                print(self._end_msg)
            return result
        setattr(wrapper, ANNOTATED, True)
        return wrapper

class Animate:
    """A decorator class for adding a CLI animation to a slow-running funciton.
    Animate uses introspection to figure out if the function it decorates is
    synchronous (defined with 'def') or asynchronous (defined with 'async def'),
    and works equally well with both.
    """

    def __init__(self, func=None, *, animation=arrow(), step=.1):
        """Constructor.

        Args:
            func (function): If Animate is used without kwargs, then the
            function it decorates is passed in here. Otherwise, this is None.
            This argument should NOT be given directly.
            animation (generator): A generator that yields strings for the animation.
            step (float): Seconds between each animation frame.
        """
        if func and not callable(func):
            raise TypeError("argument 'func' for {!r} must be "
                            "callable".format(self.__class__.__name__))
        if callable(func):
            if asyncio.iscoroutinefunction(func):
                setattr(self, ASYNC_ANIMATED, True)
            self._raise_if_annotated(func)
            partial = functools.partial(self._call_without_kwargs, animation,
                                        step, func)
            functools.update_wrapper(self, func)
        else:
            partial = functools.partial(self._call_with_kwargs, animation,
                                        step)
        self._call = partial

    def _call_without_kwargs(self, animation_, step, func, *args, **kwargs):
        """The function that __call__ calls if the constructor did not recieve
        any kwargs.

        NOTE: This method should ONLY be called directly in the constructor!

        Args:
            animation_ (generator): A generator yielding strings for the animation.
            step (float): Seconds between each animation frame.
            func (function): A function to run alongside an animation.
            args (tuple): Positional arguments for func.
            kwargs (dict): Keyword arguments for func.
        Returns:
            A function if func is a function, and a coroutine if func is a
            coroutine.
        """
        return get_supervisor(func)(animation_, step, *args, **kwargs)

    def _call_with_kwargs(self, animation_, step, func):
        """The function that __call__ calls when the constructor received kwargs.

        NOTE: This method should ONLY be called directly in the constructor!

        Args:
            animation_ (generator): A generator yielding strings for the animation.
            func (function): A function to run alongside an animation.
        Returns:
            A function if func is a function, and a coroutine if func is a
            coroutine.
        """
        self._raise_if_annotated(func)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return get_supervisor(func)(animation_, step, *args, **kwargs)
        if asyncio.iscoroutinefunction(func):
            setattr(wrapper, ASYNC_ANIMATED, True)
        return wrapper

    def __call__(self, func=None, *args, **kwargs):
        """Make the class instance callable.

        func (function): If the
        """
        LOGGER.info(f'Passing through __call__, calling {self._call}')
        return self._call(func, *args, **kwargs) if func else self._call()

    def _raise_if_annotated(self, func):
        """Raise TypeError if a function is decorated with Annotate, as such
        functions cause visual bugs when decorated with Animate.

        Animate should be wrapped by Annotate instead.

        Args:
            func (function): Any callable.
        Raises:
            TypeError
        """
        if hasattr(func, ANNOTATED) and getattr(func, ANNOTATED):
            msg = ('Functions decorated with {!r} '
                   'should not be decorated with {!r}.\n'
                   'Please reverse the order of the decorators!'
                   .format(self.__class__.__name__, Annotate.__name__))
            raise TypeError(msg)
