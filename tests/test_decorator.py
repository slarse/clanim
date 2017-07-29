# -*- coding: utf-8 -*-
# pylint: disable=protected-access
# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=wrong-import-order
"""unit tests for the decorator module.

Author: Simon Larsén
"""
import unittest
from unittest.mock import MagicMock, Mock, patch
from .context import clanim
from clanim.decorator import Animate

def animate_test_variables():
    """Return the variables for the Animate tests."""
    return_value = 42**42
    mock_function = MagicMock(return_value=return_value)
    docstring = 'This is a test docstring'
    mock_function.__doc__ = docstring
    mock_animation = MagicMock()
    step = .1
    msg = 'This is a test message'
    animate = Animate(animation=mock_animation, step=step, msg=msg)
    return mock_function, return_value, docstring, mock_animation, step, msg, animate


class DecoratorTest(unittest.TestCase):

    def test_animate_with_non_callable(self):
        non_callable = 1
        self.assertRaises(TypeError,
                          Animate,
                          func=non_callable)

    @patch('clanim.decorator.get_supervisor', side_effect=lambda func: func)
    def test_animate_with_constructor_kwargs(self, mock_get_supervisor):
        """This test emulates using kwargs in the decorator, so
        that the constructor is actually called on the kwargs, and
        not on the function that Animate decorates.
        """
        mock_function, return_value, docstring, mock_animation, step, msg, animate = (
            animate_test_variables())
        wrapped_function = animate(mock_function)
        result = wrapped_function()
        mock_get_supervisor.assert_called_once_with(mock_function)
        mock_function.assert_called_once_with(mock_animation, step, msg)
        self.assertEqual(docstring, wrapped_function.__doc__)
        self.assertEqual(return_value, result)

    @patch('clanim.decorator.get_supervisor', side_effect=lambda func: func)
    def test_animate_with_constructor_kwargs_and_function_args_and_kwargs(
            self, mock_get_supervisor):
        args = ('herro', 2, lambda x: 2*x)
        kwargs = {'herro': 2, 'python': 42}
        mock_function, return_value, docstring, mock_animation, step, msg, animate = (
            animate_test_variables())
        wrapped_function = animate(mock_function)
        result = wrapped_function(*args, **kwargs)
        mock_get_supervisor.assert_called_once_with(mock_function)
        mock_function.assert_called_once_with(mock_animation, step, msg,
                                              *args, **kwargs)
        self.assertEqual(docstring, wrapped_function.__doc__)
        self.assertEqual(return_value, result)

    @patch('clanim.decorator.get_supervisor', side_effect=lambda func: func)
    def test_animate_without_constructor_kwargs(self, mock_get_supervisor):
        """Emulates decorating a function without calling the constructor explicitly."""
        mock_function, return_value, docstring, _, _, _, _ = (
            animate_test_variables())
        wrapped_function = Animate(mock_function)
        result = wrapped_function()
        mock_get_supervisor.assert_called_once_with(mock_function)
        mock_function.assert_called_once()
        self.assertEqual(docstring, wrapped_function.__doc__)
        self.assertEqual(return_value, result)

    @patch('clanim.decorator.get_supervisor', side_effect=lambda func: func)
    def test_animate_without_constructor_kwargs_with_function_args_and_kwargs(
            self, mock_get_supervisor):
        args = ('herro', 2, lambda x: 2*x)
        kwargs = {'herro': 2, 'python': 42}
        mock_function, return_value, docstring, _, _, _, _ = (
            animate_test_variables())
        wrapped_function = Animate(mock_function)
        result = wrapped_function(*args, **kwargs)
        mock_get_supervisor.assert_called_once_with(mock_function)
        mock_function.assert_called_once()
        self.assertEqual(docstring, wrapped_function.__doc__)
        self.assertEqual(return_value, result)
