# This Python file uses the following encoding: utf-8
import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QHBoxLayout
from tableinputwindow import TableInputWindow

class TSPSolver(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TSP Solver with Genetic Algorithm")
        self.initUI()

    def initUI(self):
        # Main widget and layout
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Information label
        info_label = QLabel("Welcome to the TSP Solver. Please choose the matrix size.", self)
        main_layout.addWidget(info_label)

        # Horizontal layout for the combo box and button
        hbox = QHBoxLayout()

        # Combo box for matrix size
        self.matrix_size_box = QComboBox(self)
        for i in range(3, 11):  # Adding options 3 to 10
            self.matrix_size_box.addItem(str(i))
        hbox.addWidget(self.matrix_size_box)

        # OK button
        ok_button = QPushButton("OK", self)
        ok_button.clicked.connect(self.on_ok_clicked)
        hbox.addWidget(ok_button)

        # Add horizontal layout to the main layout
        main_layout.addLayout(hbox)

    def on_ok_clicked(self):
        # Get the selected matrix size
        matrix_size = int(self.matrix_size_box.currentText())

        # Open the TableInputWindow
        self.table_input_window = TableInputWindow(matrix_size)
        self.table_input_window.show()

        # Optionally, close the current window
        self.close()

        print(f"Selected Matrix Size: {matrix_size}")  # Placeholder for now

if __name__ == "__main__":
    app = QApplication([])
    window = TSPSolver()
    window.show()
    sys.exit(app.exec())
