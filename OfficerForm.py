from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector


class OfficerForm(QWidget):
    commited = pyqtSignal()

    def __init__(self, id_jednostki):
        super().__init__()
        self.id_jednostki = id_jednostki
        self.setWindowTitle("Formularz (oficer)")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(280, 200)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.imie = QLineEdit()
        self.layout.addRow("Imię: ", self.imie)
        self.nazwisko = QLineEdit()
        self.layout.addRow("Nazwisko: ", self.nazwisko)
        self.pesel = QLineEdit()
        self.layout.addRow("PESEL: ", self.pesel)
        self.data_ur = QLineEdit()
        self.layout.addRow("Data urodzenia: ", self.data_ur)
        self.layout.addRow(" ", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))
        self.wyznanie = QLineEdit()
        self.layout.addRow("Wyznanie: ", self.wyznanie)
        self.grupa_krwi = QComboBox()
        self.grupa_krwi.addItems(Connector.get_enum("grupa_krwi_type"))
        self.layout.addRow("Grupa krwi: ", self.grupa_krwi)
        self.ranga = QComboBox()
        rangi = Connector.get_table_data("rangi", ["nazwa_rangi"])
        for i in range(len(rangi)):
            rangi[i] = rangi[i][0]
        self.ranga.addItems(rangi)
        self.layout.addRow("Ranga: ", self.ranga)
        self.budynek = QComboBox()
        filter = " WHERE id_jednostki = " + str(self.id_jednostki);
        budynki = Connector.get_filtered("budynki", ["oznaczenie"], filter)
        for i in range(len(budynki)):
            budynki[i] = budynki[i][0]
        self.budynek.addItems(budynki)
        self.layout.addRow("Budynek: ", self.budynek)


    def confirm(self):
        pesel = self.pesel.text()
        imie = self.imie.text()
        nazwisko = self.nazwisko.text()
        data_ur = self.data_ur.text()
        grupa_krwi = self.grupa_krwi.currentText()
        wyznanie = self.wyznanie.text()
        ranga = self.ranga.currentText()
        budynek = self.budynek.currentText()
        if(Connector.insert_row("oficerowie", ["pesel", "imie", "nazwisko", "data_ur", "wyznanie", "id_jednostki", "budynek", "ranga", "grupa_krwi"],
                            [pesel, imie, nazwisko, data_ur, wyznanie, self.id_jednostki, budynek, ranga, grupa_krwi])):
            self.commited.emit()
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = OfficerForm("1")
    window.show()
    app.exec_()
