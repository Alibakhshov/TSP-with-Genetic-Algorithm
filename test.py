import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from typing import List
import random
import numpy
import math
from itertools import cycle


# TSP parameters
CITY_COORDINATES = [[5, 80], [124, 31], [46, 54], [86, 148], [21, 8],
                   [134, 72], [49, 126], [36, 34], [26, 49], [141, 6],
                   [124, 122], [80, 92], [70, 69], [76, 133], [23, 65]]
TOTAL_CHROMOSOME = len(CITY_COORDINATES) - 1

# Genetic Algorithm parameters
POPULATION_SIZE = 300
MAX_GENERATION = 400
MUTATION_RATE = 0.2
WEAKNESS_THRESHOLD = 900


class Genome:
    def __init__(self, chromosome=None):
        self.chromosome = chromosome if chromosome else []
        self.fitness = 0

    def __str__(self):
        return f"Chromosome: {self.chromosome} Fitness: {self.fitness}\n"

    def __repr__(self):
        return str(self)


def create_genome() -> Genome:
    genome = Genome()

    try:
        # Ensure that the sample size is not larger than the population or negative
        sample_size = min(TOTAL_CHROMOSOME, max(1, TOTAL_CHROMOSOME - 1))

        genome.chromosome = random.sample(range(1, TOTAL_CHROMOSOME + 1), sample_size)
        genome.fitness = eval_chromosome(genome.chromosome)
    except ValueError as e:
        print(f"Error in create_genome: {e}")
        # Handle the error here or re-raise it if needed

    return genome


def eval_chromosome(chromosome: List[int]) -> float:
    arr = [0] + chromosome + [0]
    fitness = 0
    for i in range(len(arr) - 1):
        p1, p2 = CITY_COORDINATES[arr[i]], CITY_COORDINATES[arr[i + 1]]
        fitness += distance(p1, p2)
    return numpy.round(fitness, 2)


def distance(a, b) -> float:
    return numpy.round(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2), 2)


def get_fittest_genome(genomes: List[Genome]) -> Genome:
    return min(genomes, key=lambda x: x.fitness)


def tournament_selection(population: List[Genome], k: int) -> List[Genome]:
    return max(random.sample(population, k), key=lambda x: x.fitness)


def order_crossover(parents: List[Genome]) -> Genome:
    subset_length = random.randint(2, 5)
    crossover_point = random.randrange(0, TOTAL_CHROMOSOME - subset_length)

    child_chro = parents[0].chromosome[crossover_point:crossover_point + subset_length]

    indices_to_fill = [(crossover_point + subset_length + i) % TOTAL_CHROMOSOME for i in range(TOTAL_CHROMOSOME)
                       if i < crossover_point or i >= crossover_point + subset_length]

    unused_values = cycle(set(parents[1].chromosome) - set(child_chro))

    for index_to_fill in indices_to_fill:
        try:
            child_chro.append(next(unused_values))
        except StopIteration as e:
            print(f"Error in order_crossover: {e}")
            # Handle the error here or re-raise it if needed

    child = Genome(child_chro)
    child.fitness = eval_chromosome(child.chromosome)
    return child


def scramble_mutation(genome: Genome) -> Genome:
    subset_length = random.randint(2, min(6, TOTAL_CHROMOSOME - 1))
    start_point = random.randint(0, TOTAL_CHROMOSOME - subset_length)
    subset_index = slice(start_point, start_point + subset_length)

    try:
        genome.chromosome[subset_index] = random.sample(genome.chromosome[subset_index], subset_length)
        genome.fitness = eval_chromosome(genome.chromosome)
    except ValueError as e:
        print(f"Error in scramble_mutation: {e}")
        # Handle the error here or re-raise it if needed

    return genome


def reproduction(population: List[Genome]) -> Genome:
    parents = [tournament_selection(population, 20), random.choice(population)]
    child = order_crossover(parents)
    if random.random() < MUTATION_RATE:
        scramble_mutation(child)
    return child


class TSPGeneticAlgorithmApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("TSP Genetic Algorithm")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.population_size_label = QLabel("Population Size:", self)
        self.population_size_input = QLineEdit(self)
        self.population_size_input.setText(str(POPULATION_SIZE))

        self.max_generation_label = QLabel("Max Generation:", self)
        self.max_generation_input = QLineEdit(self)
        self.max_generation_input.setText(str(MAX_GENERATION))

        self.mutation_rate_label = QLabel("Mutation Rate:", self)
        self.mutation_rate_input = QLineEdit(self)
        self.mutation_rate_input.setText(str(MUTATION_RATE))

        self.weakness_threshold_label = QLabel("Weakness Threshold:", self)
        self.weakness_threshold_input = QLineEdit(self)
        self.weakness_threshold_input.setText(str(WEAKNESS_THRESHOLD))

        self.start_button = QPushButton("Start Genetic Algorithm", self)
        self.start_button.clicked.connect(self.run_genetic_algorithm)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.ax.set_title("Initial State")

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.population_size_label)
        layout.addWidget(self.population_size_input)
        layout.addWidget(self.max_generation_label)
        layout.addWidget(self.max_generation_input)
        layout.addWidget(self.mutation_rate_label)
        layout.addWidget(self.mutation_rate_input)
        layout.addWidget(self.weakness_threshold_label)
        layout.addWidget(self.weakness_threshold_input)
        layout.addWidget(self.start_button)
        layout.addWidget(self.canvas)

        self.generation = 0
        self.population = []

    def run_genetic_algorithm(self):
        self.generation = 0
        self.population = []
        self.ax.clear()

        population_size = int(self.population_size_input.text())
        max_generation = int(self.max_generation_input.text())
        mutation_rate = float(self.mutation_rate_input.text())
        weakness_threshold = float(self.weakness_threshold_input.text())

        # Initialize population
        self.population = [create_genome() for _ in range(population_size)]

        while self.generation != max_generation:
            self.generation += 1
            print("Generation: {0} -- Population size: {1} -- Best Fitness: {2}"
                  .format(self.generation, len(self.population), get_fittest_genome(self.population).fitness))

            # Create new generation
            try:
                childs = [reproduction(self.population) for _ in range(int(population_size * 0.2))]
                self.population.extend(childs)
            except Exception as e:
                print(f"Error in run_genetic_algorithm: {e}")
                # Handle the error here or re-raise it if needed

            # Remove weak genomes
            self.population = [genome for genome in self.population if genome.fitness <= weakness_threshold]

            self.visualize()

    def visualize(self):
        self.ax.clear()

        best_genome = get_fittest_genome(self.population)
        chromosome = [0] + best_genome.chromosome + [0]
        coordinates = [CITY_COORDINATES[i] for i in chromosome]
        x, y = zip(*coordinates)

        self.ax.plot(x, y, color="midnightblue")
        self.ax.scatter(x, y, color="midnightblue")

        for i, xy in enumerate(coordinates[:-1]):
            self.ax.annotate(i, xy, xytext=(-16, -4), textcoords="offset points", color="tab:red")

        self.ax.set_title("Route")
        self.ax.set_ylabel('Y')
        self.ax.set_xlabel('X')

        self.canvas.draw()


def main():
    app = QApplication(sys.argv)
    window = TSPGeneticAlgorithmApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
