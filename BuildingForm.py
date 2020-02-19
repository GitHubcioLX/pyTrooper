import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector


class BuildingForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.setWindowTitle("Formularz (budynek)")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.sign = QLineEdit()
        self.layout.addRow("Oznaczenie: ", self.sign)
        self.empCount = QLineEdit()
        self.layout.addRow("Docelowa liczba personelu: ", self.empCount)
        self.role = QLineEdit()
        self.layout.addRow("Rola budynku: ", self.role)

    def confirm(self):
        sign = self.sign.text()
        empCount = self.empCount.text()
        role = self.role.text()
        if(Connector.insert_row("budynki", ["oznaczenie", "liczba_personelu", "rola_budynku", "id_jednostki"], [sign, empCount, role, self.id_jednostki])):
            self.commited.emit()
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = BuildingForm("34529")
    window.show()
    app.exec_()
