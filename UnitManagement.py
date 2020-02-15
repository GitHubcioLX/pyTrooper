import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# GUI
app = QApplication([])
#text_area = QPlainTextEdit()
#text_area.setFocusPolicy(Qt.NoFocus)

budynki = ["Budynek 1", "Budynek 2", "Budynek 3", "Budynek 4", "Budynek 5"]
oficerowie = ["Stasiek", "Krzysiek", "Zdzisiek", "Siurek", "Kasztan", "Krakowiaczek", "Wieniu", "Andrzej"]
pojazdy = ["Maluch", "BMW", "Silvia", "Corolla", "Rudy", "Jagdpanzer", "Rower", "Skuter", "Sterowiec", "Turbosmiglowiec"]

class UnitManagement(QTabWidget):
    def __init__(self, id_jednostki):
        global budynki, oficerowie, pojazdy
        super().__init__()
        self.infoTab = self.set_info_tab(id_jednostki)
        self.listTab1 = self.create_list_tab(budynki)
        self.listTab2 = self.create_list_tab(pojazdy)
        self.listTab3 = self.create_list_tab(oficerowie)
        self.addTab(self.infoTab, "Ogólne")
        self.addTab(self.listTab1, "Budynki")
        self.addTab(self.listTab2, "Pojazdy")
        self.addTab(self.listTab3, "Oficerowie")

    def set_info_tab(self, id_jednostki):
        tab = QWidget()
        layout = QVBoxLayout()
        info = QGroupBox("Informacje")
        infoLayout = QFormLayout()
        infoLayout.addRow("Identyfikator: ", QLabel(id_jednostki))
        infoLayout.addRow("Nazwa: ", QLabel("Jednostka Testowa Jebanej Piechoty Miejskiej"))
        infoLayout.addRow("Miasto: ", QLabel("Poznan"))
        infoLayout.addRow("Rodzaj: ", QLabel("Pizdowata masa"))
        info.setLayout(infoLayout)
        layout.addWidget(info)

        buttons = QGroupBox("Zarządzanie")
        buttonsLayout = QHBoxLayout()
        przydzialy = QPushButton("Przydziały")
        zamowienia = QPushButton("Zamowienia")
        buttonsLayout.addWidget(przydzialy)
        buttonsLayout.addWidget(zamowienia)
        buttons.setLayout(buttonsLayout)
        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def create_list_tab(self, items):
        tab = QWidget()
        layout = QVBoxLayout()

        lista = QListWidget()
        for item in items:
            lista.addItem(item)
        layout.addWidget(lista)

        buttons = QGroupBox("Zarządzanie")
        boxLayout = QHBoxLayout()
        addButton = QPushButton("Dodaj")
        rmvButton = QPushButton("Usuń")
        editButton = QPushButton("Edytuj")
        boxLayout.addWidget(addButton)
        boxLayout.addWidget(rmvButton)
        boxLayout.addWidget(editButton)
        buttons.setLayout(boxLayout)

        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def set_layout(self):
        self.layout.addWidget(self.naglowek)
        self.layout.addWidget(self.jednostki)
        self.layout.addWidget(self.gap)
        self.layout.addWidget(self.ekwipunek)
        self.layout.addWidget(self.gap)
        self.setLayout(self.layout)


main_window = UnitManagement("420")
main_window.show()

app.exec_()
