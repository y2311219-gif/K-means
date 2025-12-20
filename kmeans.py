def k_means(data, k):
    d = (max(data) - min(data)) / k
    centers = [min(data) + (i + 0.5) * d for i in range(k)]
    clusters = [[] for _ in range(k)]
    for point in data:
        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
        clusters[cluster_index].append(point)
    result = [sorted(cluster) for cluster in clusters]
    return result