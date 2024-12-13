import unittest
from unittest.mock import patch

from main import options, get_int


# Test for get_int function (as you provided)
def test_get_int():
    with patch('builtins.input', return_value='3'):
        result = get_int("3")
        self.assertEqual(result, 3)