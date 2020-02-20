import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box


class AssignmentPreview(QWidget):
    def __init__(self, data_od, pesel, nr_seryjny):
        super().__init__()
        self.setWindowTitle("Podgląd przydziału")
        self.layout = QVBoxLayout()
        filter = str(data_od) + " AND pesel_oficera = '" + pesel + "' AND numer_seryjny = " + str(nr_seryjny)
        info = create_info_box('"Przydzial-ekwipunek"', filter, "data_od", str, ["data_od", "data_do"])
        self.layout.addWidget(info)
        self.setMinimumSize(300, 230)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = AssignmentPreview("'2020-01-01'", "93050503945", 43135)
    window.show()
    app.exec_()
