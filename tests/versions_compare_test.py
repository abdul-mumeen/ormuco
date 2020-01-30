import unittest
from versions.compare_versions import compare_versions


class TestVersionsCompare(unittest.TestCase):
    def test_compose_output(self):
        # result_one = compare_versions('1.1', '1.2')
        # self.assertEqual(result_one, '"1.1" is less than "1.2"')