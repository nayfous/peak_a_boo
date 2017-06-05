# Auteur: Soufyan Lakbir
"""
Navigation program for .csv and .txt data that represent FRET traces. Classification of the data can 
also be done
"""
# Imports
import sys
import File_browser
from PyQt5.uic import loadUiType
from PyQt5.QtWidgets import QApplication
# Retrieve design of GUI
UI_MAIN_WINDOW, Q_MAIN_WINDOW = loadUiType('design_with_menu.ui')


class PeakBoo(UI_MAIN_WINDOW, Q_MAIN_WINDOW):
    # initialize the global values
    def __init__(self):
        # retrieve and initialize GUI
        super(PeakBoo, self).__init__()
        setup = self.setupUi(self)
        self.file_browser = File_browser.FileBrowser(self.listLijst, self.searchBox, setup)
        self.run()

    def run(self):
        self.actionOpen_folder.triggered.connect(self.file_browser.folder_browser)
        self.actionAdd_folder.triggered.connect(self.file_browser.add_folder)
        self.searchBox.returnPressed.connect(self.file_browser.searching)


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    MYAPP = PeakBoo()
    MYAPP.show()
    sys.exit(APP.exec_())
