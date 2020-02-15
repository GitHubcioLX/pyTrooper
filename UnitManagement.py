import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

# GUI
app = QApplication([])
#text_area = QPlainTextEdit()
#text_area.setFocusPolicy(Qt.NoFocus)

budynki = [["Budynek 1"], ["Budynek 2"], ["Budynek 3"], ["Budynek 4"], ["Budynek 5"]]
oficerowie = [["Stasiek", "Dupas", "9450245291"], ["Krzysiek", "Kasztan", "9150258790"], ["Wiechu", "Szachista", "5540235263"]]
pojazdy = [["1", "Maluch"], ["2", "BMW"], ["3", "Silvia"], ["4", "Corolla"], ["5", "Rudy"], ["6", "Jagdpanzer"], ["7", "Rower"], ["8", "Turbosmiglowiec"]]


def set_info_tab(id_jednostki):
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
    zamowienia = QPushButton("Zamówienia")
    buttonsLayout.addWidget(przydzialy)
    buttonsLayout.addWidget(zamowienia)
    buttons.setLayout(buttonsLayout)
    layout.addWidget(buttons)
    tab.setLayout(layout)
    return tab


def create_list_tab(column_names, items):
    tab = QWidget()
    layout = QVBoxLayout()

    tabela = create_table(column_names, items)
    #lista = QListWidget()
    #for item in items:
    #    lista.addItem(item)
    #layout.addWidget(lista)
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

    layout.addWidget(buttons)
    tab.setLayout(layout)
    return tab


def create_table(column_names, items):
    n_columns = len(column_names)

    table = QTableWidget()
    table.setRowCount(len(items))
    table.setColumnCount(n_columns)

    temp = []
    for i in range(n_columns):
        temp.append("")

    for nr, item in enumerate(items):
        for i in range(n_columns):
            temp[i] = QTableWidgetItem(item[i])
            temp[i].setFlags(temp[i].flags() & ~Qt.ItemIsEditable)
            table.setItem(nr, i, temp[i])

    table.setHorizontalHeaderLabels(column_names)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.horizontalHeader().setStyleSheet("color: blue")
    table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    table.verticalHeader().setVisible(False)
    if column_names[0] == "ID":
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    return table


class UnitManagement(QTabWidget):
    def __init__(self, id_jednostki):
        global budynki, oficerowie, pojazdy
        super().__init__()
        self.infoTab = set_info_tab(id_jednostki)
        self.listTab1 = create_list_tab(["Oznaczenie"], budynki)
        self.listTab2 = create_list_tab(["ID", "Model"], pojazdy)
        self.listTab3 = create_list_tab(["Imię", "Nazwisko", "PESEL"], oficerowie)
        self.addTab(self.infoTab, "Ogólne")
        self.addTab(self.listTab1, "Budynki")
        self.addTab(self.listTab2, "Pojazdy")
        self.addTab(self.listTab3, "Oficerowie")

    def set_layout(self):
        self.layout.addWidget(self.naglowek)
        self.layout.addWidget(self.jednostki)
        self.layout.addWidget(self.gap)
        self.layout.addWidget(self.ekwipunek)
        self.layout.addWidget(self.gap)
        self.setLayout(self.layout)


'''main_window = UnitManagement("420")
main_window.show()

app.exec_()'''
