import argparse
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
        found = False
        for neighbor, cost in neighbors:
            if neighbor == next_node:
                distance += cost
                found = True
                break
        if not found:
            raise ValueError(f"No edge found between {current_node} and {next_node}")
    return distance

def generate_random_path(cities):
    return random.sample(cities, len(cities))

def genetic_algorithm(graph, cities, population_size=10, generations=100):
    population = [generate_random_path(cities) for _ in range(population_size)]
    for _ in range(generations):
        population = evolve_population(population, graph)
    return population

def evolve_population(population, graph, mutation_rate=0.1):
    new_population = []
    while len(new_population) < len(population):
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        child = reproduce(parent1, parent2)
        if random.random() < mutation_rate:
            child = mutate(child, graph)
        new_population.append(child)
    return new_population

def reproduce(parent1, parent2):
    crossover_point = random.randint(0, len(parent1) - 1)
    child = parent1[:crossover_point]
    for city in parent2:
        if city not in child:
            child.append(city)
    return child

def mutate(path, graph):
    mutation_point1 = random.randint(0, len(path) - 1)
    mutation_point2 = random.randint(0, len(path) - 1)
    path[mutation_point1], path[mutation_point2] = path[mutation_point2], path[mutation_point1]
    return path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Traveling Salesman Problem Solver')
    parser.add_argument('--file', help='Path to the cities file')

    args = parser.parse_args()

    if args.file:
        cities_graph = Graph()
        add_edges_from_file(cities_graph, args.file)

        cities = list(cities_graph.map.keys())

        best_path = None
        best_cost = float('inf')
        population = genetic_algorithm(cities_graph, cities, population_size=20, generations=1000)

        for path in population:
            cost = tsp_fitness(path, cities_graph)
            if cost < best_cost:
                best_cost = cost
                best_path = path

        print("Best route found:", best_path)
        print("Cost of best route:", best_cost)
    else:
        print("Please specify the path to the cities file using --file option.")
