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
        self.layout = QVBoxLayout()
        self.set_form()
        self.addButton = QPushButton("Zatwierdź")
        self.layout.addWidget(self.addButton)
        self.setLayout(self.layout)
        self.setMinimumSize(250, 200)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        #Projekt:
        #Pierwszy GroupBox "Zamówienie" - koszt i deadline
        #Drugi GroupBox "Pojazd"/"Wyposażenie"  - formularz tworzenia takowego
        zamowienie = QGroupBox("Zamówienie")
        z_box_layout = QFormLayout()
        self.koszt = QLineEdit()
        self.koszt.setValidator(QDoubleValidator(0.01, 999999.99, 2))
        self.koszt.setMaxLength(9)
        self.data_zam = QLineEdit()
        self.data_zam.setInputMask("9999-99-99")
        self.data_zam.setText(str(Connector.get_cur_date()))
        self.deadline = QLineEdit()
        self.deadline.setInputMask("9999-99-99")
        z_box_layout.addRow("Data zamówienia: ", self.data_zam)
        z_box_layout.addRow("Maksymalny termin: ", self.deadline)
        z_box_layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))
        z_box_layout.addRow("Koszt [zł]: ", self.koszt)
        zamowienie.setLayout(z_box_layout)
        self.layout.addWidget(zamowienie)

        if self.type == "ekwipunek":
            ekwipunek = QGroupBox("Ekwipunek")
            eq_box_layout = QFormLayout()
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
            self.numer_seryjny = QLineEdit()
            self.numer_seryjny.setValidator(QIntValidator())
            eq_box_layout.addRow("Typ: ", self.typ)
            eq_box_layout.addRow("Producent: ", self.producent)
            eq_box_layout.addRow("Model: ", self.model)
            eq_box_layout.addRow("Numer seryjny: ", self.numer_seryjny)
            eq_box_layout.addRow("Data produkcji: ", self.data_produkcji)
            eq_box_layout.addRow("Data ważności: ", self.data_waznosci)
            eq_box_layout.addRow("", QLabel("Format daty: <b>RRRR-MM-DD<\b>"))
            ekwipunek.setLayout(eq_box_layout)
            self.layout.addWidget(ekwipunek)
        else:
            pojazd = QGroupBox("Pojazd")
            p_box_layout = QFormLayout()
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
            p_box_layout.addRow("Rodzaj: ", self.rodzaj)
            p_box_layout.addRow("Producent: ", self.producent)
            p_box_layout.addRow("Model: ", self.model)
            p_box_layout.addRow("Masa [kg]: ", self.masa)
            p_box_layout.addRow("Liczba załogi: ", self.zaloga)
            p_box_layout.addRow("Zasięg [km]: ", self.zasieg)
            p_box_layout.addRow("Rok produkcji: ", self.rok)
            pojazd.setLayout(p_box_layout)
            self.layout.addWidget(pojazd)

    def confirm(self):
        data_zam = self.data_zam.text()
        deadline = self.deadline.text()
        koszt = self.koszt.text()
        producent = self.producent.text()
        model = self.producent.text()
        if self.type == "ekwipunek:":
            numer_seryjny = self.numer_seryjny.text()
            typ = self.typ.currentText()
            data_produkcji = self.data_produkcji.text()
            data_waznosci = self.data_waznosci.text()
            if data_waznosci == "--":
                data_waznosci = ""
            if (Connector.insert_row('"Przydzial-ekwipunek"', ["data_od", "data_do", "pesel_oficera", "numer_seryjny"],
                                        [data_od, data_do, oficer, ekwipunek])):
                if Connector.update_row("ekwipunek", ["status"], ["Przydzielony"], ekwipunek, "numer_seryjny", int):
                    self.commited.emit()
                    self.close()
        else:
            rodzaj = self.rodzaj.currentText()
            masa = self.masa.text()
            zaloga = self.zaloga.text()
            zasieg = self.zasieg.text()
            rok = self.rok.text()
            id = Connector.create_zamowienie_pojazd([koszt, data_zam, deadline])
            print("ID: " + str(id))
            if id:
                if Connector.create_vehicle([rodzaj, producent, model, masa, zaloga, zasieg, "Zamówiony", rok, None,
                                             self.id_jednostki, id]):
                    self.commited.emit()
                    self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = OrderForm("1", "pojazd")
    window.show()
    app.exec_()
