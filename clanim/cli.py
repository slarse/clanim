# -*- coding: utf-8 -*-
"""
.. module:: cli
    :platform: Unix
    :synopsis: This module contains all functions that interact with the CLI.
.. moduleauthor:: Simon Larsén <slarse@kth.se>
"""
import sys
import time

def erase(status):
    """Erases the given status message from stdout by backspacing as many times
    as the status is long.

    Args:
        status (str): A status message that is already printed to stdout.
    """
    sys.stdout.write('\x08'*len(status))

def animate_cli(animation_cycle, step, msg, signal):
    """Print out the animation cycle to stdout. This function is for use with
    synchronous functions and must be run in a thread.

    Args:
        animation_cycle (generator): A generator that produces strings for the
        animation. Should be endless.
        step (float): Seconds between each animation frame.
        msg (str): A message to display.
        signal (Signal): An object that can be used to signal the thread to
        stop.
    """
    while not signal.done:
        time.sleep(step)
        frame = next(animation_cycle)
        status = ''.join(frame) + ' ' + msg
        sys.stdout.write(status)
        sys.stdout.flush()
        erase(status)
    erase(status)
