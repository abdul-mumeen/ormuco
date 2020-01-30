import unittest
from overlap.overlap import get_max, get_min, extract_values, check_line_overlap


class TestLineOverlap(unittest.TestCase):
    def test_get_max_with_negative_numbers(self):
        result_one = get_max(-5, 0)
        self.assertEqual(result_one, 0)

        result_two = get_max(-2, -10)
        self.assertEqual(result_two, -2)

    def test_get_max_with_positive_numbers(self):
        result_one = get_max(5, 10)
        self.assertEqual(result_one, 10)

        result_two = get_max(200, 32)
        self.assertEqual(result_two, 200)

    def test_get_max_with_positive_and_negative_numbers(self):
        result_one = get_max(-5, 10)
        self.assertEqual(result_one, 10)

        result_two = get_max(20, -1)
        self.assertEqual(result_two, 20)

    def test_get_min_with_negative_numbers(self):
        result_one = get_min(-5, 0)
        self.assertEqual(result_one, -5)

        result_two = get_min(-2, -10)
        self.assertEqual(result_two, -10)

    def test_get_min_with_positive_numbers(self):
        result_one = get_min(5, 10)
        self.assertEqual(result_one, 5)

        result_two = get_min(200, 32)
        self.assertEqual(result_two, 32)

    def test_get_min_with_positive_and_negative_numbers(self):
        result_one = get_min(-5, 10)
        self.assertEqual(result_one, -5)

        result_two = get_min(20, -1)
        self.assertEqual(result_two, -1)

    def test_extract_values(self):
        value_one, value_two = extract_values('-5 0')
        self.assertEqual(value_one, -5)
        self.assertEqual(value_two, 0)

        value_one, value_two = extract_values('100 3')
        self.assertEqual(value_one, 100)
        self.assertEqual(value_two, 3)

        value_one, value_two = extract_values('0 55')
        self.assertEqual(value_one, 0)
        self.assertEqual(value_two, 55)

        value_one, value_two = extract_values('-20 -15')
        self.assertEqual(value_one, -20)
        self.assertEqual(value_two, -15)

    def test_check_line_overlap_with_positive_numbers(self):
        result_one = check_line_overlap((5, 10), (3, 11))
        self.assertEqual(result_one, True)

        result_two = check_line_overlap((1, 10), (25, 10))
        self.assertEqual(result_two, False)

        result_three = check_line_overlap((1, 10), (25, 9))
        self.assertEqual(result_three, True)

    def test_check_line_overlap_with_negative_numbers(self):
        result_one = check_line_overlap((-5, -15), (-2, -7))
        self.assertEqual(result_one, True)

        result_two = check_line_overlap((-15, -3), (-2, -1))
        self.assertEqual(result_two, False)

        result_three = check_line_overlap((-15, -3), (-4, -1))
        self.assertEqual(result_three, True)

    def test_check_line_overlap_with_mixed_numbers(self):
        result_one = check_line_overlap((-5, 1), (7, -2))
        self.assertEqual(result_one, True)

        result_two = check_line_overlap((-15, 5), (25, 6))
        self.assertEqual(result_two, False)

        result_three = check_line_overlap((-15, 0), (54, -1))
        self.assertEqual(result_three, True)