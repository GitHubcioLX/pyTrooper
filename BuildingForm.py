import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class BuildingForm(QWidget):
    def __init__(self, id_jednostki):
        super().__init__()
        self.setWindowTitle("Formularz (budynek)")
        self.layout = QFormLayout()
        self.addButton = QPushButton("Zatwierdź")
        self.set_form()
        self.setLayout(self.layout)

    def set_form(self):
        sign = QLineEdit()
        self.layout.addRow("Oznaczenie: ", sign)
        empCount = QLineEdit()
        self.layout.addRow("Docelowa liczba personelu: ", empCount)
        role = QLineEdit()
        self.layout.addRow("Rola budynku: ", role)


if __name__ == "__main__":
    app = QApplication([])
    window = BuildingForm("34529")
    window.show()
    app.exec_()
