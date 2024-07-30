import argparse
import math
import random
from graph import Graph

def read_cities_from_file(filename):
    cities = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 3:
                    name = parts[0]
                    latitude = float(parts[1])
                    longitude = float(parts[2])
                    cities[name] = (latitude, longitude)
                else:
                    print(f"Ignoring improperly formatted line: {line}")
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except Exception as e:
        print(f"Error reading file '{filename}': {str(e)}")
    return cities

def add_edges_from_file(graph, filename):
    cities = read_cities_from_file(filename)
    for city1 in cities:
        for city2 in cities:
            if city1 != city2:
                lat1, lon1 = cities[city1]
                lat2, lon2 = cities[city2]
                # Calculating distance using Haversine formula
                distance = haversine(lon1, lat1, lon2, lat2)
                graph.addEdge(city1, city2, distance)

def haversine(lon1, lat1, lon2, lat2):
    # Haversine formula implementation
    radius_of_earth = 6371  # in kilometers
    dlon = math.radians(lon2 - lon1)
    dlat = math.radians(lat2 - lat1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius_of_earth * c
    return distance

def tsp_fitness(path, graph):
    distance = 0
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        neighbors = graph.getNeighbours(current_node)
        edge_weight = None
        for neighbor, weight in neighbors:
            if neighbor == next_node:
                edge_weight = weight
                break
        if edge_weight is None:
            raise ValueError(f"No edge between {current_node} and {next_node}")
        distance += edge_weight
    return distance

def get_initial_path(graph):
    population = []
    cities = list(graph.map.keys())
    current = random.choice(cities)
    goal = current
    for _ in range(20):
        unvisited_cities = set(cities)
        unvisited_cities.remove(current)
        path = [current]
        all_visited = 0

        while unvisited_cities:
            neighbors = graph.getNeighbours(current)  # Extract neighboring nodes
            good_neighbors = [neighbor for neighbor, _ in neighbors if neighbor in unvisited_cities]
            if good_neighbors:
                random_neighbor = random.choice(good_neighbors)
                unvisited_cities.remove(random_neighbor)
            else:
                random_neighbor = random.choice([neighbor for neighbor, _ in neighbors])
            path.append(random_neighbor)
            current = random_neighbor
            all_visited += 1

        while current != goal:
            neighbors = graph.getNeighbours(current)  # Extract neighboring nodes
            random_neighbor = random.choice([neighbor for neighbor, _ in neighbors])
            path.append(random_neighbor)
            current = random_neighbor
            all_visited += 1

        population.append((tsp_fitness(path, graph), all_visited, path))
    return sorted(population)[0]

def get_successor(graph, prev_path):
    successors = []
    goal = prev_path[0]
    cities = list(graph.map.keys())
    for _ in range(10):
        rand_ind = random.randint(1, len(prev_path) - 1)
        path = prev_path[:rand_ind]
        current = prev_path[rand_ind - 1]
        unvisited_cities = set(cities).difference(set(path))
        all_visited = 0

        while unvisited_cities:
            neighbors = graph.getNeighbours(current)  # Extract neighboring nodes
            good_neighbors = [neighbor for neighbor, _ in neighbors if neighbor in unvisited_cities]
            if good_neighbors:
                random_neighbor = random.choice(good_neighbors)
                unvisited_cities.remove(random_neighbor)
            else:
                random_neighbor = random.choice([neighbor for neighbor, _ in neighbors])
            path.append(random_neighbor)
            current = random_neighbor
            all_visited += 1

        while current != goal:
            neighbors = graph.getNeighbours(current)  # Extract neighboring nodes
            random_neighbor = random.choice([neighbor for neighbor, _ in neighbors])
            path.append(random_neighbor)
            current = random_neighbor
            all_visited += 1

        successors.append((tsp_fitness(path, graph), all_visited, path))
    return sorted(successors)[0]

def simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations, cities_graph):
    best_route = current_route
    best_cost = current_cost
    temp = start_temp
    for i in range(num_iterations):
        neighbor_cost, _, neighbor_route = get_successor(cities_graph, best_route)
        if neighbor_cost < current_cost or random.random() < math.exp((current_cost - neighbor_cost) / temp):
            current_route = neighbor_route
            current_cost = neighbor_cost
        if current_cost < best_cost:
            best_route = current_route
            best_cost = current_cost
        temp *= cooling_rate
        if temp < end_temp:
            break
    return best_route, best_cost

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Traveling Salesman Problem Solver')
    parser.add_argument('--file', help='Path to the cities file')

    args = parser.parse_args()

    if args.file:
        cities_graph = Graph()
        add_edges_from_file(cities_graph, args.file)

        current_cost, _, current_route = get_initial_path(cities_graph)

        start_temp = 100
        end_temp = 0.1
        cooling_rate = 0.99
        num_iterations = 10000

        best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations, cities_graph)

        print("Best route found: ", best_route)
        print("Cost of best route: ", best_cost)
    else:
        print("Please specify the path to the cities file using --file option.")
