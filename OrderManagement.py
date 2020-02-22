from PyQt5.QtWidgets import *

from Utilities import create_table
from OrderPreview import OrderPreview
from OrderForm import OrderForm
from DeletionConfirmation import DeletionConfirmation
from connector import Connector


class OrderManagement(QTabWidget):
    def __init__(self, id_jednostki):
        super().__init__()
        self.unit_id = id_jednostki
        self.setWindowTitle("Zamówienia")
        self.setMinimumSize(400, 350)
        self.listTab1 = None
        self.refresh_eq_orders()
        self.listTab2 = None
        self.refresh_vh_orders()
        self.addWindow = None
        self.deleteWindow = None
        self.previewWindow = None
        self.setCurrentIndex(0)

    def refresh_eq_orders(self):
        self.removeTab(0)
        self.listTab1 = self.create_list_tab(["ID zamówienia", "Data złożenia", "Koszt"],
                                             Connector.get_filtered('"Zamowienie-ekwipunek"', ["id_zamowienia", "data_zam", "koszt"],
                                                                    " ORDER BY id_zamowienia ASC"),
                                             "ekwipunek")
        self.insertTab(0, self.listTab1, "Ekwipunek")
        self.setCurrentIndex(0)

    def refresh_vh_orders(self):
        self.removeTab(1)
        self.listTab2 = self.create_list_tab(["ID zamówienia", "Data złożenia", "Koszt"],
                                             Connector.get_filtered('"Zamowienie-pojazd"', ["id_zamowienia", "data_zam", "koszt"],
                                                                    " WHERE (SELECT p.id_jednostki FROM pojazdy p WHERE p.id_zamowienia = id_zamowienia) = " + self.unit_id
                                                                    + " ORDER BY id_zamowienia ASC"),
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
        rmvButton = QPushButton("Anuluj")
        finishButton = QPushButton("Zakończ")
        boxLayout.addWidget(addButton)
        boxLayout.addWidget(rmvButton)
        boxLayout.addWidget(finishButton)
        buttons.setLayout(boxLayout)

        # addButton.clicked.connect(show_add_windows(type, id))
        if type == "ekwipunek":
            addButton.clicked.connect(self.add_eq_order)
            #rmvButton.clicked.connect(self.delete_eq_assignments)
            self.tabela_eq = tabela
            self.tabela_eq.cellDoubleClicked.connect(self.eq_order_preview)
        if type == "pojazdy":
            addButton.clicked.connect(self.add_vh_order)
            #rmvButton.clicked.connect(self.delete_vh_assignments)
            self.tabela_pojazdy = tabela
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vh_order_preview)

        layout.addWidget(buttons)
        tab.setLayout(layout)
        return tab

    def add_eq_order(self):
        print(1)
        self.addWindow = OrderForm(self.unit_id, "ekwipunek")
        print(2)
        self.addWindow.commited.connect(self.refresh_eq_orders)
        print(3)
        self.addWindow.show()

    def add_vh_order(self):
        self.addWindow = OrderForm(self.unit_id, "pojazd")
        self.addWindow.commited.connect(self.refresh_vh_orders)
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

    def eq_order_preview(self, rowid):
        id_zamowienia = self.tabela_eq.item(rowid, 0)
        self.previewWindow = OrderPreview("ekwipunek", id_zamowienia.text())
        self.previewWindow.show()

    def vh_order_preview(self, rowid):
        id_zamowienia = self.tabela_pojazdy.item(rowid, 0)
        self.previewWindow = OrderPreview("pojazd", id_zamowienia.text())
        self.previewWindow.show()


if __name__ == "__main__":
    app = QApplication([])
    window = OrderManagement("1")
    window.show()
    app.exec_()
