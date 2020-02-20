from PyQt5.QtWidgets import *

from Utilities import set_info_tab, create_table
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
        #self.listTab2 = None
        #self.refresh_vh_assignments()
        self.addWindow = None
        self.previewWindow = None
        self.setCurrentIndex(0)

    def refresh_eq_assignments(self):
        self.removeTab(0)
        self.listTab1 = self.create_list_tab(["Od", "Do", "PESEL oficera", "Numer seryjny"],
                                             Connector.get_filtered("Przydzial-ekwipunek", ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id),
                                             "ekwipunek")
        self.insertTab(1, self.listTab1, "Ekwipunek")
        self.setCurrentIndex(0)

    def refresh_vh_assignments(self):
        self.removeTab(1)
        self.listTab2 = self.create_list_tab(["Od", "Do", "PESEL oficera", "ID pojazdu"],
                                             Connector.get_filtered("public.\"Przydzial-ekwipunek\"", ["data_od", "data_do", "pesel_oficera", "id_pojazdu"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id),
                                             "pojazdy")
        self.insertTab(1, self.listTab1, "Pojazdy")
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
        editButton = QPushButton("Edytuj")
        boxLayout.addWidget(addButton)
        boxLayout.addWidget(rmvButton)
        boxLayout.addWidget(editButton)
        buttons.setLayout(boxLayout)

        # addButton.clicked.connect(show_add_windows(type, id))
        if type == "ekwipunek":
            addButton.clicked.connect(self.add_building)
            rmvButton.clicked.connect(self.delete_buildings)
            editButton.clicked.connect(self.edit_building)
            self.tabela_budynki = tabela
            self.tabela_budynki.cellDoubleClicked.connect(self.building_preview)
        if type == "pojazdy":
            addButton.clicked.connect(self.add_vehicle)
            rmvButton.clicked.connect(self.delete_vehicles)
            editButton.clicked.connect(self.edit_vehicle)
            self.tabela_pojazdy = tabela
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vehicle_preview)

        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def add_assignment(self):
        self.addWindow = BuildingForm(self.unit_id)
        self.addWindow.commited.connect(self.refresh_buildings)
        self.addWindow.show()

    def edit_assignment(self):
        selection = self.tabela_budynki.selectedItems()
        if len(selection) == 1:
            id = self.tabela_budynki.item(selection[0].row(), 0).text()
            self.addWindow = BuildingForm(self.unit_id, id)
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

    def assignment_preview(self, rowid):
        item = self.tabela_budynki.item(rowid, 0)
        self.previewWindow = BuildingPreview(item.text())
        self.previewWindow.show()


if __name__ == "__main__":
    app = QApplication([])
    window = AssignManagement("1")
    window.show()
    app.exec_()
