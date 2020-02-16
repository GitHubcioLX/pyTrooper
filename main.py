import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EquipmentListWindow import EquipmentListWindow
from UnitManagement import UnitManagement
from connector import Connector
from Utilities import create_table

# GUI
app = QApplication([])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.naglowek = QLabel()
        self.naglowek.setText("Zarządzanie jednostką")
        font = QFont()
        font.setBold(True)
        self.naglowek.setAlignment(Qt.AlignCenter)
        self.naglowek.setFont(font)

        self.jednostki = QTableWidget()

        self.addButton = QPushButton("Dodaj")

        self.gap = QLabel()

        self.equipLabel = QLabel()
        self.equipLabel.setText("Zarządzanie ekwipunkiem")
        self.equipLabel.setAlignment(Qt.AlignCenter)
        self.equipLabel.setFont(font)

        self.ekwipunek = QPushButton("Ekwipunek wojska")

        self.layout = QVBoxLayout()

        self.setWindowTitle("Menu główne")
        self.set_jednostki()
        self.set_layout()
        self.setMinimumSize(500, 500)

        self.unitwindow = None
        self.equipment_window = EquipmentListWindow()

        self.ekwipunek.clicked.connect(self.open_equipment)
        self.jednostki.cellDoubleClicked.connect(self.open_jednostki)

    def open_equipment(self):
        self.equipment_window.show()

    def set_jednostki(self):
        self.jednostki = create_table(['Identyfikator', 'Nazwa'], Connector.get_table_data("jednostki", ["identyfikator", "nazwa"]))

    def open_jednostki(self, rowid):
        item = self.jednostki.item(rowid, 0)
        self.unitwindow = UnitManagement(item.text())
        self.unitwindow.show()

    def set_layout(self):
        self.layout.addWidget(self.naglowek)
        self.layout.addWidget(self.jednostki)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.gap)
        self.layout.addWidget(self.equipLabel)
        self.layout.addWidget(self.ekwipunek)
        self.layout.addWidget(self.gap)
        self.setLayout(self.layout)

    def closeEvent(self, QCloseEvent):
        app.closeAllWindows()


main_window = MainWindow()
main_window.show()

app.exec_()
