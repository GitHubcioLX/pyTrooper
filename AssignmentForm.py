from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector
from config import rx


class AssignmentForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, type):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.type = type
        self.setWindowTitle("Nowy przydział")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        gap = QLabel()
        gap.setFixedHeight(1)
        disclaimer = QLabel('<i><font color="#707070">tekst</font> - pole nieobowiązkowe</i>')
        disclaimer.setAlignment(Qt.AlignRight)
        self.layout.addRow(gap)
        self.layout.addRow(disclaimer)
        self.setLayout(self.layout)
        self.setMinimumSize(250, 190)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.data_od = QLineEdit()
        self.data_od.setInputMask("9999-99-99")
        self.data_do = QLineEdit()
        self.data_do.setInputMask("9999-99-99")
        self.oficer = QComboBox()
        filter = " WHERE id_jednostki = " + str(self.id_jednostki) + " ORDER BY nazwisko, imie ASC"
        self.oficerowie = Connector.get_filtered("oficerowie", ["nazwisko", "imie", "pesel"], filter)
        oficerCombo = []
        for x in self.oficerowie:
            oficerCombo.append(str(x[0] + " " + x[1] + " [" + x[2] + "]"))
        self.oficer.addItems(oficerCombo)
        self.layout.addRow("Oficer: ", self.oficer)

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

        self.layout.addRow("Data rozpoczęcia: ", self.data_od)
        self.layout.addRow(QLabel('<font color="#707070">Data zakończenia: </font>'), self.data_do)
        self.layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))

    def confirm(self):
        data_od = self.data_od.text()
        data_do = self.data_do.text()
        oficer = self.oficerowie[self.oficer.currentIndex()][2]
        if self.type == "ekwipunek":
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
    window = AssignmentForm("1", "pojazd")
    window.show()
    app.exec_()
