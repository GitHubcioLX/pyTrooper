import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Utilities import create_info_box


class VehiclePreview(QWidget):
    def __init__(self, id_pojazdu):
        super().__init__()
        self.setWindowTitle("Podgląd pojazdu")
        self.layout = QVBoxLayout()
        info = create_info_box("pojazdy", id_pojazdu, "id_pojazdu", int)
        self.layout.addWidget(info)
        self.setMinimumSize(270, 200)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = VehiclePreview("1")
    window.show()
    app.exec_()
