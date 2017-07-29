# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=wrong-import-order
"""Unit tests for the util module.

Author: Simon Larsén
"""
from unittest.mock import Mock
import asynctest
from asynctest import patch as apatch
from .context import clanim
from clanim import util


def supervisor_test_variables(sync=True, raises=False):
    """Initialize the variables used in the supervisor tests.
    
    Args:
        sync (bool): Determines if the mock function should be synchronous or
        an async coroutine.
        raises (bool): Determine if teh mock function should raise an exception
        or not.
    """
    return_value = 42**42
    if sync:
        mock_function = Mock(return_value=return_value)
    else:
        mock_function = asynctest.CoroutineMock(return_value=return_value)
    if raises:
        mock_function.side_effect = Exception
    mock_animation = Mock()
    msg = 'This is a test message'
    step = .1
    signal = util.Signal()
    return mock_function, return_value, mock_animation, msg, step, signal

class UtilTest(asynctest.TestCase):

    async def test_get_supervisor_with_coroutinefunction(self):
        mock_coroutine = asynctest.CoroutineMock()
        supervisor = util.get_supervisor(mock_coroutine)
        self.assertEqual(util._async_supervisor, supervisor.func)
        self.assertEqual(1, len(supervisor.args))
        self.assertEqual(supervisor.args[0], mock_coroutine)

    async def test_get_supervisor_with_regular_function(self):
        func = lambda: None
        supervisor = util.get_supervisor(func)
        self.assertEqual(util._sync_supervisor, supervisor.func)
        self.assertEqual(1, len(supervisor.args))
        self.assertEqual(supervisor.args[0], func)

    async def test_get_supervisor_with_non_callable(self):
        mock_non_callable = asynctest.NonCallableMock()
        self.assertRaises(TypeError, util.get_supervisor(mock_non_callable))

    @apatch('clanim.util.animate_cli')
    async def test_sync_supervisor_with_noargs_function(self, mock_animate_cli):
        mock_function, return_value, mock_animation, msg, step, signal = (
            supervisor_test_variables())
        with apatch('clanim.util.Signal', return_value=signal):
            result = util._sync_supervisor(mock_function, mock_animation, step, msg)
        mock_animate_cli.assert_called_once_with(mock_animation, step, msg, signal)
        mock_function.assert_called_once()
        self.assertEqual(return_value, result)

    @apatch('clanim.util.animate_cli')
    async def test_sync_supervisor_with_args_function(self, mock_animate_cli):
        args = ('herro', 2, lambda: 1)
        mock_function, return_value, mock_animation, msg, step, signal = (
            supervisor_test_variables())
        with apatch('clanim.util.Signal', return_value=signal):
            result = util._sync_supervisor(mock_function, mock_animation, step, msg, *args)
        mock_animate_cli.assert_called_once_with(mock_animation, step, msg, signal)
        mock_function.assert_called_once_with(*args)
        self.assertEqual(return_value, result)

    @apatch('clanim.util.animate_cli')
    async def test_sync_supervisor_with_kwargs_function(self, mock_animate_cli):
        kwargs = {'herro': 2, 'no_way': 'HERRO'}
        mock_function, return_value, mock_animation, msg, step, signal = (
            supervisor_test_variables())
        with apatch('clanim.util.Signal', return_value=signal):
            result = util._sync_supervisor(mock_function, mock_animation, step, msg, **kwargs)
        mock_animate_cli.assert_called_once_with(mock_animation, step, msg, signal)
        mock_function.assert_called_once_with(**kwargs)
        self.assertEqual(return_value, result)

    @apatch('clanim.util.animate_cli')
    async def test_sync_supervisor_with_raising_function(self, mock_animate_cli):
        mock_function, _, mock_animation, msg, step, signal = (
            supervisor_test_variables(raises=True))
        with self.assertRaises(Exception):
            util._sync_supervisor(mock_function, mock_animation, step, msg, signal)

    @apatch('clanim.util.animate_cli')
    async def test_async_supervisor_with_noargs_function(self, mock_animate_cli):
        mock_function, return_value, mock_animation, msg, step, signal = (
            supervisor_test_variables(sync=False))
        with apatch('clanim.util.Signal', return_value=signal):
            result = await util._async_supervisor(mock_function, mock_animation, step, msg)
        mock_animate_cli.assert_called_once_with(mock_animation, step, msg, signal)
        mock_function.assert_called_once()
        self.assertEqual(return_value, result)

    @apatch('clanim.util.animate_cli')
    async def test_async_supervisor_with_args_function(self, mock_animate_cli):
        args = ('herro', 2, lambda: 1)
        mock_function, return_value, mock_animation, msg, step, signal = (
            supervisor_test_variables(sync=False))
        with apatch('clanim.util.Signal', return_value=signal):
            result = await util._async_supervisor(mock_function, mock_animation, step, msg, *args)
        mock_animate_cli.assert_called_once_with(mock_animation, step, msg, signal)
        mock_function.assert_called_once_with(*args)
        self.assertEqual(return_value, result)

    @apatch('clanim.util.animate_cli')
    async def test_async_supervisor_with_kwargs_function(self, mock_animate_cli):
        kwargs = {'herro': 2, 'no_way': 'HERRO'}
        mock_function, return_value, mock_animation, msg, step, signal = (
            supervisor_test_variables(sync=False))
        with apatch('clanim.util.Signal', return_value=signal):
            result = await util._async_supervisor(mock_function, mock_animation, step, msg, **kwargs)
        mock_animate_cli.assert_called_once_with(mock_animation, step, msg, signal)
        mock_function.assert_called_once_with(**kwargs)
        self.assertEqual(return_value, result)

    @apatch('clanim.util.animate_cli')
    async def test_async_supervisor_with_raising_function(self, mock_animate_cli):
        mock_function, _, mock_animation, msg, step, signal = (
            supervisor_test_variables(sync=False, raises=True))
        with self.assertRaises(Exception):
            await util._sync_supervisor(mock_function, mock_animation, step, msg, signal)
