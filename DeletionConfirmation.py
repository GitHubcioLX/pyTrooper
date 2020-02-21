from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DeletionConfirmation(QWidget):
    selected = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Usuń obiekt")
        self.layout = QGridLayout()

        self.naglowek = QLabel()
        self.naglowek.setText("Usunięcie tego obiektu spowoduje usunięcie\nwszystkich obiektów przypisanych do niego,\n"
                              + "czy na pewno chcesz kontynuować?")
        font = QFont()
        font.setBold(True)
        self.naglowek.setAlignment(Qt.AlignCenter)
        self.naglowek.setFont(font)

        self.yesButton = QPushButton("Tak")
        self.noButton = QPushButton("Nie")

        self.set_layout()

        self.yesButton.clicked.connect(self.yes_pressed)
        self.noButton.clicked.connect(self.no_pressed)

    def set_layout(self):
        self.layout.addWidget(self.naglowek, 0, 0, 1, 2)
        self.layout.addWidget(self.yesButton, 1, 0)
        self.layout.addWidget(self.noButton, 1, 1)
        self.setLayout(self.layout)

    def yes_pressed(self):
        self.selected.emit(True)
        self.close()

    def no_pressed(self):
        self.selected.emit(False)
        self.close()
