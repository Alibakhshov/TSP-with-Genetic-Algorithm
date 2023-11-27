from PySide6.QtWidgets import QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QComboBox, QVBoxLayout, QWidget, QHBoxLayout, QLabel, QMessageBox
from genetic_algorithm import run_genetic_algorithm
from result_window import ResultWindow

class TableInputWindow(QMainWindow):
    def __init__(self, matrix_size, parent=None):
        super().__init__(parent)
        self.matrix_size = matrix_size
        self.setWindowTitle("Matrix Input")
        self.initUI()
        self.adjustWindowSize()

    def initUI(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Create and setup the table
        self.table = QTableWidget(self.matrix_size, self.matrix_size, self)
        self.setupTable()
        layout.addWidget(self.table)

        # Label for starting node select box
        start_node_label = QLabel("Select the starting node:", self)
        layout.addWidget(start_node_label)

        # Combo box for starting node
        self.start_node_box = QComboBox(self)
        for i in range(self.matrix_size):
            self.start_node_box.addItem(chr(65 + i))  # ASCII 65 is 'A'
        layout.addWidget(self.start_node_box)

        # Horizontal layout for buttons
        button_layout = QHBoxLayout()

        # Buttons
        self.run_button = QPushButton("Run", self)
        self.reset_button = QPushButton("Reset", self)
        self.quit_button = QPushButton("Quit", self)
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.quit_button)

        # Add button layout to the main layout
        layout.addLayout(button_layout)

        # Connect the Quit button
        self.quit_button.clicked.connect(self.close)

        # Connect the Reset button
        self.reset_button.clicked.connect(self.reset_table)

        # Connect the Run button
        self.run_button.clicked.connect(self.run_algorithm)

        # Connect buttons
        # self.run_button.clicked.connect(self.run_algorithm)
        # self.reset_button.clicked.connect(self.reset_table)
        # self.quit_button.clicked.connect(self.close)

        # Connect the table's itemChanged signal
        self.table.itemChanged.connect(self.cell_updated)



    def run_algorithm(self):
        # Extract distance matrix from the table
        distance_matrix = self.extract_distance_matrix()

        # Genetic Algorithm parameters
        population_size = 100
        generations = 1000
        mutation_rate = 0.01
        tournament_size = 5
        elite_size = 1

        # Run the genetic algorithm
        best_solution, best_solution_fitness = run_genetic_algorithm(
            distance_matrix, population_size, generations, mutation_rate, tournament_size, elite_size)

        # Open the ResultWindow with the results
        self.result_window = ResultWindow(best_solution, best_solution_fitness, distance_matrix)
        self.result_window.show()



    def extract_distance_matrix(self):
        matrix_size = self.matrix_size
        distance_matrix = []

        # Proceed only if the matrix is valid
        if distance_matrix is not None:
            # ... run the genetic algorithm and open the ResultWindow ...
            try:
                for i in range(matrix_size):
                    row = []
                    for j in range(matrix_size):
                        item = self.table.item(i, j)
                        if not item or not item.text().strip():
                            raise ValueError("Matrix is incomplete.")
                        distance = float(item.text())
                        row.append(distance)
                    distance_matrix.append(row)

                return distance_matrix

            except ValueError as e:
                QMessageBox.warning(self, "Input Error", str(e))
                return None





    def reset_table(self):
        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                if i != j:  # Skip diagonal
                    self.table.setItem(i, j, QTableWidgetItem(""))



    def cell_updated(self, item):
        row = item.row()
        col = item.column()

        if row != col:  # Ignore diagonal cells
            self.table.blockSignals(True)
            symmetric_item = self.table.item(col, row)
            if symmetric_item is None:
                symmetric_item = QTableWidgetItem()
                self.table.setItem(col, row, symmetric_item)
            symmetric_item.setText(item.text())
            self.table.blockSignals(False)


    def adjustWindowSize(self):
        # Set preferred column width
        column_width = 80  # Adjust this value based on your preference
        row_height = 40

        # Calculate total width (add some extra for margins and scrollbar)
        total_width = self.matrix_size * column_width + 50
        total_height = self.matrix_size * row_height + 130  # Extra for buttons, select box, and margins

        # Resize the window
        self.resize(total_width, total_height)

        # Adjust column widths and row heights in the table
        for i in range(self.matrix_size):
            self.table.setColumnWidth(i, column_width)
            self.table.setRowHeight(i, row_height)



    def setupTable(self):
        headers = [chr(65 + i) for i in range(self.matrix_size)]  # ASCII 65 is 'A'
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setVerticalHeaderLabels(headers)
        for i in range(self.matrix_size):
            self.table.setItem(i, i, QTableWidgetItem("0"))  # Prefill diagonal with zeros

        # Connect cell edit signal
        # self.table.itemChanged.connect(self.autofill_symmetric_cell)

    # Implement autofill_symmetric_cell, reset_table, and run_algorithm methods
