# -*- coding: utf-8 -*-
"""
.. module: animation
    :platform: Unix
    :synopsis: Animation decorators.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import asyncio
import sys
import functools
import itertools
import threading
import inspect
import time
import daiquiri
import logging

daiquiri.setup(level=logging.INFO)
LOGGER = daiquiri.getLogger(__name__)

erase = lambda s: sys.stdout.write('\x08'*len(s))

class Signal:
    done = False

def char_wave(char='#', size=10):
    increasing = ((char*n).ljust(size) for n in range(1, size))
    decreasing = ((char*n).ljust(size) for n in range(size, 1, -1))
    wave = itertools.chain(increasing, decreasing)
    return itertools.cycle(wave)

class animate_class:
    def __init__(self, *args):
        LOGGER.info(args)
        if len(args) == 1 and callable(args[0]):
            self.func = args[0]
            self._call = self._call_noargs
            functools.update_wrapper(self, self.func)
        else:
            self.args = args
            self._call = self._call_args


    async def _async_wrapper(self, animation_cycle, *args, **kwargs):
        animation = asyncio.ensure_future(async_animation(
            'ANIMATION', animation_cycle))
        result = await self.func(*args, **kwargs)
        animation.cancel()
        return result

    def _sync_wrapper(self, animation_cycle, *args, **kwargs):
        signal = Signal()
        animation = threading.Thread(target=sync_animation,
                                     args=('ANIMATION', animation_cycle, signal))
        animation.start()
        result = self.func(*args, **kwargs)
        signal.done = True
        animation.join()
        return result

    def _call_args(self, func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            self.func = func
            animation_cycle = self.args[0]
            if inspect.iscoroutinefunction(self.func):
                return self._async_wrapper(animation_cycle, *args, **kwargs)
            else:
                return self._sync_wrapper(animation_cycle, *args, **kwargs)
        return wrapper


    def _call_noargs(self, *args, **kwargs):
        if inspect.iscoroutinefunction(self.func):
            return self._async_wrapper(arrow(), *args, **kwargs)
        else:
            return self._sync_wrapper(arrow(), *args, **kwargs)

    def __call__(self, *args):
        LOGGER.info(f'Passing through __call__, calling {self._call}')
        return self._call(*args)


def animate(func):
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        animation = asyncio.ensure_future(async_animation(
            'ANIMATION', arrow()))
        result = await func(*args, **kwargs)
        animation.cancel()
        return result
    def sync_wrapper(*args, **kwargs):
        signal = Signal()
        animation = threading.Thread(target=sync_animation,
                                     args=('ANIMATION', arrow(), signal))
        animation.start()
        result = func(*args, **kwargs)
        signal.done = True
        animation.join()
        return result
    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper

    return async_wrapper

def sync_animation(msg, animation_cycle, signal):
    status = ''
    while sync_loop_guard(signal):
        frame = next(animation_cycle)
        status = ''.join(frame) + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        erase(status)
    erase(status)

def sync_loop_guard(signal):
    time.sleep(.1)
    return not signal.done

async def async_loop_guard():
    try:
        await asyncio.sleep(.1)
        return True
    except asyncio.CancelledError:
        return False


def arrow():
    right_arrows = reversed(sorted(set(itertools.permutations('>' + ' '*4))))
    left_arrows = sorted(set(itertools.permutations('<' + ' '*4)))
    return itertools.cycle(itertools.chain(right_arrows, left_arrows))


async def async_animation(msg, animation_cycle):
    while await async_loop_guard():
        frame = next(animation_cycle)
        status = ''.join(frame) + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        erase(status)
    erase(status)

    

async def working_animation(msg, loop_guard):
    """cli.status_callback an animation to stdout.

    Args:
        msg (str): A message to come after the animation.
    """
    write, flush = sys.stdout.write, sys.stdout.flush
    erase = lambda s: write('\x08'*len(s))
    right_arrows = reversed(sorted(set(itertools.permutations('>' + ' '*4))))
    left_arrows = sorted(set(itertools.permutations('<' + ' '*4)))
    arrow_bars = itertools.cycle(itertools.chain(right_arrows, left_arrows))
    while await loop_guard():
        arrow_bar = next(arrow_bars)
        status = ''.join(arrow_bar) + ' ' + msg
        write(status)
        flush()
        erase(status)
    erase(status)


async def supervisor(work_func, animation_func):
    """Show the animation on standard out while the async function runs.

    Args:
        work_func (asyncio.coroutine): Any asynchronous function.
        animation_func (asyncio.coroutine): An asynchronous function that cli.status_callbacks an animation
        to stdout.
    """
    animation = asyncio.ensure_future(animation_func())
    await work_func()
    animation.cancel()
