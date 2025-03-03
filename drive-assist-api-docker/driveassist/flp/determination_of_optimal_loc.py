import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Геолокації точок поломок (умовні координати для Рівного)
demands = np.array([
    (50.615, 26.255), (50.616, 26.256), (50.617, 26.257), (50.618, 26.258), (50.619, 26.259),
    (50.620, 26.260), (50.621, 26.261), (50.622, 26.262), (50.623, 26.263), (50.624, 26.264),
    (50.625, 26.265), (50.626, 26.266), (50.627, 26.267), (50.628, 26.268), (50.629, 26.269),
    (50.630, 26.270), (50.631, 26.271), (50.632, 26.272), (50.633, 26.273), (50.634, 26.274),
    (50.635, 26.275), (50.636, 26.276), (50.637, 26.277), (50.638, 26.278), (50.639, 26.279)
])

np.random.seed(42)
_demands = np.random.rand(25,2) * 100

# Кількість технічних служб, які потрібно розмістити
n_services = 5

# Використання алгоритму KMeans для визначення оптимальних позицій сервісних центрів
kmeans = KMeans(n_clusters=n_services, random_state=0).fit(_demands)

# Координати оптимальних локацій сервісів
service_locations = kmeans.cluster_centers_

# Виведення результатів
print("Оптимальні локації сервісів:")
for i, loc in enumerate(service_locations):
    print(f"Сервіс {i+1}: {loc}")

# Візуалізація поломок та сервісів
plt.scatter(_demands[:, 0], _demands[:, 1], c='blue', label='Поломки')
plt.scatter(service_locations[:, 0], service_locations[:, 1], c='red', marker='x', s=200, label='Сервіси')
plt.title('Оптимальне розміщення сервісних центрів')
plt.xlabel('Широта')
plt.ylabel('Довгота')
plt.legend()
plt.show()