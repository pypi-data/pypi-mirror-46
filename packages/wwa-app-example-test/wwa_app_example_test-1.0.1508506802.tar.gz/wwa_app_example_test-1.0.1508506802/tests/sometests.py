import unittest

from wwa_app_example import main

class TestClass(unittest.TestCase):
    def test_num1(self):
        self.assertEqual(main.test(1), 2)

    # This should fail
    def test_num1(self):
        self.assertEqual(main.test(-1), 2)
