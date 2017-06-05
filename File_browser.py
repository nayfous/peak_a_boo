"""
Auteur: Soufyan Lakbir
File browser for the peak@boo program
"""
# Imports
import os
from PyQt5.QtWidgets import QFileDialog
import DataReader


class FileBrowser():
    """
    Class containing functions that open de folder browser and list all compatible (.txt and .csv)
    files.
    """

    def __init__(self, file_tree, search_box, setup):
        # initialize the global values
        self.file_tree = file_tree
        self.search_box = search_box
        self.setup = setup
        self.directory = ""
        self.selected_file_path = ""
        self.file_list = None
        self.search_list = None
        self.index = None
        self.DataReader = DataReader.DataReader()

    def folder_browser(self):
        # clear file list
        self.file_tree.clear()

        # open a folder selecting widget
        self.directory = QFileDialog.getExistingDirectory(self.setup, "Pick a folder")

        # make file list with all files in folder
        self.file_list = self.folder_crawler(self.directory)
        self.search_list = self.file_list[:]

        # initialize index to 0
        self.index = 0

        # if file name in list is clicked select file
        self.file_tree.clicked.connect(self.file_selecting)

    def folder_crawler(self, directory_path):
        list_files = []

        # search through all directory's for files ending with .txt and .csv
        for root, dirs, files in os.walk(directory_path):
            del dirs
            for file in files:
                name = directory_path + root.replace(directory_path, "") + "/" + file
                if file.endswith(".txt"):
                    # add filepath to the file list and the GUI list
                    list_files.append(name)
                    self.file_tree.addItem(name.replace(directory_path, ""))
                elif file.endswith(".csv"):
                    # loop through the csv file to find how many columns there are and add the file path to the list and GUI list
                    cell_count = self.cell_counter(name.replace(directory_path, ""))
                    for i in range(cell_count):
                        list_files.append(name + "~" + str(i))
                        self.file_tree.addItem(name.replace(directory_path, "") + "~" + str(i))

        return list_files

    def cell_counter(self, file_path):
        # open file and count amount of columns minus the first column (time column)
        with open(self.directory + file_path, 'r') as file:
            for i in range(2):
                line = file.readline()
        return len(line.split(',')) - 1

    def add_folder(self):
        # open a folder selecting widget
        self.directory = QFileDialog.getExistingDirectory(self.setup, "Pick a folder")

        # Add files in folder to file list and update search list
        self.file_list = self.file_list + self.folder_crawler(self.directory)
        self.search_list = self.file_list[:]

        # initialize index to 0
        self.index = 0

        # if file name in list is clicked select file
        self.file_tree.clicked.connect(self.file_selecting)

    def searching(self):
        # Take the search term of the user
        search_term = self.search_box.text()

        # Clear the file tree
        self.file_tree.clear()

        # if the path in file list contains the search term add to file list
        self.file_list = [path for path in self.search_list if search_term.lower() in path.lower()]

        # set index to 0
        self.index = 0

        # Add files in file list to file tree
        for path in self.file_list:
            self.file_tree.addItem(path.replace(self.directory, ""))

        # if file is selected plot data
        self.file_tree.clicked.connect(self.file_selecting)

    def file_selecting(self, index):

        # assign index and file path of selected file to variables
        self.index = index.row()
        self.selected_file_path = self.file_list[self.index]

        # read data
        self.DataReader.data_read(self.selected_file_path)




