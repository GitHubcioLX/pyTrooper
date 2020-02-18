import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box


class RankPreview(QWidget):
    def __init__(self, nazwa_rangi):
        super().__init__()
        self.setWindowTitle("Podgląd rangi")
        self.layout = QVBoxLayout()
        info = create_info_box("rangi", nazwa_rangi, "nazwa_rangi", str)
        self.layout.addWidget(info)
        self.setMinimumSize(240, 140)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = RankPreview("Kapral")
    window.show()
    app.exec_()
