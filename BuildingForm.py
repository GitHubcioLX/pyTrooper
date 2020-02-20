import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector


class BuildingForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, oznaczenie=None):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.oznaczenie = oznaczenie
        self.setWindowTitle("Formularz (budynek)")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.role = QLineEdit()
        self.empCount = QLineEdit()
        if self.oznaczenie is not None:
            oldData = Connector.get_record("budynki", ["rola_budynku", "liczba_personelu"], self.oznaczenie,
                                           "oznaczenie", str)
            self.role.setText(str(oldData[0]))
            self.empCount.setText(str(oldData[1]))
            self.sign = QLabel(self.oznaczenie)
        else:
            self.sign = QLineEdit()
        self.layout.addRow("Oznaczenie: ", self.sign)
        self.layout.addRow("Rola budynku: ", self.role)
        self.layout.addRow("Docelowa liczba personelu: ", self.empCount)

    def confirm(self):
        empCount = self.empCount.text()
        role = self.role.text()
        if self.oznaczenie is not None:
            if(Connector.update_row("budynki", ["liczba_personelu", "rola_budynku"],
                                     [empCount, role], self.oznaczenie, "oznaczenie", str)):
                self.commited.emit()
                self.close()
        else:
            sign = self.sign.text()
            if(Connector.insert_row("budynki", ["oznaczenie", "liczba_personelu", "rola_budynku", "id_jednostki"],
                                     [sign, empCount, role, self.id_jednostki])):
                self.commited.emit()
                self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = BuildingForm("34529")
    window.show()
    app.exec_()
