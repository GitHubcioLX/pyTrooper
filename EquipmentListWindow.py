import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Utilities import create_table
from EquipmentForm import EquipmentForm
from EquipmentPreview import EquipmentPreview
from DeletionConfirmation import DeletionConfirmation
from connector import Connector
from config import rx


class EquipmentListWindow(QWidget):
    commited = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ekwipunek")
        self.setMinimumSize(400, 350)

        self.filter = QLineEdit()
        self.filter.setValidator(QRegExpValidator(QRegExp(rx)))
        self.filter.setPlaceholderText("Wyszukaj...")
        self.filter.returnPressed.connect(self.refresh_eq)

        self.addButton = QPushButton("Dodaj")
        self.delButton = QPushButton("Usuń")
        self.editButton = QPushButton("Edytuj")

        self.layout = QGridLayout()

        self.equipment = QTableWidget()
        self.refresh_eq()
        self.addWindow = None
        self.deleteWindow = None
        self.previewWindow = None

        self.addButton.clicked.connect(self.create_eq)
        self.delButton.clicked.connect(self.delete_items)
        self.editButton.clicked.connect(self.edit_eq)
        self.filter.returnPressed.connect(self.refresh_eq)

        self.set_layout()

    def refresh_eq(self):
        self.equipment = create_table(['Numer Seryjny', 'Producent', 'Model'],
                                      Connector.get_filtered("ekwipunek", ["numer_seryjny", "producent", "model"],
                                                             " WHERE UPPER(producent) LIKE UPPER('%" + self.filter.text() + "%')" +
                                                             " OR UPPER(model) LIKE UPPER('%" + self.filter.text() + "%')" +
                                                             " ORDER BY producent, model ASC"))
        self.equipment.cellDoubleClicked.connect(self.open_eq)
        self.layout.removeWidget(self.equipment)
        self.layout.addWidget(self.equipment, 0, 0, 1, 3)

    def set_layout(self):
        self.layout.addWidget(self.equipment, 0, 0, 1, 3)
        self.layout.addWidget(self.filter, 1, 0, 1, 3)
        self.layout.addWidget(self.addButton, 2, 0)
        self.layout.addWidget(self.delButton, 2, 1)
        self.layout.addWidget(self.editButton, 2, 2)
        self.setLayout(self.layout)

    def create_eq(self):
        self.addWindow = EquipmentForm("Dostępny")
        self.addWindow.commited.connect(self.refresh_eq)
        self.addWindow.show()

    def delete_items(self):
        self.deleteWindow = DeletionConfirmation("ekwipunek")
        self.deleteWindow.selected.connect(self.delete_items_slot)
        self.deleteWindow.show()

    def delete_items_slot(self, answer):
        if answer:
            selection = self.equipment.selectedItems()
            if selection:
                res = []
                for x in selection:
                    res.append(self.equipment.item(x.row(), 0).text())
                res = list(dict.fromkeys(res))
                Connector.delete_items("ekwipunek", res, "numer_seryjny", int)
                self.refresh_eq()

    def edit_eq(self):
        selection = self.equipment.selectedItems()
        res = []
        for x in selection:
            res.append(self.equipment.item(x.row(), 0).text())
        res = list(dict.fromkeys(res))
        if len(res) == 1:
            id = self.equipment.item(selection[0].row(), 0).text()
            self.addWindow = EquipmentForm(None, id)
            self.addWindow.commited.connect(self.refresh_eq)
            self.addWindow.show()

    def open_eq(self, rowid):
        item = self.equipment.item(rowid, 0)
        self.previewWindow = EquipmentPreview(item.text())
        self.previewWindow.show()
