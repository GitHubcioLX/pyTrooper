import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box


class AssignmentPreview(QWidget):
    def __init__(self, type, data_od, pesel, x):
        super().__init__()
        self.setWindowTitle("Podgląd przydziału")
        self.layout = QVBoxLayout()
        oficer = create_info_box("oficerowie", pesel, "pesel", str, ["imie", "nazwisko", "ranga", "pesel"])
        oficer.setTitle("Oficer")
        if type == "ekwipunek":
            filter = "'" + str(data_od) + "' AND pesel_oficera = '" + pesel + "' AND numer_seryjny = " + str(x)
            info = create_info_box('"Przydzial-ekwipunek"', filter, "data_od", int, ["data_od", "data_do"])
            ekwipunek = create_info_box("ekwipunek", x, "numer_seryjny", int,
                                        ["typ", "producent", "model", "numer_seryjny"])
            ekwipunek.setTitle("Ekwipunek")
            self.layout.addWidget(info)
            self.layout.addWidget(oficer)
            self.layout.addWidget(ekwipunek)
        else:
            filter = "'" + str(data_od) + "' AND pesel_oficera = '" + pesel + "' AND id_pojazdu = " + str(x)
            info = create_info_box('"Przydzial-pojazd"', filter, "data_od", int, ["data_od", "data_do"])
            pojazd = create_info_box("pojazdy", x, "id_pojazdu", int,
                                        ["rodzaj", "producent", "model", "id_pojazdu"])
            pojazd.setTitle("Pojazd")
            self.layout.addWidget(info)
            self.layout.addWidget(oficer)
            self.layout.addWidget(pojazd)

        self.setMinimumSize(300, 230)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = AssignmentPreview("pojazd", "2020-01-10", "93050503945", 0)
    window.show()
    app.exec_()
