"""Unit tests for the cli module.

Author: Simon Larsén
"""
import asyncio
import asynctest
import itertools
import threading
import unittest
from unittest.mock import patch
from .context import clanim
from clanim import cli
from clanim import util

class CliTest(asynctest.TestCase):

    @asynctest.patch('asyncio.sleep', side_effect=asyncio.CancelledError)
    async def test_cancel_async_guard(self, mock_sleep):
        check = await cli.await_sleep_and_continue_unless_cancelled(.1)
        self.assertFalse(check)

    async def test_async_guard(self):
        test_loops = 50
        for _ in range(test_loops):
            check = await cli.await_sleep_and_continue_unless_cancelled(.0000001)
            self.assertTrue(check)
