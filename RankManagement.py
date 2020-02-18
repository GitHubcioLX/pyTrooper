import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from connector import Connector
from RankPreview import RankPreview
from RankEditForm import RankEditForm


class RankManagement(QWidget):
    def __init__(self):
        super().__init__()
        self.ranks = QListWidget()
        self.editButton = QPushButton("Edytuj")
        self.layout = QVBoxLayout()
        self.setWindowTitle("Rangi")
        self.preview = None
        self.edit = None
        self.set_ranks()
        self.set_layout()

    def set_ranks(self):
        data = Connector.get_table_data("rangi", ["nazwa_rangi"])
        for item in data:
            name = item[0]
            self.ranks.addItem(name)

    def open_preview(self, item):
        self.preview = RankPreview(item.text())
        self.preview.show()

    def edit_rank(self):
        selection = self.ranks.currentItem()
        if selection:
            self.edit = RankEditForm(selection.text())
            #self.edit.commited.connect()
            self.edit.show()

    def set_layout(self):
        self.layout.addWidget(self.ranks)
        self.layout.addWidget(self.editButton)
        self.setLayout(self.layout)

        self.ranks.itemDoubleClicked.connect(self.open_preview)
        self.editButton.clicked.connect(self.edit_rank)


if __name__ == "__main__":
    app = QApplication([])
    window = RankManagement()
    window.show()
    app.exec_()