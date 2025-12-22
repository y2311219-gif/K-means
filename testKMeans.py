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
                
    def test_kmeans_outlier(self):
        self.assertEqual(k_means([1, 4, 6, 13], 3), [[1], [4, 6], [13]])
        
    def test_kmeans_multiple_iteration(self):
        self.assertEqual(k_means([1, 6, 10, 11, 12], 3), [[1], [6], [10, 11, 12]])
        
    def test_kmeans_empty_cluster(self):
        self.assertEqual(k_means([10, 10], 2), [[10, 10], []])
        
    def test_k_must_be_positive(self):
        params = [-1, 0]
        for k in params:
            with self.subTest(k=k):
                with self.assertRaisesRegex(ValueError, "k must be positive"):
                    k_means([1, 2, 3], k)

    def test_k_must_be_integer(self):
        params = ["1", 0.5, [1, 2]]
        for k in params:
            with self.subTest(k=k):
                with self.assertRaisesRegex(TypeError, "k must be integer"):
                    k_means([1, 2, 3], k)
    
    def test_k_is_one(self):
        self.assertEqual(k_means([1, 2, 3], 1), [[1, 2, 3]])
                    
    def test_data_must_be_numeric_list(self):
        params = [
            [1, 2, "a"],
            [1, [2, 3], 4]
        ]
        for data in params:
            with self.subTest(data=data):
                with self.assertRaisesRegex(TypeError, "data must be numeric list"):
                    k_means(data, 3)

if __name__ == "__main__":
    unittest.main()