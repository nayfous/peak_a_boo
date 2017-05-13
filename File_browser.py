"""
Auteur: Soufyan Lakbir
File browser for the peak@boo program
"""
#imports
import os
from PeakBoo_V2 import PeakBoo
from PyQt5.QtWidgets import QFileDialog

class file_Browser():
    # initialize the global values
    def __init__(self):
        self.directory = ""
        self.selected_file_path = ""
        self.file_list = None
        self.search_list = None
        self.index = None

    def folder_browser(self):
        # clear file list
        PeakBoo.listLijst.clear()

        # open a folder selecting widget
        self.directory = QFileDialog.getExistingDirectory(self, "Pick a folder")

        # add files in folder to the file list and the search list
        if self.file_list != None:
            self.file_list = self.file_list + self.folder_crawler(self.directory)
            self.search_list = self.file_list[:]

        # make file list with all files in folder
        else:
            self.file_list = self.folder_crawler(self.directory)
            self.search_list = self.file_list[:]

        # initialize index to 0
        self.index = 0

        # if file name in list is clicked select file
        PeakBoo.listLijst.clicked.connect(self.file_selecting)

    def folder_crawler(self, directory_path):
        files = []

        # search through all directory's for files ending with .txt and .csv
        for root, dirs, files in os.walk(directory_path):
            del dirs
            for file in files:
                if file.endswith(".txt"):
                    # add filepath to the file list and the GUI list
                    name = directory_path + root.replace(directory_path, "") + "\\" + file
                    files.append(name)
                    PeakBoo.fileLijst.addItem(name.replace(directory_path, ""))
                elif file.endswith(".csv"):
                    # loop through the csv file to find how many columns there are and add the file path to the list and GUI list
                    cell_count = self.cell_counter(name.replace(directory_path, ""))
                    for i in range(cell_count):
                        files.append(name + "~" + str(i))
                        PeakBoo.listLijst.addItem(name.replace(directory_path, "") + "~" + str(i))

        return files

    def cell_counter(self, file_path):
        # open file and count amount of columns minus the first column (time column)
        with open(self.directory + file_path, 'r') as file:
            for i in range(2):
                line = file.readline()
        return len(line.split(',')) - 1

    def file_selecting(self, index):

        # assign index and file path of selected file to variables
        self.index = index.row()
        self.selected_file_path = self.file_list[self.index]

        # read data




