# -*- coding: utf-8 -*-
"""
.. module:: decorator
    :platform: Unix
    :synopsis: This module contains all of the clanim decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import inspect
import logging
import functools
import threading
import asyncio
import daiquiri
from .cli import sync_animation, async_animation
from .util import Signal
from .animation import arrow

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

    def __init__(self, *args, animation=arrow(), msg='Working ...', step=.1):
        """Constructor.

        Args:
            args (tuple): Should either be empty, or consist of a single callable
            (the function to run alongside the animation).
            animation (generator): A generator that yields strings for the animation.
            msg (str): A message to display alongside the animation.
            step (float): Seconds between each animation frame.
        """
        cls = self.__class__
        if len(args) > 1:
            raise TypeError("{.__name__!r} takes at most 1 positional argument "
                            "but {} were given".format(cls, len(args)))
        elif len(args) == 1:
            if callable(args[0]):
                func = args[0]
                self._call = functools.partial(self._call_no_kwargs, animation,
                                               step, msg, func)
                functools.update_wrapper(self, func)
            else:
                raise TypeError("Positional argument for {.__name__!r} must be "
                                "callable".format(cls))
        else:
            self._call = functools.partial(self._call_with_kwargs, animation,
                                           step, msg)

    async def _async_supervisor(self, func, animation_, step, msg, *args, **kwargs):
        """Supervisor for running an animation with an asynchronous function.

        Args:
            func (function): A function to be run alongside an animation.
            animation_ (generator): An infinite generator that produces
            strings for the animation.
            step (float): Seconds between each animation frame.
            msg (str): The message to be displayed next to the animation.
            *args (tuple): Arguments for func.
            **kwargs (dict): Keyword arguments for func.
        Returns:
            The result of func(*args, **kwargs)
        Raises:
            Any exception that is thrown when executing func.
        """
        animation = asyncio.ensure_future(async_animation(animation_, step, msg))
        try:
            result = await func(*args, **kwargs)
        except Exception:
            raise
        finally:
            animation.cancel()
        return result

    def _sync_supervisor(self, func, animation_, step, msg, *args, **kwargs):
        """Supervisor for running an animation with a synchronous function.

        Args:
            func (function): A function to be run alongside an animation.
            animation_ (generator): An infinite generator that produces
            strings for the animation.
            step (float): Seconds between each animation frame.
            msg (str): The message to be displayed next to the animation.
            args (tuple): Arguments for func.
            kwargs (dict): Keyword arguments for func.
        Returns:
            The result of func(*args, **kwargs)
        Raises:
            Any exception that is thrown when executing func.
        """
        signal = Signal()
        animation = threading.Thread(target=sync_animation,
                                     args=(animation_, step, msg, signal))
        animation.start()
        try:
            result = func(*args, **kwargs)
        except Exception:
            raise
        finally:
            signal.done = True
            animation.join()
        return result

    def _select_supervisor(self, func):
        """Select the supervisor to use and pre-apply the function.

        Args:
            func (function): A function.
        """
        if inspect.iscoroutinefunction(func):
            supervisor = self._async_supervisor
        else:
            supervisor = self._sync_supervisor
        return functools.partial(supervisor, func)

    def _call_no_kwargs(self, animation_, step, msg, func, *args, **kwargs):
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
        return self._select_supervisor(func)(animation_, step, msg, *args,
                                             **kwargs)

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
            return self._select_supervisor(func)(animation_, step, msg, *args,
                                                 **kwargs)
        return wrapper

    def __call__(self, *args):
        """Make the class instance callable.
        
        args (tuple): Arguments passed to the constructor of the class.
        """
        LOGGER.info(f'Passing through __call__, calling {self._call}')
        return self._call(*args)
