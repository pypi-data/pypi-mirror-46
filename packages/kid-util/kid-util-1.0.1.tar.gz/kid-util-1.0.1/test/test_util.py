import unittest
from kid import util


class TestKid(unittest.TestCase):

    def test_mod10(self):
        self.assertEqual('2345676', util.make_mod10('234567'))

    def test_mod10_control_digit(self):
        self.assertEqual(6, util.make_mod10_control_digit('234567'))

    def test_mod10_0(self):
        self.assertEqual('00', util.make_mod10('0'))

    def test_mod10_error(self):
        with self.assertRaises(ValueError):
            util.make_mod10('abc')

    def test_mod10_error_len(self):
        with self.assertRaises(ValueError):
            util.make_mod10('')

    def test_mod10_error_len2(self):
        with self.assertRaises(ValueError):
            util.make_mod10('01234567890123456789012345')

    def test_mod11(self):
        self.assertEqual('12345678903', util.make_mod11('1234567890'))

    def test_mod11_control_digit(self):
        self.assertEqual(3, util.make_mod11_control_digit('1234567890'))

    def test_mod11_0(self):
        self.assertEqual('310', util.make_mod11('31'))

    def test_mod11_dash(self):
        self.assertEqual('40-', util.make_mod11('40'))

    def test_mod11_error(self):
        with self.assertRaises(ValueError):
            util.make_mod10('abc')

    def test_mod11_error_len(self):
        with self.assertRaises(ValueError):
            util.make_mod11('')

    def test_mod11_error_len2(self):
        with self.assertRaises(ValueError):
            util.make_mod11('01234567890123456789012345')


if __name__ == '__main__':
    unittest.main()
