import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EquipmentListWindow import EquipmentListWindow

# GUI
app = QApplication([])


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.naglowek = QLabel()
        self.naglowek.setText("Zarządzanie jednostką")
        font = QFont()
        font.setBold(True)
        self.naglowek.setAlignment(Qt.AlignCenter)
        self.naglowek.setFont(font)

        self.jednostki = QTableWidget()

        self.addButton = QPushButton("Dodaj")

        self.gap = QLabel()

        self.equipLabel = QLabel()
        self.equipLabel.setText("Widok ekwipunku:")
        self.equipLabel.setAlignment(Qt.AlignCenter)

        self.ekwipunek = QPushButton("Ekwipunek wojska")

        self.layout = QVBoxLayout()

        self.setWindowTitle("Menu glowne")
        self.set_jednostki()
        self.set_layout()
        self.setMinimumSize(600, 600)

        self.ekwipunek.clicked.connect(self.open_equipment)
        self.jednostki.cellDoubleClicked.connect(self.open_jednostki)

    def open_equipment(self):
        self.equipment_window = EquipmentListWindow()
        self.equipment_window.show()

    def set_jednostki(self):
        self.jednostki.setRowCount(20)
        self.jednostki.setColumnCount(2)
        item = QTableWidgetItem("kurwa")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.jednostki.setItem(0, 0, item)
        self.jednostki.setItem(0, 1, QTableWidgetItem("dupa"))
        self.jednostki.setHorizontalHeaderLabels(['Identyfikator', 'Nazwa'])
        self.jednostki.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.jednostki.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def open_jednostki(self, rowid):
        item = self.jednostkiT.itemAt(0, 1)
        print(item.text())

    def set_layout(self):
        self.layout.addWidget(self.naglowek)
        self.layout.addWidget(self.jednostki)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.gap)
        self.layout.addWidget(self.equipLabel)
        self.layout.addWidget(self.ekwipunek)
        self.layout.addWidget(self.gap)
        self.setLayout(self.layout)


main_window = MainWindow()
main_window.show()

app.exec_()
