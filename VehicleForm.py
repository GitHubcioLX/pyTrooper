from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from connector import Connector
from config import rx


class VehicleForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, status, id_pojazdu=None):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.status = status
        self.id_pojazdu = id_pojazdu
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
        self.rodzaj = QComboBox()
        self.rodzaj.addItems(Connector.get_enum("rodzaj_pojazdu_type"))
        self.producent = QLineEdit()
        self.producent.setMaxLength(15)
        self.producent.setValidator(QRegExpValidator(QRegExp(rx)))
        self.model = QLineEdit()
        self.model.setMaxLength(20)
        self.model.setValidator(QRegExpValidator(QRegExp(rx)))
        self.masa = QLineEdit()
        self.masa.setValidator(QIntValidator())
        self.zaloga = QLineEdit()
        self.zaloga.setValidator(QIntValidator())
        self.zasieg = QLineEdit()
        self.zasieg.setValidator(QIntValidator())
        self.rok = QLineEdit()
        self.rok.setValidator(QIntValidator())
        self.rejestracja = QLineEdit()
        self.rejestracja.setMaxLength(7)
        self.rejestracja.setValidator(QRegExpValidator(QRegExp(rx)))
        if self.id_pojazdu is not None:
            oldData = Connector.get_record("pojazdy", ["rodzaj", "producent", "model", "rok_produkcji", "masa",
                                                       "liczba_zalogi", "zasieg", "rejestracja", "status"],
                                           self.id_pojazdu, "id_pojazdu", int)
            self.rodzaj.setCurrentText(oldData[0])
            self.producent.setText(oldData[1])
            self.model.setText(oldData[2])
            self.rok.setText(str(oldData[3]))
            self.masa.setText(str(oldData[4]))
            self.zaloga.setText(str(oldData[5]))
            self.zasieg.setText(str(oldData[6]))
            self.rejestracja.setText(oldData[7])
            self.status = oldData[8]
        self.layout.addRow("Rodzaj: ", self.rodzaj)
        self.layout.addRow("Producent: ", self.producent)
        self.layout.addRow("Model: ", self.model)
        self.layout.addRow("Masa [kg]: ", self.masa)
        self.layout.addRow("Liczba załogi: ", self.zaloga)
        self.layout.addRow("Zasięg [km]: ", self.zasieg)
        self.layout.addRow("Rok produkcji: ", self.rok)
        self.layout.addRow("Rejestracja: ", self.rejestracja)

    def confirm(self):
        rodzaj = self.rodzaj.currentText()
        producent = self.producent.text()
        model = self.model.text()
        masa = self.masa.text()
        zaloga = self.zaloga.text()
        zasieg = self.zasieg.text()
        rok = self.rok.text()
        rejestracja = self.rejestracja.text()
        id_zamowienia = None
        if self.id_pojazdu is not None:
            if(Connector.update_row("pojazdy", ["rodzaj", "producent", "model", "rok_produkcji", "masa",
                                                "liczba_zalogi", "zasieg", "rejestracja", "status"],
                                    [rodzaj, producent, model, rok, masa, zaloga, zasieg, rejestracja, self.status],
                                    self.id_pojazdu, "id_pojazdu", int)):
                self.commited.emit()
                self.close()
        else:
            if(Connector.create_vehicle([rodzaj,
                                      producent,
                                      model,
                                      masa,
                                      zaloga,
                                      zasieg,
                                      self.status,
                                      rok,
                                      rejestracja,
                                      self.id_jednostki,
                                      id_zamowienia])):
                self.commited.emit()
                self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = VehicleForm('1', None, 0)
    window.show()
    app.exec_()
