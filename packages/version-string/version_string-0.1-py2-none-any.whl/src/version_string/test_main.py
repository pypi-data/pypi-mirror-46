import unittest
import main


class TestVersion(unittest.TestCase):
    # Greater test
    def test_main_great(self):
        result = main.version_compare('1.3', '1.1')
        self.assertEqual(result, '1.3 Version is greater than Version 1.1')
        result = main.version_compare('2.1', '-1.3')
        # import pdb
        # pdb.set_trace()
        self.assertEqual(result, '2.1 Version is greater than Version -1.3')
        result = main.version_compare('1.1', '0')
        self.assertEqual(result, '1.1 Version is greater than Version 0')

    # Equal test
    def test_main_equal(self):
        result = main.version_compare('1.1', '1.1')
        self.assertEqual(result, '1.1 Version is equal to Version 1.1')
        result = main.version_compare('-21.1', '-21.1')
        self.assertEqual(result, '-21.1 Version is equal to Version -21.1')
        result = main.version_compare('0', '0')
        self.assertEqual(result, '0 Version is equal to Version 0')

    # Less test
    def test_main_less(self):
        result = main.version_compare('0.1', '1.1')
        self.assertEqual(result, '0.1 Version is lesser than Version 1.1')
        result = main.version_compare('-112.1', '-21.1')
        self.assertEqual(result, '-112.1 Version is lesser than Version -21.1')
        result = main.version_compare('-12.1', '1.1')
        self.assertEqual(result, '-12.1 Version is lesser than Version 1.1')


if __name__ == 'main':
    unittest.main()
