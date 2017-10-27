# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""
.. module:: util
    :platform: Unix
    :synopsis: This module contains util functions and classes.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import asyncio
import time
import functools
import itertools
import threading
import logging
import daiquiri
from .cli import animate_cli, BACKSPACE

daiquiri.setup(level=logging.ERROR)
LOGGER = daiquiri.getLogger(__name__)

BACKSPACE_GEN = lambda size: itertools.cycle([BACKSPACE*size])
BACKLINE_GEN = lambda lines: itertools.cycle(['\033[F'*(lines-1)])

class Signal:
    """A wrapper for a boolean value used to signal the end of a thread's
    execution. This is not thread-safe, so it should not be used in contexts
    where precision matters.
    """
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

async def _async_supervisor(func, animation_, step, *args, **kwargs):
    """Supervisor for running an animation with an asynchronous function.

    Args:
        func (function): A function to be run alongside an animation.
        animation_ (generator): An infinite generator that produces
        strings for the animation.
        step (float): Seconds between each animation frame.
        *args (tuple): Arguments for func.
        **kwargs (dict): Keyword arguments for func.
    Returns:
        The result of func(*args, **kwargs)
    Raises:
        Any exception that is thrown when executing func.
    """
    signal = Signal()
    loop = asyncio.get_event_loop()
    anim = threading.Thread(target=animate_cli,
                            args=(animation_, step, signal))
    monitor = threading.Thread(target=_unexpected_loop_exit_monitor,
                               args=(signal, loop))
    anim.start()
    monitor.start()
    try:
        result = await func(*args, **kwargs)
    except:
        raise
    finally:
        signal.done = True
        anim.join()
        monitor.join()
    return result

def _unexpected_loop_exit_monitor(signal, loop):
    """Monitors the asyncio loop and the signal. Terminates if the signal is done,
    and also if the loop closes prematurely.

    Args:
        signal (Signal): A Signal.
        loop (asyncio.BaseEventLoop): An asyncio loop.
    """
    while not signal.done:
        time.sleep(.1)
        if loop.is_closed():
            # loop was shut down unexpectedly
            signal.done = True

def _sync_supervisor(func, animation_, step, *args, **kwargs):
    """Supervisor for running an animation with a synchronous function.

    Args:
        func (function): A function to be run alongside an animation.
        animation_ (generator): An infinite generator that produces
        strings for the animation.
        step (float): Seconds between each animation frame.
        args (tuple): Arguments for func.
        kwargs (dict): Keyword arguments for func.
    Returns:
        The result of func(*args, **kwargs)
    Raises:
        Any exception that is thrown when executing func.
    """
    signal = Signal()
    animation = threading.Thread(target=animate_cli,
                                 args=(animation_, step, signal))
    animation.start()
    try:
        result = func(*args, **kwargs)
    except Exception:
        raise
    finally:
        signal.done = True
        animation.join()
    return result

def concatechain(*generators, separator=''):
    """Create generator that in each iteration takes one value from each of the
    supplied generators, adds them togeter in-place (so the values yielded must
    suport __iadd__) and yields the result. Stops as soon as any iterator
    raises StopIteration and returns the value contained in it.

    Primarily created for concatenating strings, hence the name.

    Args:
        generators (List[generator]): A list
        separator (str): A separator to insert between each value yielded by
        the different generators.
    Returns:
        A generator as described above.
    """
    while True:
        try:
            next_ = []
            for gen in generators:
                next_.append(next(gen))
            yield separator.join(next_)
        except StopIteration as e:
            return e.value
