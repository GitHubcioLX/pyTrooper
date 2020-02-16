import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class UnitForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nowa jednostka")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(300, 170)

    def set_form(self):
        id = QLineEdit()
        self.layout.addRow("Identyfikator: ", id)
        name = QLineEdit()
        self.layout.addRow("Nazwa: ", name)
        type = QLineEdit()
        self.layout.addRow("Rodzaj: ", type)
        city = QLineEdit()
        self.layout.addRow("Miasto: ", city)


if __name__ == "__main__":
    app = QApplication([])
    window = UnitForm()
    window.show()
    app.exec_()
