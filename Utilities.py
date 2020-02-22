import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from connector import Connector
from BuildingForm import BuildingForm
from config import formatter, column_names

create_view = None


'''def show_add_windows(type, id):
    types = {
        "budynki": lambda x: BuildingForm(x)
    }
    create_view = types.get(type)(id)
    create_view.show()'''


def create_info_box(tablename, id, idname, idtype, columns=None):
    box = QGroupBox("Informacje")
    layout = QFormLayout()
    if columns is not None:
        data = Connector.get_dict(tablename, columns, id, idname, idtype)
    else:
        data = Connector.get_dict(tablename, column_names[tablename], id, idname, idtype)
        if tablename == "pojazdy" and data["status"] == "Zamówiony":
            ex_columns = ["rodzaj", "producent", "model", "rok_produkcji", "masa", "liczba_zalogi", "zasieg",
                          "rejestracja", "id_jednostki", "status", "id_zamowienia"]
            data = Connector.get_dict(tablename, ex_columns, id, idname, idtype)
        if tablename == "ekwipunek" and data["status"] == "Zamówiony":
            ex_columns = ["typ", "producent", "model", "numer_seryjny", "data_produkcji", "data_waznosci", "status",
                          "id_zamowienia"]
            data = Connector.get_dict(tablename, ex_columns, id, idname, idtype)
    font = QFont()
    font.setBold(True)
    for k, v in data.items():
        if v is None:
            label = QLabel(str("-"))
        else:
            label = QLabel(str(v))
        label.setFont(font)
        layout.addRow(formatter[k] + ": ", label)
    box.setLayout(layout)
    return box


def set_info_tab(id_jednostki):
    tab = QWidget()
    layout = QVBoxLayout()
    info = create_info_box("jednostki", id_jednostki, "identyfikator", int)
    '''info = QGroupBox("Informacje")
    infoLayout = QFormLayout()

    unit_data = Connector.get_record("jednostki", None, id_jednostki, "identyfikator", int)

    infoLayout.addRow("Identyfikator: ", QLabel(id_jednostki))
    infoLayout.addRow("Nazwa: ", QLabel(unit_data[1]))
    infoLayout.addRow("Miasto: ", QLabel(unit_data[3]))
    infoLayout.addRow("Rodzaj: ", QLabel(unit_data[2]))
    info.setLayout(infoLayout)'''
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


label_to_collumn = {
    "UnitForm": {
        "Identyfikator: ": "identyfikator",
        "Nazwa: ": "nazwa",
        "Rodzaj: ": "rodzaj",
        "Miasto: ": "miasto"
    }
}
