# Auteur: Soufyan Lakbir
"""
Navigation program for .csv and .txt data that represent FRET traces. Classification of the data can 
also be done
"""
# Imports
from PyQt5.uic import loadUiType

# Retrieve design of GUI
UI_MAIN_WINDOW, Q_MAIN_WINDOW = loadUiType('design_with_menu.ui')


class PeakBoo(UI_MAIN_WINDOW, Q_MAIN_WINDOW):
    # initialize the global values
    def __init__(self):
        # retrieve and initialize GUI
        super(PeakBoo, self).__init__()
        self.setupUi(self)


