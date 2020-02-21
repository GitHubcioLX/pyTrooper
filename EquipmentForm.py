from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector
from config import rx


class EquipmentForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, status, numer_seryjny=None):
        super().__init__()
        self.numer_seryjny_old = numer_seryjny
        self.status = status
        print(self.status)
        self.setWindowTitle("Formularz (ekwipunek)")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(280, 200)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.producent = QLineEdit()
        self.producent.setMaxLength(20)
        self.producent.setValidator(QRegExpValidator(QRegExp(rx)))
        self.model = QLineEdit()
        self.model.setMaxLength(20)
        self.model.setValidator(QRegExpValidator(QRegExp(rx)))
        self.data_produkcji = QLineEdit()
        self.data_produkcji.setInputMask("9999-99-99")
        self.data_waznosci = QLineEdit()
        self.data_waznosci.setInputMask("9999-99-99")
        self.typ = QComboBox()
        self.typ.addItems(Connector.get_enum("rodzaj_wyposazenia_type"))

        if self.numer_seryjny_old is not None:
            oldData = Connector.get_record("ekwipunek", ["producent", "model", "data_produkcji", "data_waznosci",
                                                          "typ", "status"],
                                           self.numer_seryjny_old, "numer_seryjny", int)
            self.producent.setText(oldData[0])
            self.model.setText(oldData[1])
            self.numer_seryjny = QLabel(str(self.numer_seryjny_old))
            self.data_produkcji.setText(str(oldData[2]))
            self.data_waznosci.setText(str(oldData[3]))
            self.typ.setCurrentText(oldData[4])
            self.status = oldData[5]
        else:
            self.numer_seryjny = QLineEdit()
            self.numer_seryjny.setValidator(QIntValidator())

        self.layout.addRow("Numer seryjny: ", self.numer_seryjny)
        self.layout.addRow("Producent: ", self.producent)
        self.layout.addRow("Model: ", self.model)
        self.layout.addRow("Data produkcji: ", self.data_produkcji)
        self.layout.addRow("Data ważności: ", self.data_waznosci)
        self.layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))
        self.layout.addRow("Typ: ", self.typ)

    def confirm(self):
        producent = self.producent.text()
        model = self.model.text()
        data_produkcji = self.data_produkcji.text()
        data_waznosci = self.data_waznosci.text()
        if data_waznosci == "--":
            data_waznosci = ""
        typ = self.typ.currentText()
        if self.numer_seryjny_old is not None:
            if (Connector.update_row("ekwipunek", ["producent", "model", "data_produkcji", "data_waznosci",
                                                          "typ", "status"],
                                     [producent, model, data_produkcji, data_waznosci, typ, self.status],
                                     self.numer_seryjny_old, "numer_seryjny", int)):
                self.commited.emit()
                self.close()
        else:
            numer_seryjny = self.numer_seryjny.text()
            if (Connector.insert_row("ekwipunek", ["numer_seryjny", "producent", "model", "data_produkcji", "data_waznosci",
                                                          "typ", "status"],
                                     [numer_seryjny, producent, model, data_produkcji, data_waznosci, typ, self.status])):
                self.commited.emit()
                self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = EquipmentForm(None, 1235135)
    window.show()
    app.exec_()