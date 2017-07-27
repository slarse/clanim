# -*- coding: utf-8 -*-
"""
.. module:: cli
    :platform: Unix
    :synopsis: This module contains all functions that interact with the CLI.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import sys
import time
import asyncio

def erase(status):
    """Erases the given status message from stdout by backspacing as many times
    as the status is long.

    Args:
        status (str): A status message that is already printed to stdout.
    """
    sys.stdout.write('\x08'*len(status))

def sync_animation(msg, animation_cycle, signal):
    """Print out the animation cycle to stdout. This function is for use with
    synchronous functions and must be run in a thread.

    Args:
        msg (str): A message to display.
        animation_cycle (generator): A generator that produces strings for the
        animation. Should be endless.
        signal (Signal): An object that can be used to signal the thread to
        stop.
    """
    sleep_time = .1
    while not signal.done:
        time.sleep(sleep_time)
        frame = next(animation_cycle)
        status = ''.join(frame) + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        erase(status)
    erase(status)

async def await_sleep_and_continue_unless_cancelled(sleep_time):
    """Await an async sleep and check for a CancelledError.

    Args:
        sleep_time (float): The amount of time to sleep.
    Returns:
        False if a CancelledError is raised during the sleep, else True.
    """
    try:
        await asyncio.sleep(.1)
        return True
    except asyncio.CancelledError:
        return False

async def async_animation(msg, animation_cycle):
    """Print out the animation cycle to stdout. This function is for use with
    asynchronous functions and must be run in an event loop.

    Args:
        msg (str): A message to display.
        animation_cycle (generator): A generator that produces strings for the
        animation. Should be endless.
    """
    sleep_time = .1
    while await await_sleep_and_continue_unless_cancelled(sleep_time):
        frame = next(animation_cycle)
        status = ''.join(frame) + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        erase(status)
    erase(status)
