def k_means(data, k):
    centers = _init_centers(data, k)
    
    old_clusters = [[] for _ in range(k)]
    while True:
        clusters = _form_clusters(data, k, centers)
        if(clusters == old_clusters):
            break

        for i in range(k):
            centers[i] = sum(clusters[i]) / len(clusters[i])
        old_clusters = clusters

    result = [sorted(cluster) for cluster in clusters]
    return result

def _init_centers(data, k):
    sorted_data = sorted(data)
    d = (len(data) - 1) / (k - 1)
    centers = [sorted_data[int(d * i)] for i in range(k)]
    return centers

def _form_clusters(data, k, centers):
    clusters = [[] for _ in range(k)]
    for point in data:
        cluster_index = min(range(k), key=lambda i: abs(point - centers[i]))
        clusters[cluster_index].append(point)
    return clusters