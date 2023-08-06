from unittest import TestCase

from qbo import utils


class TestUtils(TestCase):
    def test_valid(self):
        parsed = utils.parse_int("12345")
        assert parsed == 12345

    def test_invalid(self):
        parsed = utils.parse_int("test")
        assert parsed is None

    def test_invalid_with_default(self):
        parsed = utils.parse_int("test", 42)
        assert parsed is 42
