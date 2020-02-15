import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from EquipmentListWindow import EquipmentListWindow

# GUI
app = QApplication([])
#text_area = QPlainTextEdit()
#text_area.setFocusPolicy(Qt.NoFocus)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.naglowek = QLabel()
        self.naglowek.setText("Zarządzanie jednostką")
        font = QFont()
        font.setBold(True)
        self.naglowek.setAlignment(Qt.AlignCenter)
        self.naglowek.setFont(font)
        self.jednostki = QListWidget()
        self.jednostkiT = QTableWidget()
        self.addButton = QPushButton("Dodaj")
        self.gap = QLabel()
        self.ekwipunek = QPushButton("Ekwipunek wojska")
        self.layout = QVBoxLayout()
        self.setWindowTitle("Menu glowne")
        self.set_jednostki()
        self.set_layout()
        self.setMinimumSize(600, 600)
        self.ekwipunek.clicked.connect(self.open_equipment)
        self.jednostkiT.cellDoubleClicked.connect(self.open_jednostki)


    def open_equipment(self):
        self.equipment_window = EquipmentListWindow()
        self.equipment_window.show()


    def set_jednostki(self):
        self.jednostki.addItem("Kurwa dupa chuj")
        self.jednostki.addItem("Kurwa chuj dupa")
        self.jednostki.addItem("Dupa kurwa chuj")
        self.jednostki.addItem("Chuj kurwa dupa")
        self.jednostkiT.setRowCount(10)
        self.jednostkiT.setColumnCount(2)
        item = QTableWidgetItem("kurwa")
        item.setFlags(item.flags() & ~Qt.ItemIsEditable)
        self.jednostkiT.setItem(0, 0, item)
        self.jednostkiT.setItem(0, 1, QTableWidgetItem("dupa"))
        self.jednostkiT.setHorizontalHeaderLabels(['Identyfikator', 'Nazwa'])
        self.jednostkiT.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.jednostkiT.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)

    def open_jednostki(self, rowid):
        item = self.jednostkiT.itemAt(0, 1)
        print(item.text())


    def set_layout(self):
        self.layout.addWidget(self.naglowek)
        self.layout.addWidget(self.jednostkiT)
        self.layout.addWidget(self.addButton)
        self.layout.addWidget(self.gap)
        self.layout.addWidget(self.ekwipunek)
        self.layout.addWidget(self.gap)
        self.setLayout(self.layout)


main_window = MainWindow()
main_window.show()

app.exec_()
