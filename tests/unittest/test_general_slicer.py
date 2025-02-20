import unittest
from utils.general_slicer import SliceContext, slice_data, SliceManipulator
import numpy as np

class TestSimpleSlicer(unittest.TestCase):
    def setUp(self):
        self.slice_size = 3
        self.slice_axis = 0
        self.context = SliceContext.create_numpy_slice_context(self.slice_size, self.slice_axis)

    def test_slice_data_no_remainder(self):
        data = np.array([1, 2, 3, 4, 5, 6])
        expected_output = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        result = list(slice_data(self.context, data))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_with_remainder(self):
        data = np.array([1, 2, 3, 4, 5])
        expected_output = [np.array([1, 2, 3])]
        result = list(slice_data(self.context, data))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_with_initial_remainder(self):
        self.context.last_remainder = np.array([1, 2])
        data = np.array([3, 4, 5, 6, 7])
        expected_output = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        result = list(slice_data(self.context, data))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_empty_data(self):
        data = np.array([])
        expected_output = []
        self.assertEqual(list(slice_data(self.context, data)), expected_output)

    def test_slice_data_single_element_data(self):
        data = np.array([1])
        self.assertEqual(len(list(slice_data(self.context, data))), 0)
        self.assertEqual(self.context.last_remainder, data)

    def test_slice_data_multidimensional(self):
        data = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
        expected_output = [np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])]
        result = list(slice_data(self.context, data))
        self.assertEqual(len(result), len(expected_output))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_initial_remainder_empty(self):
        self.context.last_remainder = np.array([])
        data = np.array([1, 2, 3, 4, 5])
        expected_output = [np.array([1, 2, 3])]
        result = list(slice_data(self.context, data))
        self.assertEqual(len(result), len(expected_output))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_initial_remainder_single_element(self):
        self.context.last_remainder = np.array([1])
        data = np.array([2, 3, 4, 5, 6])
        expected_output = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        result = list(slice_data(self.context, data))
        self.assertEqual(len(result), len(expected_output))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_initial_remainder_exceeds_slice_size(self):
        self.context.last_remainder = np.array([1, 2, 3, 4])
        data = np.array([5, 6, 7, 8, 9])
        expected_output = [np.array([1, 2, 3]), np.array([4, 5, 6]), np.array([7, 8, 9])]
        result = list(slice_data(self.context, data))
        self.assertEqual(len(result), len(expected_output))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))

    def test_slice_data_initial_remainder_multidimensional(self):
        self.context.last_remainder = np.array([[1, 2, 3]])
        data = np.array([[4, 5, 6], [7, 8, 9], [10, 11, 12]])
        expected_output = [np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])]
        result = list(slice_data(self.context, data))
        self.assertEqual(len(result), len(expected_output))
        self.assertTrue(all(np.array_equal(a, b) for a, b in zip(result, expected_output)))


class TestStringSlicer(unittest.TestCase):
    def setUp(self):
        self.slice_size = 3
        self.slice_axis = 0
        self.context = SliceContext(
            slice_size=self.slice_size,
            data_manipulator=SliceManipulator(
                size_func=lambda x: len(x),
                slice_func=lambda x, start, end: x[start:end],
                concat_func=lambda x: ''.join(x)
            )
        )

    def test_slice_string_no_remainder(self):
        data = "abcdef"
        expected_output = ["abc", "def"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

    def test_slice_string_with_remainder(self):
        data = "abcde"
        expected_output = ["abc"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

    def test_slice_string_with_initial_remainder(self):
        self.context.last_remainder = "ab"
        data = "cdefg"
        expected_output = ["abc", "def"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

    def test_slice_string_empty_data(self):
        data = ""
        expected_output = []
        self.assertEqual(list(slice_data(self.context, data)), expected_output)

    def test_slice_string_single_element_data(self):
        data = "a"
        self.assertEqual(len(list(slice_data(self.context, data))), 0)
        self.assertEqual(self.context.last_remainder, data)

    def test_slice_string_initial_remainder_empty(self):
        self.context.last_remainder = ""
        data = "abcde"
        expected_output = ["abc"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

    def test_slice_string_initial_remainder_single_element(self):
        self.context.last_remainder = "a"
        data = "bcdef"
        expected_output = ["abc", "def"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

    def test_slice_string_initial_remainder_exceeds_slice_size(self):
        self.context.last_remainder = "abcd"
        data = "efghi"
        expected_output = ["abc", "def", "ghi"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

    def test_slice_string_modify_slice_size(self):
        data = "abcdefghij"
        expected_output = ["abc", "def", "ghi"]
        self.context.slice_size = 3
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

        # 修改 slice_size 为 2
        self.context.slice_size = 2
        expected_output = ["ja", "bc", "de", "fg", "hi"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

        # 修改 slice_size 为 4
        self.context.slice_size = 4
        expected_output = ["jabc", "defg"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)

        # 修改 slice_size 为 16
        self.context.slice_size = 16
        expected_output = []
        expected_remainder = "hijabcdefghij"
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)
        self.assertEqual(self.context.last_remainder, expected_remainder)

        # 修改 slice_size 为 4
        self.context.slice_size = 4
        expected_output = ["hija", "bcde", "fghi", "jabc", "defg"]
        result = list(slice_data(self.context, data))
        self.assertEqual(result, expected_output)


if __name__ == '__main__':
    unittest.main()
