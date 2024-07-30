import time
import argparse
from hill import get_initial_path, hill_climbing
from genetic import genetic_algorithm
from simulated import simulated_annealing
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
    from math import radians, sin, cos, sqrt, atan2

    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    radius_of_earth = 6371  # in kilometers
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

def main():
    parser = argparse.ArgumentParser(description='Compare TSP Solvers')
    parser.add_argument('--file', help='Path to the cities file')
    args = parser.parse_args()

    if args.file:
        cities_graph = Graph()
        add_edges_from_file(cities_graph, args.file)

        cities = list(cities_graph.map.keys())

        algorithms = [
            ('Hill Climbing', hill_climbing),
            ('Genetic Algorithm', genetic_algorithm),
            ('Simulated Annealing', simulated_annealing)
        ]

        num_cities = [8, 16, 20]
        num_iterations = 5000

        for num_city in num_cities:
            print(f"\nComparison for {num_city} cities:")
            selected_cities = cities[:num_city]

            for name, algorithm in algorithms:
                start_time = time.time()
                
                current_cost, _, current_route = get_initial_path(cities_graph, selected_cities)  # Reset current_route and current_cost for each algorithm
                if algorithm == hill_climbing:
                    best_route, best_cost = hill_climbing(current_route, current_cost, num_iterations, cities_graph, selected_cities)
                elif algorithm == genetic_algorithm:
                    best_path = None
                    best_cost = float('inf')
                    population = genetic_algorithm(cities_graph, selected_cities, population_size=20, generations=1000)

                    for path in population:
                        cost = tsp_fitness(path, cities_graph)
                        if cost < best_cost:
                            best_cost = cost
                            best_path = path
                    best_route = best_path
                elif algorithm == simulated_annealing:
                    start_temp = 100
                    end_temp = 0.1
                    cooling_rate = 0.99
                    current_cost, _, current_route = get_initial_path(cities_graph, selected_cities)  # Reset current_route and current_cost for simulated annealing
                    best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations, cities_graph)

                end_time = time.time()
                execution_time = end_time - start_time

                print(f"{name}:")
                print("Best route found:", best_route)
                print("Cost of best route:", best_cost)
                print("Execution time:", execution_time, "seconds")


    else:
        print("Please specify the path to the cities file using --file option.")

if __name__ == "__main__":
    main()
