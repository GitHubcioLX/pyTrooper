import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


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
            temp[i] = QTableWidgetItem(str(item[i]))
            temp[i].setFlags(temp[i].flags() & ~Qt.ItemIsEditable)
            table.setItem(nr, i, temp[i])

    table.setHorizontalHeaderLabels(column_names)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    table.horizontalHeader().setStyleSheet("background-color: lightgray")
    table.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
    table.verticalHeader().setVisible(False)
    if column_names[0] == "ID":
        table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)

    return table
