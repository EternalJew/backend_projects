import osmnx as ox
import networkx as nx

def get_route_coordinates(origin_point_dict, destination_point_dict):
    place_name = "Rivne, Ukraine"
    """
    Функція для отримання координат найкоротшого маршруту між двома точками.
    
    Parameters:
    - place_name (str): Назва місця для завантаження графа доріг (наприклад, "Rivne, Ukraine").
    - origin_point_dict (dict): Координати початкової точки у форматі {'latitude': ..., 'longitude': ...}.
    - destination_point_dict (dict): Координати кінцевої точки у форматі {'latitude': ..., 'longitude': ...}.
    
    Returns:
    - list: Список координат маршруту для передачі на фронтенд.
    """
    # Перетворення координат із словників у кортежі (latitude, longitude)
    origin_point = (origin_point_dict['latitude'], origin_point_dict['longitude'])
    destination_point = (destination_point_dict['latitude'], destination_point_dict['longitude'])
    
    # Завантажити граф доріг для вказаного місця
    graph = ox.graph_from_place(place_name, network_type='drive')

    # Знайти найближчі вузли на графі до початкової та кінцевої точок
    origin_node = ox.distance.nearest_nodes(graph, origin_point[1], origin_point[0])
    destination_node = ox.distance.nearest_nodes(graph, destination_point[1], destination_point[0])

    # Побудувати найкоротший шлях за алгоритмом Дейкстри
    route = nx.dijkstra_path(graph, origin_node, destination_node, weight='length')

    # Отримати координати маршруту
    route_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node in route]

    return route_coords

# Приклад використання
# place_name = "Rivne, Ukraine"
# origin_point = {'latitude': 50.6199, 'longitude': 26.2516}
# destination_point = {'latitude': 50.6231, 'longitude': 26.2274}

# route_coords = get_route_coordinates(place_name, origin_point, destination_point)
# print("Координати маршруту для фронтенду:", route_coords)