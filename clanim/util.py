# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""
.. module:: util
    :platform: Unix
    :synopsis: This module contains util functions and classes.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import asyncio
import functools
import threading
from .cli import animate_cli

class Signal:
    """A wrapper for a boolean value used to signal the end of a thread's
    execution."""
    done = False

def get_supervisor(func):
    """Get the appropriate supervisor to use and pre-apply the function.

    Args:
        func (function): A function.
    """
    if asyncio.iscoroutinefunction(func):
        supervisor = _async_supervisor
    else:
        supervisor = _sync_supervisor
    return functools.partial(supervisor, func)

async def _async_supervisor(func, animation_, step, msg, *args, **kwargs):
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
    signal = Signal()
    animation = threading.Thread(target=animate_cli,
                                 args=(animation_, step, msg, signal))
    animation.start()
    try:
        result = await func(*args, **kwargs)
    except Exception:
        raise
    finally:
        signal.done = True
        animation.join()
    return result

def _sync_supervisor(func, animation_, step, msg, *args, **kwargs):
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
    animation = threading.Thread(target=animate_cli,
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
