import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box


class OfficerPreview(QWidget):
    def __init__(self, pesel):
        super().__init__()
        self.setWindowTitle("Dane oficera")
        self.layout = QVBoxLayout()
        info = create_info_box("oficerowie", pesel, "pesel", str)
        self.layout.addWidget(info)
        self.setMinimumSize(300, 230)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = OfficerPreview("1")
    window.show()
    app.exec_()
