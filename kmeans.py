def k_means(data, k):
    if not all(isinstance(x, (int, float)) for x in data):
        raise TypeError("data must be numeric list")
    if not isinstance(k, int):
        raise TypeError("k must be integer")
    if k <= 0:
        raise ValueError("k must be positive")
    if k > len(data):
        raise ValueError("k must not be larger than data size")
    
    if k == 1:
        return [sorted(data)]
    
    centers = _init_centers(data, k)
    
    old_clusters = [[] for _ in range(k)]
    while True:
        clusters = _form_clusters(data, k, centers)
        if(clusters == old_clusters):
            break

        centers = _update_centers(centers, clusters)
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

def _update_centers(centers, clusters):
    new_centers = []
    for current_center, cluster in zip(centers, clusters):
        if cluster != []:
            new_centers.append(sum(cluster) / len(cluster))
        else:
            new_centers.append(current_center)
    return new_centers
