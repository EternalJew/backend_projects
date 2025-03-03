import osmnx as ox
import networkx as nx

# Завантажити граф доріг для певного міста або координат
place_name = "Rivne, Ukraine"
graph = ox.graph_from_place(place_name, network_type='drive')

# Координати початкової і кінцевої точок
origin_point = (50.6199, 26.2516)  # Задайте координати початку
destination_point = (50.6231, 26.2274)  # Задайте координати кінця

# Найближчі вузли на графі до початкової і кінцевої точок
origin_node = ox.distance.nearest_nodes(graph, origin_point[1], origin_point[0])
destination_node = ox.distance.nearest_nodes(graph, destination_point[1], destination_point[0])

# Побудувати найкоротший шлях за алгоритмом Дейкстри
route = nx.dijkstra_path(graph, origin_node, destination_node, weight='length')

# Отримати координати маршруту
route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

# Вивести координати для передачі на фронтенд
print("Координати маршруту для фронтенду:", route_coords)
