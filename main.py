import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# GUI
app = QApplication([])
#text_area = QPlainTextEdit()
#text_area.setFocusPolicy(Qt.NoFocus)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.jednostki = QListWidget()
        self.ekwipunek = QPushButton("Ekwipunek wojska")
        self.layout = QVBoxLayout()
        self.setWindowTitle("Menu glowne")
        self.set_jednostki()
        self.set_layout()

    def set_jednostki(self):
        self.jednostki.addItem("Kurwa dupa chuj")
        self.jednostki.addItem("Kurwa chuj dupa")
        self.jednostki.addItem("Dupa kurwa chuj")
        self.jednostki.addItem("Chuj kurwa dupa")

    def set_layout(self):
        self.layout.addWidget(self.jednostki)
        self.layout.addWidget(self.ekwipunek)
        self.setLayout(self.layout)


main_window = MainWindow()
main_window.show()

app.exec_()
