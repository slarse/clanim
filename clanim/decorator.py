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
DEFAULT_ANIMATION = arrow

class Animate:
    """A decorator class for adding a CLI animation to a slow-running funciton.
    Animate uses introspection to figure out if the function it decorates is
    synchronous (defined with 'def') or asynchronous (defined with 'async def'),
    and works equally well with both.

    The decorator takes a single, optional argument: The animation to be used.
    If no argument is given, the 'arrow' animation is selected by default.
    """

    def __init__(self, *args):
        """Constructor.

        Args:
            *args (tuple): Should consist of a callable and/or a generator
            producing animation steps.
        """
        LOGGER.info("Animate __init__ called with:" + str(args))
        self.args = None
        if len(args) == 1 and callable(args[0]):
            func = args[0]
            self._call = functools.partial(self._call_noargs, func)
            functools.update_wrapper(self, func)
        else:
            self.args = args
            self._call = self._call_args

    async def _async_supervisor(self, func, animation_cycle, *args, **kwargs):
        """Supervisor for running an animation with an asynchronous function.

        Args:
            func (function): A function to be run alongside an animation.
            animation_cycle (generator): An infinite generator that produces
            strings for the animation.
            *args (tuple): Arguments for self.func.
            **kwargs (dict): Keyword arguments for self.func.
        Returns:
            The result of self.func(*args, **kwargs)
        Raises:
            Any exception that is thrown when executing self.func.
        """
        animation = asyncio.ensure_future(async_animation(
            'ANIMATION', animation_cycle))
        try:
            result = await func(*args, **kwargs)
        except Exception:
            raise
        finally:
            animation.cancel()
        return result

    def _sync_supervisor(self, func, animation_cycle, *args, **kwargs):
        """Supervisor for running an animation with a synchronous function.

        Args:
            func (function): A function to be run alongside an animation.
            animation_cycle (generator): An infinite generator that produces
            strings for the animation.
            *args (tuple): Arguments for self.func.
            **kwargs (dict): Keyword arguments for self.func.
        Returns:
            The result of self.func(*args, **kwargs)
        Raises:
            Any exception that is thrown when executing self.func.
        """
        signal = Signal()
        animation = threading.Thread(target=sync_animation,
                                     args=('ANIMATION', animation_cycle, signal))
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

    def _call_noargs(self, func, *args, **kwargs):
        """The function that __call__ calls if the constructor only received
        a callable (i.e. the decorated function).

        NOTE: This method should ONLY be called directly in the constructor!

        Args:
            func (function): A function to run alongside an animation.
        Returns:
            A function if func is a function, and a coroutine if func is a
            coroutine.
        """
        return self._select_supervisor(func)(DEFAULT_ANIMATION(), *args, **kwargs)

    def _call_args(self, func):
        """The function that __call__ calls when the constructor did not receive
        only a callable (i.e. the decorated function).

        NOTE: This method should ONLY be called directly in the constructor!

        Args:
            func (function): A function to run alongside an animation.
        Returns:
            A function if func is a function, and a coroutine if func is a
            coroutine.
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            animation_cycle = self.args[0]
            return self._select_supervisor(func)(animation_cycle, *args, **kwargs)
        return wrapper

    def __call__(self, *args):
        """Make the class instance callable.
        
        args (tuple): Arguments passed to the constructor of the class.
        """
        LOGGER.info(f'Passing through __call__, calling {self._call}')
        return self._call(*args)
