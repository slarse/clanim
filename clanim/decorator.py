# -*- coding: utf-8 -*-
"""
.. module:: decorator
    :platform: Unix
    :synopsis: This module contains all of the clanim decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import logging
import functools
import daiquiri
from .animation import arrow
from .util import get_supervisor

daiquiri.setup(level=logging.ERROR)
LOGGER = daiquiri.getLogger(__name__)

ANNOTATED = '_clanim_annotated'

class Annotate:
    """A decorator meant for decorating functions that are decorated with the
    Animation decorator. It prints a message to stdout before and/or after the
    function has finished.

    This decorator can also be used standalon, but you should NOT decorate a
    function that is decorated with Animate with Annotate. That is to say,
    the decorator order must be like this:

        @Annotate
        @Animate
        def some_function()
            pass
    """
    def __init__(self, before_msg, after_msg):
        """
        Args:
            working_msg (str): A message to print before the function runs.
            after_msg (str): A message to print after the function has finished.
        """
        self._before_msg = before_msg
        self._after_msg = after_msg

    def __call__(self, func, *args, **kwargs):
        """
        Args:
            func (function): The annotated function.
            args (tuple): Arguments for func.
            kwrags (dict): Keyword arguments for func.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if self._before_msg:
                print(self._before_msg)
            result = func(*args, **kwargs)
            if self._after_msg:
                print(self._after_msg)
            return result
        setattr(wrapper, ANNOTATED, True)
        return wrapper

class Animate:
    """A decorator class for adding a CLI animation to a slow-running funciton.
    Animate uses introspection to figure out if the function it decorates is
    synchronous (defined with 'def') or asynchronous (defined with 'async def'),
    and works equally well with both.

    The decorator takes a single, optional argument: The animation to be used.
    If no argument is given, the 'arrow' animation is selected by default.
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
