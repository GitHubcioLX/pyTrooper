from PyQt5.QtWidgets import *

from Utilities import create_table
from AssignmentPreview import AssignmentPreview
from connector import Connector


class AssignManagement(QTabWidget):
    def __init__(self, id_jednostki):
        global budynki, oficerowie, pojazdy
        super().__init__()
        self.unit_id = id_jednostki
        self.setWindowTitle("Przydziały")
        self.setMinimumSize(400, 350)
        self.listTab1 = None
        self.refresh_eq_assignments()
        self.listTab2 = None
        self.refresh_vh_assignments()
        self.addWindow = None
        self.previewWindow = None
        self.setCurrentIndex(0)

    def refresh_eq_assignments(self):
        self.removeTab(0)
        self.listTab1 = self.create_list_tab(["Od", "Do", "PESEL oficera", "Numer seryjny"],
                                             Connector.get_filtered('"Przydzial-ekwipunek"', ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id),
                                             "ekwipunek")
        self.insertTab(0, self.listTab1, "Ekwipunek")
        self.setCurrentIndex(0)

    def refresh_vh_assignments(self):
        self.removeTab(1)
        self.listTab2 = self.create_list_tab(["Od", "Do", "PESEL oficera", "ID pojazdu"],
                                             Connector.get_filtered('"Przydzial-pojazd"', ["data_od", "data_do", "pesel_oficera", "id_pojazdu"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id),
                                             "pojazdy")
        self.insertTab(1, self.listTab2, "Pojazdy")
        self.setCurrentIndex(1)

    def create_list_tab(self, column_names, items, type):
        tab = QWidget()
        layout = QVBoxLayout()

        tabela = create_table(column_names, items)
        layout.addWidget(tabela)

        buttons = QGroupBox("Zarządzanie")
        boxLayout = QHBoxLayout()
        addButton = QPushButton("Dodaj")
        rmvButton = QPushButton("Usuń")
        boxLayout.addWidget(addButton)
        boxLayout.addWidget(rmvButton)
        buttons.setLayout(boxLayout)

        # addButton.clicked.connect(show_add_windows(type, id))
        if type == "ekwipunek":
            #addButton.clicked.connect(self.add_assignment)
            #rmvButton.clicked.connect(self.delete_assignments)
            self.tabela_eq = tabela
            self.tabela_eq.cellDoubleClicked.connect(self.eq_assignment_preview)
        if type == "pojazdy":
            #addButton.clicked.connect(self.add_assignment)
            #rmvButton.clicked.connect(self.delete_assignments)
            self.tabela_pojazdy = tabela
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vh_assignment_preview)

        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def add_assignment(self):
        self.addWindow = BuildingForm(self.unit_id)
        self.addWindow.commited.connect(self.refresh_buildings)
        self.addWindow.show()

    def delete_assignments(self):
        selection = self.tabela_budynki.selectedItems()
        if selection:
            res = []
            for x in selection:
                res.append(self.tabela_budynki.item(x.row(), 0).text())
            res = list(dict.fromkeys(res))
            Connector.delete_items("budynki", res, "oznaczenie", str)
            self.refresh_buildings()

    def eq_assignment_preview(self, rowid):
        data_od = self.tabela_eq.item(rowid, 0)
        pesel = self.tabela_eq.item(rowid, 2)
        nr_seryjny = self.tabela_eq.item(rowid, 3)
        self.previewWindow = AssignmentPreview("ekwipunek", data_od.text(), pesel.text(), nr_seryjny.text())
        self.previewWindow.show()

    def vh_assignment_preview(self, rowid):
        data_od = self.tabela_pojazdy.item(rowid, 0)
        pesel = self.tabela_pojazdy.item(rowid, 2)
        id_pojazdu = self.tabela_pojazdy.item(rowid, 3)
        self.previewWindow = AssignmentPreview("pojazd", data_od.text(), pesel.text(), id_pojazdu.text())
        self.previewWindow.show()


if __name__ == "__main__":
    app = QApplication([])
    window = AssignManagement("1")
    window.show()
    app.exec_()
