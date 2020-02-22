import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box
from connector import Connector


class OrderPreview(QWidget):
    def __init__(self, type, id_zamowienia):
        super().__init__()
        self.setWindowTitle("Podgląd zamówienia")
        self.layout = QVBoxLayout()
        if type == "ekwipunek":
            info = create_info_box('"Zamowienie-ekwipunek"', id_zamowienia, "id_zamowienia", int, ["id_zamowienia",
                                                                                                   "koszt", "data_zam",
                                                                                                   "deadline"])
            numer_seryjny = Connector.get_filtered("ekwipunek", ["numer_seryjny"],
                                                   " WHERE id_zamowienia = " + str(id_zamowienia))[0][0]
            ekwipunek = create_info_box("ekwipunek", numer_seryjny, "numer_seryjny", int,
                                        ["typ", "producent", "model", "numer_seryjny"])
            ekwipunek.setTitle("Ekwipunek")
            self.layout.addWidget(info)
            self.layout.addWidget(ekwipunek)
        else:
            info = create_info_box('"Zamowienie-pojazd"', id_zamowienia, "id_zamowienia", int, ["id_zamowienia",
                                                                                                "koszt", "data_zam",
                                                                                                "deadline"])
            id_pojazdu = Connector.get_filtered("pojazdy", ["id_pojazdu"],
                                                " WHERE id_zamowienia = " + str(id_zamowienia))[0][0]
            pojazd = create_info_box("pojazdy", id_pojazdu, "id_pojazdu", int,
                                        ["rodzaj", "producent", "model", "id_pojazdu"])
            pojazd.setTitle("Pojazd")
            self.layout.addWidget(info)
            self.layout.addWidget(pojazd)

        self.setMinimumSize(300, 230)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = OrderPreview("pojazd", "2")
    window.show()
    app.exec_()
