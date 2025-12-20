import unittest

def k_means(data, k):
    d = (data[-1] - data[0]) / k
    centers = [data[0] + (i + 0.5) * d for i in range(k)]
    clusters = [[] for _ in range(k)]
    for point in data:
        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
        clusters[cluster_index].append(point)
    return clusters

class TestKMeans(unittest.TestCase):
    def test_kmeans_basic(self):
        params = [
            ([1, 2, 4], 2, [[1, 2], [4]]),
            ([1, 5, 6, 10], 3, [[1], [5, 6], [10]])
        ]
        for data, k, expected in params:
            with self.subTest(data=data, k=k, expected=expected):
                self.assertEqual(k_means(data, k), expected)

if __name__ == "__main__":
    unittest.main()