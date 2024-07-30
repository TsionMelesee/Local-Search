import argparse
import random
from genetic import add_edges_from_file as genetic_add_edges_from_file, genetic_algorithm, tsp_fitness as genetic_fitness
from graph import Graph as CitiesGraph
from hill import get_initial_path as hill_get_initial_path, hill_climbing, main as hill_main
from simulated import simulated_annealing, get_initial_path as simulated_get_initial_path

def main():
    parser = argparse.ArgumentParser(description='Traveling Salesman Problem Solver')
    parser.add_argument('--algorithm', choices=['sa', 'ha', 'ga'], help='Algorithm to use (sa for simulated annealing, ha for hill climbing, ga for genetic algorithm)')
    parser.add_argument('--cities', help='Path to the cities file')  # Change '--file' to '--cities'

    args = parser.parse_args()

    if args.algorithm == 'sa':
        if args.cities:  # Change 'args.file' to 'args.cities'
            cities_graph = CitiesGraph()
            genetic_add_edges_from_file(cities_graph, args.cities)  # Change 'args.file' to 'args.cities'

            current_cost, _, current_route = simulated_get_initial_path(cities_graph)

            start_temp = 100
            end_temp = 0.1
            cooling_rate = 0.99
            num_iterations = 10000

            best_route, best_cost = simulated_annealing(current_route, current_cost, start_temp, end_temp, cooling_rate, num_iterations, cities_graph)

            print("Best route found using simulated annealing: ", best_route)
            print("Cost of best route: ", best_cost)
        else:
            print("Please specify the path to the cities file.")
    elif args.algorithm == 'ha':
        if args.cities:  # Change 'args.file' to 'args.cities'
            cities_graph = CitiesGraph()
            genetic_add_edges_from_file(cities_graph, args.cities)  # Change 'args.file' to 'args.cities'
            cities = list(cities_graph.map.keys())
            num_iterations = 500
            current_cost, _, current_route = hill_get_initial_path(cities_graph, cities)
            best_route, best_cost = hill_climbing(current_route, current_cost, num_iterations, cities_graph, cities)
            print("Best route found using hill climbing: ", best_route)
            print("Cost of best route: ", best_cost)
        else:
            print("Please specify the path to the cities file.")
    elif args.algorithm == 'ga':
        if args.cities:
            cities_graph = CitiesGraph()
            genetic_add_edges_from_file(cities_graph, args.cities)
            cities = list(cities_graph.map.keys())  # Get the list of cities
            population_size = 20
            generations = 1000
            best_path = None
            best_cost = float('inf')
            population = genetic_algorithm(cities_graph, cities, population_size=population_size, generations=generations)  # Pass 'cities' as an argument
            for path in population:
                cost = genetic_fitness(path, cities_graph)
                if cost < best_cost:
                    best_cost = cost
                    best_path = path
            print("Best route found using genetic algorithm:", best_path)
            print("Cost of best route:", best_cost)
        else:
            print("Please specify the path to the cities file.")


if __name__ == "__main__":
    main()