# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=wrong-import-order
"""unit tests for the alnum module.

Author: Simon Larsén
"""
import unittest
from .context import clanim
from clanim import alnum

class AlnumTest(unittest.TestCase):

    def test_big_message_when_msg_length_equal_to_width(self):
        msg = 'Hi'
        width = 12
        msg_gen = alnum.big_message(msg, width)
        expected_frames = [["           X",
                            "           X",
                            "           X",
                            "           X",
                            "           X"],
                           ["          X ",
                            "          X ",
                            "          XX",
                            "          X ",
                            "          X "],

                           ["         X  ",
                            "         X  ",
                            "         XXX",
                            "         X  ",
                            "         X  "],

                           ["        X   ",
                            "        X   ",
                            "        XXXX",
                            "        X   ",
                            "        X   "],

                           ["       X   X",
                            "       X   X",
                            "       XXXXX",
                            "       X   X",
                            "       X   X"],

                           ["      X   X ",
                            "      X   X ",
                            "      XXXXX ",
                            "      X   X ",
                            "      X   X "],

                           ["     X   X  ",
                            "     X   X  ",
                            "     XXXXX  ",
                            "     X   X  ",
                            "     X   X  "],

                           ["    X   X  X",
                            "    X   X   ",
                            "    XXXXX   ",
                            "    X   X   ",
                            "    X   X  X"],

                           ["   X   X  XX",
                            "   X   X    ",
                            "   XXXXX    ",
                            "   X   X    ",
                            "   X   X  XX"],

                           ["  X   X  XXX",
                            "  X   X    X",
                            "  XXXXX    X",
                            "  X   X    X",
                            "  X   X  XXX"],

                           [" X   X  XXXX",
                            " X   X    X ",
                            " XXXXX    X ",
                            " X   X    X ",
                            " X   X  XXXX"],

                           ["X   X  XXXXX",
                            "X   X    X  ",
                            "XXXXX    X  ",
                            "X   X    X  ",
                            "X   X  XXXXX"],

                           ["   X  XXXXX ",
                            "   X    X   ",
                            "XXXX    X   ",
                            "   X    X   ",
                            "   X  XXXXX "],

                           ["  X  XXXXX  ",
                            "  X    X    ",
                            "XXX    X    ",
                            "  X    X    ",
                            "  X  XXXXX  "],

                           [" X  XXXXX   ",
                            " X    X     ",
                            "XX    X     ",
                            " X    X     ",
                            " X  XXXXX   "],

                           ["X  XXXXX    ",
                            "X    X      ",
                            "X    X      ",
                            "X    X      ",
                            "X  XXXXX    "],

                           ["  XXXXX     ",
                            "    X       ",
                            "    X       ",
                            "    X       ",
                            "  XXXXX     "],

                           [" XXXXX      ",
                            "   X        ",
                            "   X        ",
                            "   X        ",
                            " XXXXX      "],

                           ["XXXXX       ",
                            "  X         ",
                            "  X         ",
                            "  X         ",
                            "XXXXX       "],

                           ["XXXX        ",
                            " X          ",
                            " X          ",
                            " X          ",
                            "XXXX        "],

                           ["XXX         ",
                            "X           ",
                            "X           ",
                            "X           ",
                            "XXX         "],

                           ["XX          ",
                            "            ",
                            "            ",
                            "            ",
                            "XX          "],

                           ["X           ",
                            "            ",
                            "            ",
                            "            ",
                            "X           "],

                           ["            ",
                            "            ",
                            "            ",
                            "            ",
                            "            "]]
        expected_frames = ['\n'.join(frame) for frame in expected_frames]
        for expected_frame in expected_frames:
            self.assertEqual(expected_frame, next(msg_gen))
        self.assertRaises(StopIteration, msg_gen.__next__)
