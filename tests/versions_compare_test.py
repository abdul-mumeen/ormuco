import unittest
from versions.compare_versions import compare_versions, compose_output


class TestVersionsCompare(unittest.TestCase):
    def test_compose_output(self):
        output_one = compose_output('1.1', '1.2', -1)
        self.assertEqual(output_one, '"1.1" is less than "1.2"')

        output_two = compose_output('1.4.1', '1.2.0', 1)
        self.assertEqual(output_two, '"1.4.1" is greater than "1.2.0"')

        output_three = compose_output('1.1.0', '1.1.0', 0)
        self.assertEqual(output_three, '"1.1.0" is equal to "1.1.0"')

    def test_compare_versions_greater_than(self):
        output_one = compare_versions('1.2', '1.1')
        self.assertEqual(output_one, '"1.2" is greater than "1.1"')

        output_two = compare_versions('1.2.1', '1.2')
        self.assertEqual(output_two, '"1.2.1" is greater than "1.2"')

        output_three = compare_versions('2.0', '1.3')
        self.assertEqual(output_three, '"2.0" is greater than "1.3"')

        output_four = compare_versions('2.02.0', '2.1.0')
        self.assertEqual(output_four, '"2.02.0" is greater than "2.1.0"')

        output_five = compare_versions('2.12.0', '2.2.0')
        self.assertEqual(output_five, '"2.12.0" is greater than "2.2.0"')

        output_six = compare_versions('2.1.0.0.0.0.1', '2.1.0')
        self.assertEqual(output_six, '"2.1.0.0.0.0.1" is greater than "2.1.0"')

    def test_compare_versions_less_than(self):
        output_one = compare_versions('1.0', '1.1')
        self.assertEqual(output_one, '"1.0" is less than "1.1"')

        output_two = compare_versions('1.1.1', '1.02')
        self.assertEqual(output_two, '"1.1.1" is less than "1.02"')

        output_three = compare_versions('2.0', '2.3')
        self.assertEqual(output_three, '"2.0" is less than "2.3"')

        output_four = compare_versions('02.02.0', '2.3.0')
        self.assertEqual(output_four, '"02.02.0" is less than "2.3.0"')

        output_five = compare_versions('1.12.0', '2.2.0')
        self.assertEqual(output_five, '"1.12.0" is less than "2.2.0"')

        output_six = compare_versions('2.0.1', '2.0.1.0000.1')
        self.assertEqual(output_six, '"2.0.1" is less than "2.0.1.0000.1"')

    def test_compare_versions_equal_to(self):
        output_one = compare_versions('1.1', '1.1')
        self.assertEqual(output_one, '"1.1" is equal to "1.1"')

        output_two = compare_versions('1.10.1', '1.10.1')
        self.assertEqual(output_two, '"1.10.1" is equal to "1.10.1"')

        output_three = compare_versions('2.1.0', '2.1')
        self.assertEqual(output_three, '"2.1.0" is equal to "2.1"')

        output_four = compare_versions('02.02.0', '2.2.0')
        self.assertEqual(output_four, '"02.02.0" is equal to "2.2.0"')

        output_five = compare_versions('5.02.0.0.0', '5.2')
        self.assertEqual(output_five, '"5.02.0.0.0" is equal to "5.2"')

    def test_compare_versions_invalid_versions(self):
        output_one = compare_versions('1.b.2', '1.1')
        self.assertEqual(output_one, 'Invalid version supplied: 1.b.2')

        output_two = compare_versions('1.10.1', '1.10.cads')
        self.assertEqual(output_two, 'Invalid version supplied: 1.10.cads')

        output_three = compare_versions('2.1.//.4', '2.1')
        self.assertEqual(output_three, 'Invalid version supplied: 2.1.//.4')

        output_four = compare_versions('02.b2.0', '2.2.0')
        self.assertEqual(output_four, 'Invalid version supplied: 02.b2.0')
