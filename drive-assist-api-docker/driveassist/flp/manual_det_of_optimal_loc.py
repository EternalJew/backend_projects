import numpy as np
import matplotlib.pyplot as plt

# Функція для обчислення евклідової відстані між двома точками
def euclidean_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2) ** 2))

# Функція для ініціалізації початкових центрів кластерів
def initialize_centroids(points, k):
    np.random.seed(42)
    return points[np.random.choice(points.shape[0], k, replace=False)]

# Функція для призначення кожної точки до найближчого кластера
def assign_clusters(points, centroids):
    clusters = []
    for point in points:
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        cluster = np.argmin(distances)
        clusters.append(cluster)
    return np.array(clusters)

# Функція для оновлення центрів кластерів
def update_centroids(points, clusters, k):
    new_centroids = []
    for i in range(k):
        cluster_points = points[clusters == i]
        if len(cluster_points) > 0:
            new_centroids.append(np.mean(cluster_points, axis=0))
        else:
            new_centroids.append(points[np.random.choice(points.shape[0])])
    return np.array(new_centroids)

# Алгоритм KMeans
def kmeans_manual(points, k, max_iters=100, tol=1e-4):
    centroids = initialize_centroids(points, k)
    for _ in range(max_iters):
        clusters = assign_clusters(points, centroids)
        new_centroids = update_centroids(points, clusters, k)
        
        # Перевірка на збіжність
        if np.all(np.abs(new_centroids - centroids) < tol):
            break
        centroids = new_centroids
    return centroids, clusters

# Геолокації точок поломок (випадкові координати)
np.random.seed(42)
demands = np.random.rand(60, 3) * 500 #масштаб діапазону

# Кількість технічних служб
n_services = 5

# Виклик алгоритму KMeans вручну
service_locations, clusters = kmeans_manual(demands, n_services)

# Виведення результатів
print("Оптимальні локації сервісів:")
for i, loc in enumerate(service_locations):
    print(f"Сервіс {i+1}: {loc}")

# Візуалізація результатів
plt.scatter(demands[:, 0], demands[:, 1], c=clusters, cmap='viridis', label='Поломки')
plt.scatter(service_locations[:, 0], service_locations[:, 1], c='red', marker='x', s=200, label='Сервіси')
plt.title('Оптимальне розміщення сервісних центрів (вручну)')
plt.xlabel('X координата')
plt.ylabel('Y координата')
plt.legend()
plt.show()