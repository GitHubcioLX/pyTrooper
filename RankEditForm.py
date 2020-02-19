import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector


class RankEditForm(QWidget):
    #commited = pyqtSignal()

    def __init__(self, nazwa_rangi):
        super().__init__()
        self.nazwa = nazwa_rangi
        self.oldData = Connector.get_record("rangi", ["liczba_przepustek", "poziom_upr", "zold"], self.nazwa,
                                            "nazwa_rangi", str)
        self.setWindowTitle("Edycja rangi")
        self.layout = QFormLayout()
        self.set_form()
        self.addButton = QPushButton("Zapisz")
        self.layout.addRow(QLabel())
        self.layout.addRow(self.addButton)
        self.setLayout(self.layout)

        self.addButton.clicked.connect(self.confirm)

    def set_form(self):
        self.layout.addRow("Nazwa: ", QLabel(self.nazwa))
        self.przepustki = QLineEdit()
        self.przepustki.setText(str(self.oldData[0]))
        self.layout.addRow("Liczba przepustek: ", self.przepustki)
        self.uprawnienia = QLineEdit()
        self.uprawnienia.setText(str(self.oldData[1]))
        self.layout.addRow("Poziom uprawnień: ", self.uprawnienia)
        self.zold = QLineEdit()
        self.zold.setText(str(self.oldData[2]))
        self.layout.addRow("Żołd: ", self.zold)

    def confirm(self):
        przepustki = self.przepustki.text()
        uprawnienia = self.uprawnienia.text()
        zold = self.zold.text()
        if(Connector.update_row("rangi", ["liczba_przepustek", "poziom_upr", "zold"],
                             [przepustki, uprawnienia, zold], self.nazwa, "nazwa_rangi", str)):
            #self.commited.emit()
            self.close()


if __name__ == "__main__":
    app = QApplication([])
    window = RankEditForm("Kapral")
    window.show()
    app.exec_()
