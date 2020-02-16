import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ErrorPopUp(QWidget):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("ERROR")
        self.layout = QVBoxLayout()

        self.naglowek = QLabel()
        self.naglowek.setText(message)
        font = QFont()
        font.setBold(True)
        self.naglowek.setAlignment(Qt.AlignCenter)
        self.naglowek.setFont(font)

        self.okButton = QPushButton("OK")

        self.set_layout()

        self.okButton.clicked.connect(self.close)

    def set_layout(self):
        self.layout.addWidget(self.naglowek)
        self.layout.addWidget(self.okButton)
        self.setLayout(self.layout)