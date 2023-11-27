# This Python file uses the following encoding: utf-8
# genetic_algorithm.py
import numpy as np
import random

# Fitness Function
def calculate_fitness(tour, distance_matrix):
    return 1 / sum(distance_matrix[tour[i]-1][tour[(i+1) % len(tour)]-1] for i in range(len(tour)))

# Initialize Population
def initialize_population(pop_size, num_nodes):
    return [random.sample(range(1, num_nodes + 1), num_nodes) for _ in range(pop_size)]

# Selection Function (Tournament Selection)
def tournament_selection(population, fitnesses, tournament_size):
    selected = []
    for _ in range(len(population)):
        tournament = [random.choice(list(zip(population, fitnesses))) for _ in range(tournament_size)]
        selected.append(max(tournament, key=lambda x: x[1])[0])
    return selected

# Crossover Function (Ordered Crossover)
def ordered_crossover(parent1, parent2):
    start, end = sorted(random.sample(range(len(parent1)), 2))
    child = [None] * len(parent1)
    child[start:end] = parent1[start:end]
    child_items = set(child[start:end])
    child[end:] = [item for item in parent2 if item not in child_items]
    child[:start] = [item for item in parent2 if item not in child_items and item not in child[end:]]
    return child

# Mutation Function (Swap Mutation)
def swap_mutation(tour, mutation_rate):
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(tour)), 2)
        tour[i], tour[j] = tour[j], tour[i]
    return tour

# Genetic Algorithm Main Function
def genetic_algorithm(distance_matrix, pop_size, generations, mutation_rate, tournament_size, elite_size):
    num_nodes = len(distance_matrix)
    population = initialize_population(pop_size, num_nodes)
    best_fitness = float('inf')
    best_tour = None

    for generation in range(generations):
        fitnesses = [calculate_fitness(tour, distance_matrix) for tour in population]
        fittest_index = np.argmax(fitnesses)
        fittest_value = 1 / fitnesses[fittest_index]

        if fittest_value < best_fitness:
            best_fitness = fittest_value
            best_tour = population[fittest_index]

        selected = tournament_selection(population, fitnesses, tournament_size)
        children = [ordered_crossover(selected[i], selected[(i + 1) % len(selected)]) for i in range(0, len(selected), 2)]

        mutated_children = [swap_mutation(child, mutation_rate) for child in children]
        population = mutated_children[:]

        # Implementing elitism by keeping the best solution
        if elite_size > 0:
            population = sorted(zip(population, fitnesses), key=lambda x: x[1], reverse=True)
            population = [x[0] for x in population]  # Unzip to get only the tours
            for i in range(elite_size):
                population[-(i+1)] = best_tour

        if generation % 100 == 0 or generation == generations - 1:
            print(f"Generation {generation}: Best distance so far: {best_fitness}")

    return best_tour, best_fitness



# Export this function for use in other files
def run_genetic_algorithm(distance_matrix, pop_size, generations, mutation_rate, tournament_size, elite_size):
    return genetic_algorithm(distance_matrix, pop_size, generations, mutation_rate, tournament_size, elite_size)

# if __name__ == "__main__":
#     pass
