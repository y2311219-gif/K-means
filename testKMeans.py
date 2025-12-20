import unittest
from kmeans import k_means

class TestKMeans(unittest.TestCase):
    def test_kmeans_basic(self):
        params = [
            ([1, 2, 4], 2, [[1, 2], [4]]),
            ([1, 5, 6, 10], 3, [[1], [5, 6], [10]])
        ]
        for data, k, expected in params:
            with self.subTest(data=data, k=k, expected=expected):
                self.assertEqual(k_means(data, k), expected)
                
    def test_kmeans_unsorted(self):
        params = [
            ([2, 1, 4], 2, [[1, 2], [4]]),
            ([10, 5, 6, 1], 3, [[1], [5, 6], [10]])
        ]
        for data, k, expected in params:
            with self.subTest(data=data, k=k, expected=expected):
                self.assertEqual(k_means(data, k), expected)

if __name__ == "__main__":
    unittest.main()