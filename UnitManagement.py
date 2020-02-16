import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Utilities import set_info_tab, create_table
from connector import Connector
from BuildingForm import BuildingForm

# GUI
# app = QApplication([])

budynki = [["AB3", "Wychodek"], ["DG2", "Toaleta"], ["BG7", "Urynał"], ["QV1", "Ubikacja"], ["HU1", "Kibel"]]
oficerowie = [["Stasiek", "Dupas", "9450245291"], ["Krzysiek", "Kasztan", "9150258790"], ["Wiechu", "Szachista", "5540235263"]]
pojazdy = [["1", "Maluch"], ["2", "BMW"], ["3", "Silvia"], ["4", "Corolla"], ["5", "Rudy"], ["6", "Jagdpanzer"], ["7", "Rower"], ["8", "Turbosmiglowiec"]]


class UnitManagement(QTabWidget):
    def __init__(self, id_jednostki):
        global budynki, oficerowie, pojazdy
        super().__init__()
        self.unit_id = id_jednostki
        self.setWindowTitle("Zarządzanie jednostką")
        self.setMinimumSize(400, 350)
        self.infoTab = set_info_tab(id_jednostki)
        self.listTab1 = self.create_list_tab(["Oznaczenie", "Rola"], Connector.get_filtered("budynki", ["oznaczenie", "rola_budynku"], " WHERE id_jednostki = " + id_jednostki), "budynki")
        self.listTab2 = self.create_list_tab(["ID", "Model"], Connector.get_filtered("pojazdy", ["id_pojazdu", "model"], " WHERE id_jednostki = " + id_jednostki), "pojazdy")
        self.listTab3 = self.create_list_tab(["Imię", "Nazwisko", "PESEL"], Connector.get_filtered("oficerowie", ["imie", "nazwisko", "pesel"], " WHERE id_jednostki = " + id_jednostki), "oficerowie")
        self.addTab(self.infoTab, "Ogólne")
        self.addTab(self.listTab1, "Budynki")
        self.addTab(self.listTab2, "Pojazdy")
        self.addTab(self.listTab3, "Oficerowie")
        self.addWindow = None

    def create_list_tab(self, column_names, items, type):
        tab = QWidget()
        layout = QVBoxLayout()

        tabela = create_table(column_names, items)
        # lista = QListWidget()
        # for item in items:
        #    lista.addItem(item)
        # layout.addWidget(lista)
        layout.addWidget(tabela)

        buttons = QGroupBox("Zarządzanie")
        boxLayout = QHBoxLayout()
        addButton = QPushButton("Dodaj")
        rmvButton = QPushButton("Usuń")
        editButton = QPushButton("Edytuj")
        boxLayout.addWidget(addButton)
        boxLayout.addWidget(rmvButton)
        boxLayout.addWidget(editButton)
        buttons.setLayout(boxLayout)

        #addButton.clicked.connect(show_add_windows(type, id))
        if type == "budynki":
            addButton.clicked.connect(self.add_building)

        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def add_building(self):
        self.addWindow = BuildingForm(self.unit_id)
        self.addWindow.show()


'''main_window = UnitManagement("420")
main_window.show()

app.exec_()'''
