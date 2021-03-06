from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from BuildingForm import BuildingForm
from BuildingPreview import BuildingPreview
from DeletionConfirmation import DeletionConfirmation
from OfficerForm import OfficerForm
from OfficerPreview import OfficerPreview
from Utilities import create_table, create_info_box
from VehicleForm import VehicleForm
from VehiclePreview import VehiclePreview
from AssignManagement import AssignManagement
from OrderManagement import OrderManagement
from config import rx
from connector import Connector


class UnitManagement(QTabWidget):
    def __init__(self, id_jednostki):
        super().__init__()
        self.unit_id = id_jednostki
        self.setWindowTitle("Zarządzanie jednostką")
        self.setMinimumSize(400, 350)
        self.infoTab = self.set_info_tab()
        self.insertTab(0, self.infoTab, "Ogólne")
        self.initiation = True
        self.listTab1 = None
        self.filter_budynki = QLineEdit()
        #self.refresh_buildings()
        self.listTab2 = None
        self.filter_pojazdy = QLineEdit()
        #self.refresh_vehicles()
        self.listTab3 = None
        self.filter_oficerowie = QLineEdit()
        #self.refresh_officers()
        self.create_tabs()
        self.initiation = False
        self.addWindow = None
        self.previewWindow = None
        self.deleteWindow = None
        self.assignmentWindow = None
        self.ordersWindow = None
        self.setCurrentIndex(0)

    def create_tabs(self):
        self.listTab1 = self.create_list_tab(["Oznaczenie", "Rola"],
                                             Connector.get_filtered("budynki", ["oznaczenie", "rola_budynku"],
                                                                    " WHERE id_jednostki = " + self.unit_id +
                                                                    " AND (UPPER(oznaczenie) LIKE UPPER('%" +
                                                                    self.filter_budynki.text() + "%')" +
                                                                    " OR UPPER(rola_budynku) LIKE UPPER('%" +
                                                                    self.filter_budynki.text() + "%'))" +
                                                                    " ORDER BY oznaczenie ASC"),
                                             "budynki")
        self.insertTab(1, self.listTab1, "Budynki")
        self.listTab2 = self.create_list_tab(["ID", "Producent", "Model"],
                                             Connector.get_filtered("pojazdy", ["id_pojazdu", "producent", "model"],
                                                                    " WHERE id_jednostki = " + self.unit_id +
                                                                    " AND (UPPER(model) LIKE UPPER('%" +
                                                                    self.filter_pojazdy.text() + "%')" +
                                                                    " OR UPPER(producent) LIKE UPPER('%" +
                                                                    self.filter_pojazdy.text() + "%'))" +
                                                                    " ORDER BY id_pojazdu ASC"),
                                             "pojazdy")
        self.insertTab(2, self.listTab2, "Pojazdy")
        self.listTab3 = self.create_list_tab(["Imię", "Nazwisko", "PESEL"],
                                             Connector.get_filtered("oficerowie", ["imie", "nazwisko", "pesel"],
                                                                    " WHERE id_jednostki = " + self.unit_id +
                                                                    " AND (UPPER(imie) LIKE UPPER('%" +
                                                                    self.filter_oficerowie.text() + "%')" +
                                                                    " OR UPPER(nazwisko) LIKE UPPER('%" +
                                                                    self.filter_oficerowie.text() + "%')" +
                                                                    " OR UPPER(pesel) LIKE UPPER('%" +
                                                                    self.filter_oficerowie.text() + "%'))" +
                                                                    " ORDER BY nazwisko, imie ASC"),
                                             "oficerowie")
        self.insertTab(3, self.listTab3, "Oficerowie")


    def refresh_buildings(self):
        '''self.removeTab(1)
        self.listTab1 = self.create_list_tab(["Oznaczenie", "Rola"],
                                             Connector.get_filtered("budynki", ["oznaczenie", "rola_budynku"],
                                                                    " WHERE id_jednostki = " + self.unit_id +
                                                                    " AND (UPPER(oznaczenie) LIKE UPPER('%" +
                                                                    self.filter_budynki.text() + "%')" +
                                                                    " OR UPPER(rola_budynku) LIKE UPPER('%" +
                                                                    self.filter_budynki.text() + "%'))" +
                                                                    " ORDER BY oznaczenie ASC"),
                                             "budynki")
        self.insertTab(1, self.listTab1, "Budynki")
        self.setCurrentIndex(1)'''
        if self.tabela_budynki is not None:
            layout = self.listTab1.layout()
            layout.removeWidget(self.tabela_budynki)
            self.tabela_budynki = create_table(["Oznaczenie", "Rola"],
                                               Connector.get_filtered("budynki", ["oznaczenie", "rola_budynku"],
                                                                      " WHERE id_jednostki = " + self.unit_id +
                                                                      " AND (UPPER(oznaczenie) LIKE UPPER('%" +
                                                                      self.filter_budynki.text() + "%')" +
                                                                      " OR UPPER(rola_budynku) LIKE UPPER('%" +
                                                                      self.filter_budynki.text() + "%'))" +
                                                                      " ORDER BY oznaczenie ASC"))
            self.tabela_budynki.cellDoubleClicked.connect(self.building_preview)
            layout.addWidget(self.tabela_budynki, 0, 0, 1, 3)
        if not self.initiation:
            self.refresh_c_box()

    def refresh_vehicles(self):
        '''self.removeTab(2)
        self.listTab2 = self.create_list_tab(["ID", "Producent", "Model"],
                                             Connector.get_filtered("pojazdy", ["id_pojazdu", "producent", "model"],
                                                                    " WHERE id_jednostki = " + self.unit_id +
                                                                    " AND (UPPER(model) LIKE UPPER('%" +
                                                                    self.filter_pojazdy.text() + "%')" +
                                                                    " OR UPPER(producent) LIKE UPPER('%" +
                                                                    self.filter_pojazdy.text() + "%'))" +
                                                                    " ORDER BY id_pojazdu ASC"),
                                             "pojazdy")
        self.insertTab(2, self.listTab2, "Pojazdy")
        self.setCurrentIndex(2)'''
        if self.tabela_pojazdy is not None:
            layout = self.listTab2.layout()
            layout.removeWidget(self.tabela_pojazdy)
            self.tabela_pojazdy = create_table(["ID", "Producent", "Model"],
                                               Connector.get_filtered("pojazdy", ["id_pojazdu", "producent", "model"],
                                                                      " WHERE id_jednostki = " + self.unit_id +
                                                                      " AND (UPPER(model) LIKE UPPER('%" +
                                                                      self.filter_pojazdy.text() + "%')" +
                                                                      " OR UPPER(producent) LIKE UPPER('%" +
                                                                      self.filter_pojazdy.text() + "%'))" +
                                                                      " ORDER BY id_pojazdu ASC"))
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vehicle_preview)
            layout.addWidget(self.tabela_pojazdy, 0, 0, 1, 3)
        if not self.initiation:
            self.refresh_c_box()

    def refresh_officers(self):
        '''self.removeTab(3)
        self.listTab3 = self.create_list_tab(["Imię", "Nazwisko", "PESEL"],
                                             Connector.get_filtered("oficerowie", ["imie", "nazwisko", "pesel"],
                                                                    " WHERE id_jednostki = " + self.unit_id +
                                                                    " AND (UPPER(imie) LIKE UPPER('%" +
                                                                    self.filter_oficerowie.text() + "%')" +
                                                                    " OR UPPER(nazwisko) LIKE UPPER('%" +
                                                                    self.filter_oficerowie.text() + "%')" +
                                                                    " OR UPPER(pesel) LIKE UPPER('%" +
                                                                    self.filter_oficerowie.text() + "%'))" +
                                                                    " ORDER BY nazwisko, imie ASC"),
                                             "oficerowie")
        self.insertTab(3, self.listTab3, "Oficerowie")
        self.setCurrentIndex(3)'''
        if self.tabela_oficerowie is not None:
            layout = self.listTab3.layout()
            layout.removeWidget(self.tabela_oficerowie)
            self.tabela_oficerowie = create_table(["Imię", "Nazwisko", "PESEL"],
                                                  Connector.get_filtered("oficerowie", ["imie", "nazwisko", "pesel"],
                                                                         " WHERE id_jednostki = " + self.unit_id +
                                                                         " AND (UPPER(imie) LIKE UPPER('%" +
                                                                         self.filter_oficerowie.text() + "%')" +
                                                                         " OR UPPER(nazwisko) LIKE UPPER('%" +
                                                                         self.filter_oficerowie.text() + "%')" +
                                                                         " OR UPPER(pesel) LIKE UPPER('%" +
                                                                         self.filter_oficerowie.text() + "%'))" +
                                                                         " ORDER BY nazwisko, imie ASC"))
            self.tabela_oficerowie.cellDoubleClicked.connect(self.officer_preview)
            layout.addWidget(self.tabela_oficerowie, 0, 0, 1, 3)
        if not self.initiation:
            self.refresh_c_box()

    def create_list_tab(self, column_names, items, type):
        tab = QWidget()
        #layout = QVBoxLayout()
        layout = QGridLayout()
        tabela = create_table(column_names, items)
        layout.addWidget(tabela, 0, 0, 1, 3)

        filter = QLineEdit()
        filter.setValidator(QRegExpValidator(QRegExp(rx)))
        filter.setPlaceholderText("Wyszukaj...")

        #buttons = QGroupBox("Zarządzanie")
        #boxLayout = QHBoxLayout()
        addButton = QPushButton("Dodaj")
        rmvButton = QPushButton("Usuń")
        editButton = QPushButton("Edytuj")
        #boxLayout.addWidget(addButton)
        #boxLayout.addWidget(rmvButton)
        #boxLayout.addWidget(editButton)
        #buttons.setLayout(boxLayout)

        # addButton.clicked.connect(show_add_windows(type, id))
        if type == "budynki":
            addButton.clicked.connect(self.add_building)
            rmvButton.clicked.connect(self.delete_buildings)
            editButton.clicked.connect(self.edit_building)
            self.filter_budynki = filter
            self.filter_budynki.returnPressed.connect(self.refresh_buildings)
            layout.addWidget(self.filter_budynki, 1, 0, 1, 3)
            self.tabela_budynki = tabela
            self.tabela_budynki.cellDoubleClicked.connect(self.building_preview)
        if type == "pojazdy":
            addButton.clicked.connect(self.add_vehicle)
            rmvButton.clicked.connect(self.delete_vehicles)
            editButton.clicked.connect(self.edit_vehicle)
            self.filter_pojazdy = filter
            self.filter_pojazdy.returnPressed.connect(self.refresh_vehicles)
            layout.addWidget(self.filter_pojazdy, 1, 0, 1, 3)
            self.tabela_pojazdy = tabela
            self.tabela_pojazdy.cellDoubleClicked.connect(self.vehicle_preview)
        if type == "oficerowie":
            addButton.clicked.connect(self.add_officer)
            rmvButton.clicked.connect(self.delete_officers)
            editButton.clicked.connect(self.edit_officer)
            self.filter_oficerowie = filter
            self.filter_oficerowie.returnPressed.connect(self.refresh_officers)
            layout.addWidget(self.filter_oficerowie, 1, 0, 1, 3)
            self.tabela_oficerowie = tabela
            self.tabela_oficerowie.cellDoubleClicked.connect(self.officer_preview)

        #layout.addWidget(buttons)
        layout.addWidget(addButton, 2, 0)
        layout.addWidget(rmvButton, 2, 1)
        layout.addWidget(editButton, 2, 2)
        tab.setLayout(layout)
        return tab

    def add_building(self):
        self.addWindow = BuildingForm(self.unit_id)
        self.addWindow.commited.connect(self.refresh_buildings)
        self.addWindow.show()

    def add_vehicle(self):
        self.addWindow = VehicleForm(self.unit_id, "Dostępny")
        self.addWindow.commited.connect(self.refresh_vehicles)
        self.addWindow.show()

    def add_officer(self):
        self.addWindow = OfficerForm(self.unit_id)
        self.addWindow.commited.connect(self.refresh_officers)
        self.addWindow.show()

    def edit_building(self):
        selection = self.tabela_budynki.selectedItems()
        res = []
        for x in selection:
            res.append(self.tabela_budynki.item(x.row(), 0).text())
        res = list(dict.fromkeys(res))
        if len(res) == 1:
            id = self.tabela_budynki.item(selection[0].row(), 0).text()
            self.addWindow = BuildingForm(self.unit_id, id)
            self.addWindow.commited.connect(self.refresh_buildings)
            self.addWindow.show()

    def edit_vehicle(self):
        selection = self.tabela_pojazdy.selectedItems()
        res = []
        for x in selection:
            res.append(self.tabela_pojazdy.item(x.row(), 0).text())
        res = list(dict.fromkeys(res))
        if len(res) == 1:
            id = self.tabela_pojazdy.item(selection[0].row(), 0).text()
            self.addWindow = VehicleForm(self.unit_id, None, id)
            self.addWindow.commited.connect(self.refresh_vehicles)
            self.addWindow.show()

    def edit_officer(self):
        selection = self.tabela_oficerowie.selectedItems()
        res = []
        for x in selection:
            res.append(self.tabela_oficerowie.item(x.row(), 0).text())
        res = list(dict.fromkeys(res))
        if len(res) == 1:
            pesel = self.tabela_oficerowie.item(selection[0].row(), 2).text()
            self.addWindow = OfficerForm(self.unit_id, pesel)
            self.addWindow.commited.connect(self.refresh_officers)
            self.addWindow.show()

    def delete_buildings(self):
        self.deleteWindow = DeletionConfirmation("budynki")
        self.deleteWindow.selected.connect(self.delete_building_slot)
        self.deleteWindow.show()

    def delete_building_slot(self, answer):
        if answer:
            selection = self.tabela_budynki.selectedItems()
            if selection:
                res = []
                for x in selection:
                    res.append(self.tabela_budynki.item(x.row(), 0).text())
                res = list(dict.fromkeys(res))
                Connector.delete_items("budynki", res, "oznaczenie", str)
                self.refresh_buildings()

    def delete_vehicles(self):
        self.deleteWindow = DeletionConfirmation("pojazdy")
        self.deleteWindow.selected.connect(self.delete_vehicles_slot)
        self.deleteWindow.show()

    def delete_vehicles_slot(self, answer):
        if answer:
            selection = self.tabela_pojazdy.selectedItems()
            if selection:
                res = []
                for x in selection:
                    res.append(self.tabela_pojazdy.item(x.row(), 0).text())
                res = list(dict.fromkeys(res))
                Connector.delete_items("pojazdy", res, "id_pojazdu", int)
                self.refresh_vehicles()

    def delete_officers(self):
        self.deleteWindow = DeletionConfirmation("oficerowie")
        self.deleteWindow.selected.connect(self.delete_officers_slot)
        self.deleteWindow.show()

    def delete_officers_slot(self, answer):
        if answer:
            selection = self.tabela_oficerowie.selectedItems()
            if selection:
                res = []
                for x in selection:
                    res.append(self.tabela_oficerowie.item(x.row(), 2).text())
                res = list(dict.fromkeys(res))
                Connector.delete_items("oficerowie", res, "pesel", str)
                self.refresh_officers()

    def building_preview(self, rowid):
        item = self.tabela_budynki.item(rowid, 0)
        self.previewWindow = BuildingPreview(item.text())
        self.previewWindow.show()

    def vehicle_preview(self, rowid):
        item = self.tabela_pojazdy.item(rowid, 0)
        self.previewWindow = VehiclePreview(item.text())
        self.previewWindow.show()

    def officer_preview(self, rowid):
        item = self.tabela_oficerowie.item(rowid, 2)
        self.previewWindow = OfficerPreview(item.text())
        self.previewWindow.show()

    def set_info_tab(self):
        tab = QWidget()
        self.infoLayout = QGridLayout()
        info = create_info_box("jednostki", self.unit_id, "identyfikator", int)
        self.infoLayout.addWidget(info, 0, 0)

        self.counters = QGroupBox("Stan")
        counters_dict = Connector.get_count_data(self.unit_id)
        c_box_layout = QFormLayout()
        b_count = QLabel("<b>" + str(counters_dict["b_count"]) + "<\b>")
        c_box_layout.addRow("Liczba budynków: ", b_count)
        p_count = QLabel("<b>" + str(counters_dict["p_count"]) + "<\b>")
        c_box_layout.addRow("Liczba pojazdów: ", p_count)
        o_count = QLabel("<b>" + str(counters_dict["o_count"]) + "<\b>")
        c_box_layout.addRow("Liczba oficerów: ", o_count)
        self.counters.setLayout(c_box_layout)
        self.infoLayout.addWidget(self.counters, 1, 0)

        buttons = QGroupBox("Zarządzanie")
        buttonsLayout = QHBoxLayout()
        self.przydzialy = QPushButton("Przydziały")
        self.przydzialy.clicked.connect(self.assignment_window)
        self.zamowienia = QPushButton("Zamówienia")
        self.zamowienia.clicked.connect(self.orders_window)
        buttonsLayout.addWidget(self.przydzialy)
        buttonsLayout.addWidget(self.zamowienia)
        buttons.setLayout(buttonsLayout)
        self.infoLayout.addWidget(buttons, 2, 0)
        tab.setLayout(self.infoLayout)
        return tab

    def refresh_c_box(self):
        counters_dict = Connector.get_count_data(self.unit_id)
        c_box_layout = QFormLayout()
        b_count = QLabel("<b>" + str(counters_dict["b_count"]) + "<\b>")
        c_box_layout.addRow("Liczba budynków: ", b_count)
        p_count = QLabel("<b>" + str(counters_dict["p_count"]) + "<\b>")
        c_box_layout.addRow("Liczba pojazdów: ", p_count)
        o_count = QLabel("<b>" + str(counters_dict["o_count"]) + "<\b>")
        c_box_layout.addRow("Liczba oficerów: ", o_count)
        self.counters.setParent(None)
        self.counters = QGroupBox("Stan")
        self.counters.setLayout(c_box_layout)
        self.infoLayout.addWidget(self.counters, 1, 0)

    def assignment_window(self):
        self.assignmentWindow = AssignManagement(self.unit_id)
        self.assignmentWindow.show()

    def orders_window(self):
        self.ordersWindow = OrderManagement(self.unit_id)
        self.ordersWindow.show()
