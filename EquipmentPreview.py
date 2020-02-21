import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box


class EquipmentPreview(QWidget):
    def __init__(self, numer_seryjny):
        super().__init__()
        self.setWindowTitle("Dane pojazdu")
        self.layout = QVBoxLayout()
        info = create_info_box("ekwipunek", numer_seryjny, "numer_seryjny", int)
        self.layout.addWidget(info)
        self.setMinimumSize(280, 200)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = EquipmentPreview("43135")
    window.show()
    app.exec_()
