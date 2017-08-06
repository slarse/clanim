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
from clanim import animation

class AnimationTest(unittest.TestCase):

    def test_raise_value_error_if_size_is_too_small(self):
        values = [-100, -2, 0, 1]
        for val in values:
            self.assertRaises(
                ValueError,
                animation.raise_value_error_if_size_is_too_small,
                val)

    def test_dont_raise_value_error_if_size_is_good(self):
        values = [2, 45, 110]
        for val in values:
            animation.raise_value_error_if_size_is_too_small(val)

    def test_char_wave_raises_with_too_small_size(self):
        values = [-100, -2, 0, 1]
        for val in values:
            with self.assertRaises(ValueError):
                next(animation.char_wave(size=val))

    def test_char_wave_raises_with_empty_string(self):
        with self.assertRaises(ValueError):
            next(animation.char_wave(char=''))

    def test_char_wave_raises_for_multiple_chars(self):
        with self.assertRaises(ValueError):
            next(animation.char_wave(char='##'))

    def test_char_wave_with_adequate_size(self):
        size = 3
        char = '#'
        expected_sequence = ['#  ', '## ', '###', '## ', '#  ']
        for i in range(1, len(expected_sequence)):
            expected_sequence[i] = '\x08'*size + expected_sequence[i]
        for expected, actual in zip(
                expected_sequence, animation.char_wave(size=size)):
            self.assertEqual(expected, actual)

    def test_arrow_raises_with_too_small_size(self):
        values = [-100, -2, 0, 1]
        for val in values:
            with self.assertRaises(ValueError):
                gen = animation.arrow(size=val)
                next(gen)

    def test_arrow_with_adequate_size(self):
        size = 3
        expected_sequence = ['>  ', ' > ', '  <', ' < ', '>  ']
        for i in range(1, len(expected_sequence)):
            expected_sequence[i] = '\x08'*size + expected_sequence[i]
        for expected, actual in zip(
                expected_sequence, animation.arrow(size=size)):
            self.assertEqual(expected, actual)
