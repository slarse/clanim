# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=wrong-import-order
"""unit tests for the animation module.

author: simon larsén
"""
import unittest
from .context import clanim
from clanim.animation import animation
from clanim.animation import singleline
from clanim.animation import multiline

class AnimationTest(unittest.TestCase):

    def test_raise_value_error_if_width_is_too_small(self):
        values = [-100, -2, 0, 1]
        for val in values:
            self.assertRaises(
                ValueError,
                animation._raise_value_error_if_width_is_too_small,
                val)

    def test_dont_raise_value_error_if_width_is_good(self):
        values = [2, 45, 110]
        for val in values:
            animation._raise_value_error_if_width_is_too_small(val)

    def test_char_wave_raises_with_too_small_width(self):
        values = [-100, -2, 0, 1]
        for val in values:
            with self.assertRaises(ValueError):
                next(singleline.char_wave(width=val))

    def test_char_wave_raises_with_empty_string(self):
        with self.assertRaises(ValueError):
            next(singleline.char_wave(char=''))

    def test_char_wave_raises_for_multiple_chars(self):
        with self.assertRaises(ValueError):
            next(singleline.char_wave(char='##'))

    def test_char_wave_with_adequate_width(self):
        width = 3
        char = '#'
        expected_sequence = ['#  ', '## ', '###', '## ', '#  ']
        for i in range(0, len(expected_sequence)):
            expected_sequence[i] =  expected_sequence[i] + '\x08'*width
        for expected, actual in zip(
                expected_sequence, singleline.char_wave(width=width)):
            self.assertEqual(expected, actual)

    def test_arrow_raises_with_too_small_width(self):
        values = [-100, -2, 0, 1]
        for val in values:
            with self.assertRaises(ValueError):
                gen = singleline.arrow(width=val)
                next(gen)

    def test_arrow_with_adequate_width(self):
        width = 3
        expected_sequence = ['>  ', ' > ', '  <', ' < ', '>  ']
        for i in range(0, len(expected_sequence)):
            expected_sequence[i] =  expected_sequence[i] + '\x08'*width
        for expected, actual in zip(
                expected_sequence, singleline.arrow(width=width)):
            self.assertEqual(expected, actual)
