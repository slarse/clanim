# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=wrong-import-order
"""unit tests for the big_char module.

Author: Simon Larsén
"""
import unittest
from unittest.mock import MagicMock, Mock, patch
from .context import clanim
from clanim.animation import big_char

class BigCharTest(unittest.TestCase):
    def test_chars_are_correct_size(self):
        for char in big_char.CHARS.values():
            self.assertEqual(big_char.CHAR_HEIGHT, len(char))
            for line in char:
                self.assertEqual(big_char.CHAR_WIDTH, len(line))

