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

daiquiri.setup(level=logging.WARNING)
LOGGER = daiquiri.getLogger(__name__)

class Animate:
    """A decorator class for adding a CLI animation to a slow-running funciton.
    Animate uses introspection to figure out if the function it decorates is
    synchronous (defined with 'def') or asynchronous (defined with 'async def'),
    and works equally well with both.

    The decorator takes a single, optional argument: The animation to be used.
    If no argument is given, the 'arrow' animation is selected by default.
    """

    def __init__(self, func=None, *, animation=arrow(), msg='Working ', step=.1):
        """Constructor.

        Args:
            func (function): If Animate is used without kwargs, then the
            function it decorates is passed in here. Otherwise, this is None.
            This argument should NOT be given directly.
            animation (generator): A generator that yields strings for the animation.
            msg (str): A message to display alongside the animation.
            step (float): Seconds between each animation frame.
        """
        if callable(func):
            self._call = functools.partial(self._call_without_kwargs, animation,
                                           step, msg, func)
            functools.update_wrapper(self, func)
        elif func:
            raise TypeError("argument 'func' for {!r} must be "
                            "callable".format(self.__class__.__name__))
        else:
            self._call = functools.partial(self._call_with_kwargs, animation,
                                               step, msg)

    def _call_without_kwargs(self, animation_, step, msg, func, *args, **kwargs):
        """The function that __call__ calls if the constructor did not recieve
        any kwargs.

        NOTE: This method should ONLY be called directly in the constructor!

        Args:
            animation_ (generator): A generator yielding strings for the animation.
            step (float): Seconds between each animation frame.
            msg (str): The message to be displayed next to the animation.
            func (function): A function to run alongside an animation.
            args (tuple): Positional arguments for func.
            kwargs (dict): Keyword arguments for func.
        Returns:
            A function if func is a function, and a coroutine if func is a
            coroutine.
        """
        return get_supervisor(func)(animation_, step, msg, *args, **kwargs)

    def _call_with_kwargs(self, animation_, step, msg, func):
        """The function that __call__ calls when the constructor received kwargs.

        NOTE: This method should ONLY be called directly in the constructor!

        Args:
            animation_ (generator): A generator yielding strings for the animation.
            msg (str): The message to be displayed next to the animation.
            func (function): A function to run alongside an animation.
        Returns:
            A function if func is a function, and a coroutine if func is a
            coroutine.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return get_supervisor(func)(animation_, step, msg, *args, **kwargs)
        return wrapper

    def __call__(self, func=None, *args, **kwargs):
        """Make the class instance callable.

        func (function): If the
        """
        LOGGER.info(f'Passing through __call__, calling {self._call}')
        return self._call(func, *args, **kwargs) if func else self._call()
