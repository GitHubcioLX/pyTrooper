from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class DeletionConfirmation(QWidget):
    selected = pyqtSignal(bool)

    def __init__(self, object = "nocascade"):
        super().__init__()
        self.setWindowTitle("Usuń obiekt")
        self.layout = QGridLayout()

        self.messages = {
            "jednostki": "Usunięcie zaznaczonych jednostek spowoduje usunięcie\nwszystkich obiektów przypisanych do nich,\nczy na pewno chcesz kontynuować?",
            "przydzialy": "Czy na pewno chcesz usunąć zaznaczone przydziały?",
            "budynki": "Usunięcie zaznaczonych budynków spowoduje\nusunięcie przypisanych do nich oficerów.\nczy na pewno chcesz kontynuować?",
            "oficerowie": "Usunięcie zaznaczonych oficerów spowoduje usunięcie ich przydziałów.\nczy na pewno chcesz kontynuować?",
            "pojazdy": "Usunięcie zaznaczonych pojazdów spowoduje\nusunięcie ich przydziałów i zamówień.\nczy na pewno chcesz kontynuować?",
            "zamowienia": "Czy na pewno chcesz usnąć zaznaczone zamówienia?",
            "ekwipunek": "Usunięcie zaznaczonego ewkipunku spowoduje\nusunięcie jego przydziałów i zamówień.\nczy na pewno chcesz kontynuować?",
            "nocascade": "Czy na pewno chesz usunąć zaznaczone obiekty?"
        }

        self.naglowek = QLabel()
        self.naglowek.setText(self.messages.get(object))
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
