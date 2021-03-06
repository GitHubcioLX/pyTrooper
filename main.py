import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EquipmentListWindow import EquipmentListWindow
from UnitManagement import UnitManagement
from DeletionConfirmation import DeletionConfirmation
from connector import Connector
from Utilities import create_table
from UnitForm import UnitForm
from RankManagement import RankManagement
from config import rx

# GUI
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
app = QApplication([])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.filter = QLineEdit()
        self.filter.setValidator(QRegExpValidator(QRegExp(rx)))
        self.filter.setPlaceholderText("Wyszukaj nazwę...")
        #self.filter.textEdited.connect(self.set_jednostki)
        self.filter.returnPressed.connect(self.set_jednostki)

        self.jednostki = QTableWidget()

        self.addButton = QPushButton("Dodaj")
        self.delButton = QPushButton("Usuń")

        self.ekwipunek = QPushButton("Ekwipunek wojska")
        self.rangi = QPushButton("Rangi")

        self.layout = QVBoxLayout()

        self.setWindowTitle("Menu główne")
        self.setMinimumSize(480, 500)
        self.unit_box = None
        self.unit_box_layout = None
        self.set_jednostki()
        self.set_layout()

        self.unitwindow = None
        self.unitcreation = None
        self.deleteWindow = None
        self.equipment_window = EquipmentListWindow()
        self.rankWindow = RankManagement()

    def create_unit(self):
        self.unitcreation = UnitForm(self)
        self.unitcreation.show()

    def open_equipment(self):
        self.equipment_window.show()

    def set_jednostki(self):
        self.jednostki = create_table(['Identyfikator', 'Nazwa'],
                                      Connector.get_filtered("jednostki", ["identyfikator", "nazwa"],
                                                             " WHERE UPPER(nazwa) LIKE UPPER('%" + self.filter.text() +
                                                             "%')" + " ORDER BY identyfikator ASC"))
        self.refresh_unit_box()

    def open_jednostki(self, rowid):
        item = self.jednostki.item(rowid, 0)
        self.unitwindow = UnitManagement(item.text())
        self.unitwindow.show()

    def open_rangi(self):
        self.rankWindow.show()

    def delete_items(self):
        self.deleteWindow = DeletionConfirmation("jednostki")
        self.deleteWindow.selected.connect(self.delete_items_slot)
        self.deleteWindow.show()

    def delete_items_slot(self, answer):
        if answer:
            selection = self.jednostki.selectedItems()
            if selection:
                res = []
                for x in selection:
                    res.append(self.jednostki.item(x.row(), 0).text())
                res = list(dict.fromkeys(res))
                Connector.delete_items("jednostki", res, "identyfikator", int)
                self.set_jednostki()

    def refresh_unit_box(self):
        if self.unit_box_layout:
            while self.unit_box_layout.itemAt(0):
                self.unit_box_layout.removeItem(self.unit_box_layout.itemAt(0))
            self.unit_box_layout.addWidget(self.jednostki, 0, 0, 1, 2)
            self.unit_box_layout.addWidget(self.filter, 1, 0, 1, 2)
            self.unit_box_layout.addWidget(self.addButton, 2, 0)
            self.unit_box_layout.addWidget(self.delButton, 2, 1)
            self.unit_box.setLayout(self.unit_box_layout)
            self.jednostki.cellDoubleClicked.connect(self.open_jednostki)

    def set_layout(self):
        #self.layout.addWidget(self.naglowek)
        #self.layout.addWidget(self.jednostki)
        self.unit_box = QGroupBox("Zarządzanie jednostkami")
        self.unit_box_layout = QGridLayout()
        self.unit_box_layout.addWidget(self.jednostki, 0, 0, 1, 2)
        self.unit_box_layout.addWidget(self.filter, 1, 0, 1, 2)
        self.unit_box_layout.addWidget(self.addButton, 2, 0)
        self.unit_box_layout.addWidget(self.delButton, 2, 1)
        self.unit_box.setLayout(self.unit_box_layout)
        self.layout.addWidget(self.unit_box)
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
        self.rangi.clicked.connect(self.open_rangi)

    def closeEvent(self, QCloseEvent):
        app.closeAllWindows()


main_window = MainWindow()
main_window.show()

app.exec_()
print("Finished execution")
Connector.close_connection()
