import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector


class RankManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.ranks = QListWidget()
        self.addButton = QPushButton("Edytuj")
        self.layout = QVBoxLayout()
        self.setWindowTitle("Rangi")
        self.set_ranks()
        self.set_layout()

    def set_ranks(self):
        data = Connector.get_table_data("rangi", ["nazwa_rangi"])
        for item in data:
            name = item[0]
            self.ranks.addItem(name)

    def set_layout(self):
        self.layout.addWidget(self.ranks)
        self.layout.addWidget(self.addButton)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication([])
    window = RankManagement()
    window.show()
    app.exec_()