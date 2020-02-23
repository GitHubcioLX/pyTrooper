from PyQt5.QtWidgets import *

from Utilities import create_table
from AssignmentPreview import AssignmentPreview
from AssignmentForm import AssignmentForm
from DeletionConfirmation import DeletionConfirmation
from connector import Connector


class AssignManagement(QTabWidget):
    def __init__(self, id_jednostki):
        super().__init__()
        self.unit_id = id_jednostki
        self.setWindowTitle("Przydziały")
        self.setMinimumSize(400, 350)
        #self.listTab1 = None
        #self.refresh_eq_assignments()
        #self.listTab2 = None
        #self.refresh_vh_assignments()
        self.listTab1 = self.create_list_tab(["Od", "Do", "PESEL oficera", "Numer seryjny"],
                                             Connector.get_filtered('"Przydzial-ekwipunek"',
                                                                    ["data_od", "data_do", "pesel_oficera",
                                                                     "numer_seryjny"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id
                                                                    + " ORDER BY data_od DESC"),
                                             "ekwipunek")
        self.insertTab(0, self.listTab1, "Ekwipunek")
        self.listTab2 = self.create_list_tab(["Od", "Do", "PESEL oficera", "ID pojazdu"],
                                             Connector.get_filtered('"Przydzial-pojazd"', ["data_od", "data_do", "pesel_oficera", "id_pojazdu"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id
                                                                    + " ORDER BY data_od DESC"),
                                             "pojazdy")
        self.insertTab(1, self.listTab2, "Pojazdy")
        self.addWindow = None
        self.deleteWindow = None
        self.previewWindow = None
        self.setCurrentIndex(0)

    def refresh_eq_assignments(self):
        '''self.removeTab(0)
        self.listTab1 = self.create_list_tab(["Od", "Do", "PESEL oficera", "Numer seryjny"],
                                             Connector.get_filtered('"Przydzial-ekwipunek"', ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id
                                                                    + " ORDER BY data_od DESC"),
                                             "ekwipunek")
        self.insertTab(0, self.listTab1, "Ekwipunek")
        self.setCurrentIndex(0)'''
        if self.tabela_eq is not None:
            layout = self.listTab1.layout()
            layout.removeWidget(self.tabela_eq)
            self.tabela_eq = create_table(["Od", "Do", "PESEL oficera", "Numer seryjny"],
                                      Connector.get_filtered('"Przydzial-ekwipunek"', ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                                             " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id
                                                             + " ORDER BY data_od DESC"))
            self.tabela_eq.cellDoubleClicked.connect(self.eq_assignment_preview)
            layout.addWidget(self.tabela_eq, 0, 0, 1, 2)

    def refresh_vh_assignments(self):
        '''self.removeTab(1)
        self.listTab2 = self.create_list_tab(["Od", "Do", "PESEL oficera", "ID pojazdu"],
                                             Connector.get_filtered('"Przydzial-pojazd"', ["data_od", "data_do", "pesel_oficera", "id_pojazdu"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id
                                                                    + " ORDER BY data_od DESC"),
                                             "pojazdy")
        self.insertTab(1, self.listTab2, "Pojazdy")
        self.setCurrentIndex(1)'''
        if self.tabela_pojazdy is not None:
            layout = self.listTab2.layout()
            layout.removeWidget(self.tabela_pojazdy)
            self.tabela_pojazdy = create_table(["Od", "Do", "PESEL oficera", "ID pojazdu"],
                                             Connector.get_filtered('"Przydzial-pojazd"', ["data_od", "data_do", "pesel_oficera", "id_pojazdu"],
                                                                    " WHERE (SELECT id_jednostki FROM oficerowie WHERE pesel LIKE pesel_oficera) = " + self.unit_id
                                                                    + " ORDER BY data_od DESC"))
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vh_assignment_preview)
            layout.addWidget(self.tabela_pojazdy, 0, 0, 1, 2)

    def create_list_tab(self, column_names, items, type):
        tab = QWidget()
        layout = QGridLayout()

        tabela = create_table(column_names, items)
        layout.addWidget(tabela, 0, 0, 1, 2)

        #buttons = QGroupBox("Zarządzanie")
        #boxLayout = QHBoxLayout()
        addButton = QPushButton("Dodaj")
        rmvButton = QPushButton("Usuń")
        layout.addWidget(addButton, 1, 0)
        layout.addWidget(rmvButton, 1, 1)
        #boxLayout.addWidget(addButton)
        #boxLayout.addWidget(rmvButton)
        #buttons.setLayout(boxLayout)

        # addButton.clicked.connect(show_add_windows(type, id))
        if type == "ekwipunek":
            addButton.clicked.connect(self.add_eq_assignment)
            rmvButton.clicked.connect(self.delete_eq_assignments)
            self.tabela_eq = tabela
            self.tabela_eq.cellDoubleClicked.connect(self.eq_assignment_preview)
        if type == "pojazdy":
            addButton.clicked.connect(self.add_vh_assignment)
            rmvButton.clicked.connect(self.delete_vh_assignments)
            self.tabela_pojazdy = tabela
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vh_assignment_preview)

        #layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def add_eq_assignment(self):
        self.addWindow = AssignmentForm(self.unit_id, "ekwipunek")
        self.addWindow.commited.connect(self.refresh_eq_assignments)
        self.addWindow.show()

    def add_vh_assignment(self):
        self.addWindow = AssignmentForm(self.unit_id, "pojazd")
        self.addWindow.commited.connect(self.refresh_vh_assignments)
        self.addWindow.show()

    def delete_eq_assignments(self):
        self.deleteWindow = DeletionConfirmation()
        self.deleteWindow.selected.connect(self.delete_eq_assignment_slot)
        self.deleteWindow.show()

    def delete_eq_assignment_slot(self, answer):
        if answer:
            selection = self.tabela_eq.selectedItems()
            if selection:
                rows = []
                for x in selection:
                    rows.append(x.row())
                rows = list(dict.fromkeys(rows))
                res = []
                for x in rows:
                    res.append("'" + self.tabela_eq.item(x, 0).text() + "' AND pesel_oficera = '"
                               + self.tabela_eq.item(x, 2).text() + "' AND numer_seryjny = "
                               + self.tabela_eq.item(x, 3).text())
                Connector.delete_items('"Przydzial-ekwipunek"', res, "data_od", int)
                for x in rows:
                    Connector.update_row("ekwipunek", ["status"], ["Dostępny"], self.tabela_eq.item(x, 3).text(), "numer_seryjny", int)
                self.refresh_eq_assignments()

    def delete_vh_assignments(self):
        self.deleteWindow = DeletionConfirmation()
        self.deleteWindow.selected.connect(self.delete_vh_assignment_slot)
        self.deleteWindow.show()

    def delete_vh_assignment_slot(self, answer):
        if answer:
            selection = self.tabela_pojazdy.selectedItems()
            if selection:
                rows = []
                for x in selection:
                    rows.append(x.row())
                rows = list(dict.fromkeys(rows))
                res = []
                for x in rows:
                    res.append("'" + self.tabela_pojazdy.item(x, 0).text() + "' AND pesel_oficera = '"
                               + self.tabela_pojazdy.item(x, 2).text() + "' AND id_pojazdu = "
                               + self.tabela_pojazdy.item(x, 3).text())
                Connector.delete_items('"Przydzial-pojazd"', res, "data_od", int)
                for x in rows:
                    Connector.update_row("pojazdy", ["status"], ["Dostępny"], self.tabela_pojazdy.item(x, 3).text(), "id_pojazdu", int)
                self.refresh_vh_assignments()

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
