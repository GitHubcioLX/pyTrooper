from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from connector import Connector


class VehicleForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, status):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.status = status
        self.setWindowTitle("Formularz (pojazd)")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(280, 200)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.rodzaj = QLineEdit()
        self.layout.addRow("Rodzaj: ", self.rodzaj)
        self.producent = QLineEdit()
        self.layout.addRow("Producent: ", self.producent)
        self.model = QLineEdit()
        self.layout.addRow("Model: ", self.model)
        self.masa = QLineEdit()
        self.layout.addRow("Masa [kg]: ", self.masa)
        self.zaloga = QLineEdit()
        self.layout.addRow("Liczba załogi: ", self.zaloga)
        self.zasieg = QLineEdit()
        self.layout.addRow("Zasięg [km]: ", self.zasieg)
        self.rok = QLineEdit()
        self.layout.addRow("Rok produkcji: ", self.rok)
        self.rejestracja = QLineEdit()
        self.layout.addRow("Rejestracja: ", self.rejestracja)

    def confirm(self):
        rodzaj = self.rodzaj.text()
        producent = self.producent.text()
        model = self.model.text()
        masa = self.masa.text()
        zaloga = self.zaloga.text()
        zasieg = self.zasieg.text()
        rok = self.rok.text()
        rejestracja = self.rejestracja.text()
        Connector.create_vehicle([rodzaj,
                                  producent,
                                  model,
                                  masa,
                                  zaloga,
                                  zasieg,
                                  self.status,
                                  rok,
                                  rejestracja,
                                  self.id_jednostki,
                                  None])
        self.commited.emit()
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = VehicleForm("34529", "Dostępny")
    window.show()
    app.exec_()
