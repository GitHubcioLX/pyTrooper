from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector
from config import rx


class AssignmentForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki, pesel=None):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.oldPesel = pesel
        self.setWindowTitle("Nowy przydział")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(250, 200)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.data_od = QLineEdit()
        self.data_od.setInputMask("9999-99-99")
        self.data_do = QLineEdit()
        self.data_do.setInputMask("9999-99-99")
        self.oficer = QComboBox()
        filter = " WHERE id_jednostki = " + str(self.id_jednostki)
        self.oficerowie = Connector.get_filtered("oficerowie", ["imie", "nazwisko", "pesel"], filter)
        oficerCombo = []
        for x in self.oficerowie:
            oficerCombo.append(str(x[0] + " " + x[1] + " [" + x[2] + "]"))
        self.oficer.addItems(oficerCombo)
        self.ekwipunek = QComboBox()
        self.eq = Connector.get_filtered("ekwipunek", ["typ", "producent", "model", "numer_seryjny"],
                                    " WHERE status = 'Dostępny'")
        eqCombo = []
        for y in self.eq:
            eqCombo.append(str(y[0] + ": " + y[1] + " " + y[2] + " [" + str(y[3]) + "]"))
        self.ekwipunek.addItems(eqCombo)
        self.layout.addRow("Oficer: ", self.oficer)
        self.layout.addRow("Ekwipunek: ", self.ekwipunek)
        self.layout.addRow("Data rozpoczęcia: ", self.data_od)
        self.layout.addRow("Data zakończenia: ", self.data_do)
        self.layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))

    def confirm(self):
        data_od = self.data_od.text()
        data_do = self.data_do.text()
        oficer = self.oficerowie[self.oficer.currentIndex()][2]
        ekwipunek = self.eq[self.ekwipunek.currentIndex()][3]
        if(Connector.insert_row('"Przydzial-ekwipunek"', ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                    [data_od, data_do, oficer, ekwipunek])):
            if Connector.update_row("ekwipunek", ["status"], ["Przydzielony"], ekwipunek, "numer_seryjny", int):
                self.commited.emit()
                self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = AssignmentForm("1")
    window.show()
    app.exec_()
