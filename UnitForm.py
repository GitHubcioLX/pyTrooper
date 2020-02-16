import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector


class UnitForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, parent):
        super().__init__()
        self.setWindowTitle("Nowa jednostka")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(300, 170)
        self.commited.connect(parent.set_jednostki)
        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.id = QLineEdit()
        self.layout.addRow("Identyfikator: ", self.id)
        self.name = QLineEdit()
        self.layout.addRow("Nazwa: ", self.name)
        self.type = QLineEdit()
        self.layout.addRow("Rodzaj: ", self.type)
        self.city = QLineEdit()
        self.layout.addRow("Miasto: ", self.city)

    def confirm(self):
        id = self.id.text()
        name = self.name.text()
        type = self.type.text()
        city = self.city.text()
        Connector.insert_row("jednostki", ["identyfikator", "nazwa", "rodzaj", "miasto"], [id, name, type, city])
        self.commited.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = UnitForm()
    window.show()
    app.exec_()