"""
Auteur: Soufyan Lakbir
File browser for the peak@boo program
"""
# Imports
import difflib
import pandas
import numpy as np

class DataReader():
    """
    Class containing functions that read the selected file and plot its content
    """

    def __init__(self):
        # Initialize the global values
       self.stimuli_data_frame = None
       self.data_memory = {}
       self.labels = {}
       self.data = None

    def data_read(self, file_path):
        # Read data from selected file

        # Create ind variable for confocal data use
        ind = None

        # if file not yet in the labels dictionary, check what the used stimuli are and save in self.labels
        if file_path not in self.labels:
            try:
                # check for the closest match of the file in the stimuli data
                index = difflib.get_close_matches(file_path, list(self.stimuli_data_frame[0]),
                                                  cutoff=0.6)
                # take the used stimuli
                self.labels[file_path] = self.stimuli_data_frame[
                                             self.stimuli_data_frame[0] == index[0]].dropna(axis=1).values[0][1:]
                # if no stimuli were used delete the plot
                if len(self.labels[file_path]) < 1:
                    #todo make toolbar file
                    #self.toolbar.delete_plot()
                    return
            except Exception:
                pass

        # Split file path if ~ in the path
        if '~' in file_path:
            new_file_path, ind = file_path.split('~')
        else:
            new_file_path = file_path

        # Open and read first line of file
        with open(new_file_path, 'r') as file:
            line = file.readline().strip()

        # If the first line is equal to "2" (Zeiss data) than read data
        if line == "2":
            # Read data
            self.data = pandas.read_csv(new_file_path, "\t", header=3)
            # Delete extra column
            del self.data["X.1"]
            # Change column names
            self.data.columns = ["Time", "YFP", "CFP"]

        # If line is equal to "Calcium_Ratio_Default" or "Channel.001" (convocal data) than read data
        elif line == "Calcium_Ratio_Default" or line == "Channel.001":
            # Read data
            self.data = pandas.read_csv(new_file_path, ',', header=1)
            # delete time column
            del self.data["Axis [s]"]
            # Make new time column
            self.data["Time"] = self.data.index.values
            # take the selected file column
            self.data = self.data.ix[:, int(ind)]

        # Read Nikkon data
        else:
            self.data = pandas.read_csv(new_file_path, "\t")[2:]

        # check for unnecessary columns and remove them
        if "Unnamed: 3" in self.data.columns.values:
            del self.data["Unnamed: 3"]
        elif "Unnamed: 4" in self.data.columns.values:
            del self.data["Unnamed: 4"]

        # change type of time column to int
        self.data['Time'] = self.data['Time'].astype(int)

        # remove duplicate time points and set time column as index
        self.data = self.data.drop_duplicates(subset='Time', keep='last')
        self.data = self.data.set_index('Time')

        # replace , in .
        self.data = self.data.replace(to_replace=",", value=".", regex=True)

        # create or overwrite column ratio by dividing YFP to CFP
        self.data["Ratio"] = self.data["YFP"].astype("float") / self.data["CFP"].astype("float")

        # # If normalize button is checked, normalize the data
        # if self.actionNormalize.isChecked():
        #     self.normalize_data()
        #
        # # plot data
        # self.plotter(file_path)