# This Python file uses the following encoding: utf-8
# result_window.py
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QGroupBox
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import FancyArrowPatch
from matplotlib.figure import Figure
from genetic_algorithm import run_genetic_algorithm

class ResultWindow(QDialog):
    def __init__(self, tour, fitness, distance_matrix, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TSP Shortest path calculated with Genetic Algorithm")
        self.tour = tour
        self.fitness = fitness
        self.distance_matrix = distance_matrix
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout(self)

        # Left side - Graph
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        # Right side - Results and Parameters
        right_layout = QVBoxLayout()

        # Results Group
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        self.best_tour_label = QLabel("Best Tour: " + ' - '.join(map(str, self.tour)))
        self.best_distance_label = QLabel(f"Best Distance: {self.fitness:.2f}")
        results_layout.addWidget(self.best_tour_label)
        results_layout.addWidget(self.best_distance_label)
        right_layout.addWidget(results_group)

        # GA Parameters Group
        params_group = QGroupBox("GA Parameters")
        params_layout = QVBoxLayout(params_group)
        self.pop_size_input = QLineEdit("100")
        self.generations_input = QLineEdit("1000")
        self.mutation_rate_input = QLineEdit("0.01")
        self.tournament_size_input = QLineEdit("5")
        self.elite_size_input = QLineEdit("1")
        params_layout.addWidget(QLabel("Population Size"))
        params_layout.addWidget(self.pop_size_input)
        params_layout.addWidget(QLabel("Generations"))
        params_layout.addWidget(self.generations_input)
        params_layout.addWidget(QLabel("Mutation Rate"))
        params_layout.addWidget(self.mutation_rate_input)
        params_layout.addWidget(QLabel("Tournament Size"))
        params_layout.addWidget(self.tournament_size_input)
        params_layout.addWidget(QLabel("Elite Size"))
        params_layout.addWidget(self.elite_size_input)
        right_layout.addWidget(params_group)

        # Re-run Button
        rerun_button = QPushButton("Re-run")
        rerun_button.clicked.connect(self.rerun_algorithm)
        right_layout.addWidget(rerun_button)

        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.plot_graph()



    def plot_graph(self):

        G = nx.Graph()

        # Adding nodes
        for i in range(len(self.distance_matrix)):
            G.add_node(chr(65 + i))

        # Adding edges with weights
        for i in range(len(self.distance_matrix)):
            for j in range(i+1, len(self.distance_matrix)):
                G.add_edge(chr(65 + i), chr(65 + j), weight=self.distance_matrix[i][j])

        pos = nx.circular_layout(G)  # Nodes in a circle

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        nx.draw_networkx_nodes(G, pos, node_color='white', edgecolors='black', node_size=400, ax=ax)
        nx.draw_networkx_labels(G, pos, font_color='black', ax=ax)
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color='gray', alpha=0.5)

        # Extracting edges in the TSP path
        # Assuming self.tour contains node indices starting from 1
        tsp_edges = [(chr(65 + self.tour[i] - 1), chr(65 + self.tour[(i+1) % len(self.tour)] - 1)) for i in range(len(self.tour))]
        nx.draw_networkx_edges(G, pos, edgelist=tsp_edges, edge_color='green', width=2, ax=ax)

        # Edge labels (weights)
        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='black', ax=ax)

        ax.set_aspect('equal')
        ax.axis('off')
        self.canvas.draw()




    def rerun_algorithm(self):
        # Extract parameters
        pop_size = int(self.pop_size_input.text())
        generations = int(self.generations_input.text())
        mutation_rate = float(self.mutation_rate_input.text())
        tournament_size = int(self.tournament_size_input.text())
        elite_size = int(self.elite_size_input.text())

        # Run the genetic algorithm with new parameters
        new_tour, new_fitness = run_genetic_algorithm(
            self.distance_matrix, pop_size, generations, mutation_rate, tournament_size, elite_size)

        # Update the tour and fitness
        self.tour = new_tour
        self.fitness = new_fitness

        # Update the labels for Best Tour and Best Distance
        self.best_tour_label.setText("Best Tour: " + ' - '.join(map(str, [chr(65 + node - 1) for node in self.tour])))
        self.best_distance_label.setText(f"Best Distance: {self.fitness:.2f}")

        # Update the graph
        self.plot_graph()


