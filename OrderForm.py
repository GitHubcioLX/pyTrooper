from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector
from config import rx


class OrderForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, type):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.type = type
        self.setWindowTitle("Nowe zamówienie")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zatwierdź")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(250, 200)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        #Projekt:
        #Pierwszy GroupBox "Zamówienie" - koszt i deadline
        #Drugi GroupBox "Pojazd"/"Wyposażenie"  - formularz tworzenia takowego
        self.koszt = QLineEdit()
        self.koszt.setValidator(QIntValidator())
        self.data_zam = QLineEdit()
        self.data_zam.setInputMask("9999-99-99")
        self.deadline = QLineEdit()
        self.deadline.setInputMask("9999-99-99")

        if self.type == "ekwipunek":
            self.ekwipunek = QComboBox()
            self.eq = Connector.get_filtered("ekwipunek", ["typ", "producent", "model", "numer_seryjny"],
                                             " WHERE status = 'Dostępny' ORDER BY typ, producent, model ASC")
            eqCombo = []
            for y in self.eq:
                eqCombo.append(y[0] + ": " + y[1] + " " + y[2] + " [" + str(y[3]) + "]")
            self.ekwipunek.addItems(eqCombo)
            self.layout.addRow("Ekwipunek: ", self.ekwipunek)
        else:
            self.pojazdy = QComboBox()
            self.vh = Connector.get_filtered("pojazdy", ["producent", "model", "id_pojazdu"],
                                             " WHERE status = 'Dostępny' AND id_jednostki = " + self.id_jednostki +
                                             " ORDER BY producent, model ASC")
            vhCombo = []
            for y in self.vh:
                vhCombo.append(y[0] + " " + y[1] + " [" + str(y[2]) + "]")
            self.pojazdy.addItems(vhCombo)
            self.layout.addRow("Pojazd: ", self.pojazdy)

        self.layout.addRow("Data zamowienia: ", self.data_zam)
        self.layout.addRow("Maksymalny termin: ", self.data_deadline)
        self.layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))

    def confirm(self):
        data_od = self.data_od.text()
        data_do = self.data_do.text()
        oficer = self.oficerowie[self.oficer.currentIndex()][2]
        if self.type == "ekwipunek:":
            ekwipunek = self.eq[self.ekwipunek.currentIndex()][3]
            if(Connector.insert_row('"Przydzial-ekwipunek"', ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                        [data_od, data_do, oficer, ekwipunek])):
                if Connector.update_row("ekwipunek", ["status"], ["Przydzielony"], ekwipunek, "numer_seryjny", int):
                    self.commited.emit()
                    self.close()
        else:
            pojazd = self.vh[self.pojazdy.currentIndex()][2]
            if (Connector.insert_row('"Przydzial-pojazd"', ["data_od", "data_do", "pesel_oficera", "id_pojazdu"],
                                     [data_od, data_do, oficer, pojazd])):
                if Connector.update_row("pojazdy", ["status"], ["Przydzielony"], pojazd, "id_pojazdu", int):
                    self.commited.emit()
                    self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = OrderForm("1", "pojazd")
    window.show()
    app.exec_()
