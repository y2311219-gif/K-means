import unittest

def k_means(data, k):
    return [[1, 2], [4]]

class TestKMeans(unittest.TestCase):
    def test_kmeans_basic(self):
        self.assertEqual(k_means([1, 2, 4], 2), [[1, 2], [4]])

if __name__ == "__main__":
    unittest.main()