import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EquipmentListWindow import EquipmentListWindow
from UnitManagement import UnitManagement
from connector import Connector
from Utilities import create_table
from UnitForm import UnitForm

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
        self.delButton = QPushButton("Usuń")

        self.equipLabel = QLabel()
        self.equipLabel.setText("Zarządzanie ekwipunkiem")
        self.equipLabel.setAlignment(Qt.AlignCenter)
        self.equipLabel.setFont(font)

        self.ekwipunek = QPushButton("Ekwipunek wojska")
        self.rangi = QPushButton("Rangi")

        self.layout = QVBoxLayout()

        self.setWindowTitle("Menu główne")
        self.setMinimumSize(500, 500)
        self.set_jednostki()

        self.unitwindow = None
        self.unitcreation = None
        self.equipment_window = EquipmentListWindow()

    def create_unit(self):
        self.unitcreation = UnitForm(self)
        self.unitcreation.show()

    def open_equipment(self):
        self.equipment_window.show()

    def set_jednostki(self):
        self.layout.removeWidget(self.jednostki)
        self.jednostki = create_table(['Identyfikator', 'Nazwa'], Connector.get_table_data("jednostki", ["identyfikator", "nazwa"]))
        self.set_layout()

    def open_jednostki(self, rowid):
        item = self.jednostki.item(rowid, 0)
        self.unitwindow = UnitManagement(item.text())
        self.unitwindow.show()

    def delete_items(self):
        selection = self.jednostki.selectedItems()
        if selection:
            res = []
            for x in selection:
                res.append(self.jednostki.item(x.row(), 0).text())
            res = list(dict.fromkeys(res))
            Connector.delete_items("jednostki", res, "identyfikator", int)
            self.set_jednostki()

    def set_layout(self):
        #self.layout.addWidget(self.naglowek)
        #self.layout.addWidget(self.jednostki)
        button_box = QGroupBox("Zarządzanie jednostką")
        b_box_layout = QGridLayout()
        b_box_layout.addWidget(self.jednostki, 0, 0, 1, 2)
        b_box_layout.addWidget(self.addButton, 1, 0)
        b_box_layout.addWidget(self.delButton, 1, 1)
        button_box.setLayout(b_box_layout)
        self.layout.addWidget(button_box)
        #self.layout.addWidget(QLabel())
        #self.layout.addWidget(self.equipLabel)
        eq_box = QGroupBox("Zarządzanie ekwipunkiem")
        eq_box_layout = QVBoxLayout()
        eq_box_layout.addWidget(self.ekwipunek)
        eq_box.setLayout(eq_box_layout)
        self.layout.addWidget(eq_box)
        #self.layout.addWidget(self.ekwipunek)
        #self.layout.addWidget(QLabel())
        rank_box = QGroupBox("Zarządzanie rangami")
        rank_box_layout = QVBoxLayout()
        rank_box_layout.addWidget(self.rangi)
        rank_box.setLayout(rank_box_layout)
        self.layout.addWidget(rank_box)
        self.setLayout(self.layout)

        self.addButton.clicked.connect(self.create_unit)
        self.ekwipunek.clicked.connect(self.open_equipment)
        self.jednostki.cellDoubleClicked.connect(self.open_jednostki)
        self.delButton.clicked.connect(self.delete_items)

    def closeEvent(self, QCloseEvent):
        app.closeAllWindows()


main_window = MainWindow()
main_window.show()

app.exec_()
print("Finished execution")
Connector.close_connection()
