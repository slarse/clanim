# -*- coding: utf-8 -*-
# pylint: disable=too-few-public-methods
"""
.. module:: util
    :platform: Unix
    :synopsis: This module contains util functions and classes.
.. moduleauthor:: Simon Larsén <slarse@kth.se>

"""

class Signal:
    """A wrapper for a boolean value used to signal the end of a thread's
    execution."""
    done = False
