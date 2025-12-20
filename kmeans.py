def k_means(data, k):
    d = (data[-1] - data[0]) / k
    centers = [data[0] + (i + 0.5) * d for i in range(k)]
    clusters = [[] for _ in range(k)]
    for point in data:
        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
        clusters[cluster_index].append(point)
    return clusters