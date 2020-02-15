import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class EquipmentListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.equipmnet = QListWidget()
        self.addButton = QPushButton("Dodaj")
        self.layout = QVBoxLayout()
        self.setWindowTitle("Ekwipunek")
        self.set_jednostki()
        self.set_layout()

    def set_jednostki(self):
        self.equipmnet.addItem("Kurwa dupa chuj")
        self.equipmnet.addItem("Kurwa chuj dupa")
        self.equipmnet.addItem("Dupa kurwa chuj")
        self.equipmnet.addItem("Chuj kurwa dupa")

    def set_layout(self):
        self.layout.addWidget(self.equipmnet)
        self.layout.addWidget(self.addButton)
        self.setLayout(self.layout)