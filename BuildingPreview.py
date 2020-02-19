import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box

mock_personel = ["Andrzej Konopka", "Stefan Orzech", "Marian Ziemny", "Grzegorz Włoski"]


class BuildingPreview(QWidget):
    def __init__(self, oznaczenie):
        global mock_personel
        super().__init__()
        self.setWindowTitle("Dane budynku")
        self.layout = QVBoxLayout()
        info = create_info_box("budynki", oznaczenie, "oznaczenie", str)
        self.layout.addWidget(info)

        personel_box = QGroupBox("Personel")
        p_box_layout = QVBoxLayout()
        personel = QListWidget()
        for pracownik in mock_personel:
            personel.addItem(pracownik)
        p_box_layout.addWidget(personel)
        personel_box.setLayout(p_box_layout)
        self.layout.addWidget(personel_box)

        self.setLayout(self.layout)


def set_info_box(oznaczenie, id_jednostki):
    info = QGroupBox("Informacje")
    layout = QFormLayout()
    layout.addRow("Oznaczenie: ", QLabel(oznaczenie))
    layout.addRow("Docelowa liczba personelu: ", QLabel("15"))
    layout.addRow("Rola budynku: ", QLabel("Wychodek"))
    layout.addRow("Identyfikator jednostki: ", QLabel(id_jednostki))
    info.setLayout(layout)
    return info


if __name__ == "__main__":
    app = QApplication([])
    window = BuildingPreview("A05")
    window.show()
    app.exec_()
