import PyQt5
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Utilities import set_info_tab, create_list_tab

# GUI
# app = QApplication([])

budynki = [["AB3", "Wychodek"], ["DG2", "Toaleta"], ["BG7", "Urynał"], ["QV1", "Ubikacja"], ["HU1", "Kibel"]]
oficerowie = [["Stasiek", "Dupas", "9450245291"], ["Krzysiek", "Kasztan", "9150258790"], ["Wiechu", "Szachista", "5540235263"]]
pojazdy = [["1", "Maluch"], ["2", "BMW"], ["3", "Silvia"], ["4", "Corolla"], ["5", "Rudy"], ["6", "Jagdpanzer"], ["7", "Rower"], ["8", "Turbosmiglowiec"]]


class UnitManagement(QTabWidget):
    def __init__(self, id_jednostki):
        global budynki, oficerowie, pojazdy
        super().__init__()
        self.setWindowTitle("Zarządzanie jednostką")
        self.setMinimumSize(400, 350)
        self.infoTab = set_info_tab(id_jednostki)
        self.listTab1 = create_list_tab(["Oznaczenie", "Rola"], budynki)
        self.listTab2 = create_list_tab(["ID", "Model"], pojazdy)
        self.listTab3 = create_list_tab(["Imię", "Nazwisko", "PESEL"], oficerowie)
        self.addTab(self.infoTab, "Ogólne")
        self.addTab(self.listTab1, "Budynki")
        self.addTab(self.listTab2, "Pojazdy")
        self.addTab(self.listTab3, "Oficerowie")


'''main_window = UnitManagement("420")
main_window.show()

app.exec_()'''
