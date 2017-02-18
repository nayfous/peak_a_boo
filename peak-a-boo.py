import sys
import csv
import os
import pandas
import peakutils
import scipy
import scipy.signal
import difflib
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import matplotlib.pyplot as plt
import matplotlib.backends.qt_editor.figureoptions as figureoptions
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
UI_MAIN_WINDOW, Q_MAIN_WINDOW = loadUiType('design-2.ui')
plt.style.use('ggplot')
DIRECTORY_PATH = sys.path[0]

class MyApp(UI_MAIN_WINDOW, Q_MAIN_WINDOW):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.importButton.clicked.connect(self.reading_stimulie_file)
        self.fileKnop.clicked.connect(self.browse_folder)
        self.addButton.clicked.connect(self.folder_add)
        self.exportButton.clicked.connect(self.case(self.viewTable_1))
        self.model = QFileSystemModel()
        self.fig1 = Figure()
        self.canvas = FigureCanvas(self.fig1)
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()
        self.graphWindowLayout.addWidget(self.canvas)
        self.toolbar = MyToolbar(self.canvas)
        self.graphWindowLayout.addWidget(self.toolbar)
        self.data_memory = {}
        self.piek_height = {}
        self.input_values = {}
        self.labels = {}
        self.data = None
        self.file_list = None
        self.index = None
        self.file_path = None
        self.stimulie_dataframe = None
        self.directory = None
        self.ax1f1 = None
        self.ax1f2 = None

    def reading_stimulie_file(self):
        file_path = QFileDialog.getOpenFileName(self)[0]
        self.stimulie_dataframe = pandas.read_csv(file_path, header=None, sep=";")
        self.data_memory = {}
        try:
            self.data_read(self.file_path)
        except Exception:
            pass

    def browse_folder(self):
        self.listLijst.clear()
        self.folder_add()
    
    def folder_add(self):
        self.directory = QFileDialog.getExistingDirectory(self,
                                                        "Pick a folder")
        print(self.file_list)
        if self.file_list != None:
            self.file_list = self.file_list + self.file_lister(self.directory)
        else:
            self.file_list = self.file_lister(self.directory)
        self.index = 0
        self.listLijst.clicked.connect(self.selected_file)

    def file_lister(self, directory_path):

        """ Function file_lister: Takes as input the directory path (string directory_path);
            Returns a list containing paths of all txt files in the directory.
            Walks through all folders in de directory and adds the paths
            ending with .txt to the file_list. """

        file_list = []
        for root, dirs, files in os.walk(directory_path):
            del dirs
            for file in files:
                if file.endswith(".txt"):
                    file_list.append(root.replace(directory_path, "") + self.directory + "\\" + file)
                    self.listLijst.addItem(root.replace(directory_path, "") + "\\" + file)
                elif file.endswith(".csv"):
                    ammount = self.data_checker(root.replace(directory_path, "") + "\\" + file)
                    for i in range(ammount):
                        file_list.append(root.replace(directory_path, "") + self.directory +
                                         "\\" + file + "~" + str(i))
                        self.listLijst.addItem(root.replace(directory_path, "") +
                                               "\\" + file + "~" + str(i))
        return file_list

    def data_checker(self, file_path):
        with open(self.directory + file_path, 'r') as file:
            for i in range(2):
                line = file.readline()
        return len(line.split(',')) - 1

    # def tableSetter(self, table, row_count, column_count, columnData):

    #     """ Function tableSetter: Takes as input the table instant (tableWidget table),
    #         the ammount of rowes (int row_count), the ammount of columns (int column_count),
    #         the data for the table (list columnData). Initialize the table and
    #         fills it with the items of columnData. """

    #     table.setrow_count(row_count)
    #     table.setcolumn_count(column_count)
    #     for i in range(len(columnData)):
    #         table.setItem(0, i, QTableWidgetItem(str(columnData[i])))
    #     table.resizeColumnsToContents()
    #     table.resizeRowsToContents()
    #     table.cellChanged.connect(self.cellchanged)

    def input_table_setter(self, table, row_count, column_count):

        """ Function input_table_setter: takes as input the table instant (tableWidget table),
            the ammount of rows (int row_count), the ammount of columns (int column_count).
             Initialize the table and fills it with a combo_box with multiple options. """
        table.setRowCount(row_count)
        table.setColumnCount(column_count)
        if len(self.labels) > 0:
            table.setHorizontalHeaderLabels(self.labels[self.file_path])
        combo_box_options = ["O", "-", "--"]
        for i in range(column_count):
            combo = QComboBox()
            combo.addItems(combo_box_options)
            if self.file_path in self.input_values:
                ind = combo.findText(self.input_values[self.file_path][i])
                combo.setCurrentIndex(ind)
            table.setCellWidget(0, i, combo)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def bigTableSetter(self, table, row_count, column_count, data):

        """ Function bigTableSetter: takes as input the table instant (tableWidget table),
            the ammount of rows (int row_count), the ammount of columns (int column_count),
            the data for the table (dict data). Initialize the table and fills it with the data. """

        table.setRowCount(row_count)
        table.setColumnCount(column_count)
        i = 0
        for name in list(data.keys()):
            j = 0
            table.setItem(i, j, QTableWidgetItem(str(name.split("\\")[-1])))
            for val in data[name]:
                table.setItem(i, j+1, QTableWidgetItem(str(val)))
                j += 1
            i += 1
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def save_user_input(self, column_count):

        """ Function save_user_input: takes as input the ammount of columns (int column_count).
        Saves input of userInputTable in dict """

        inputs = []
        for i in range(column_count):
            inputs.append(self.inputTable.cellWidget(0, i).currentText())
        self.input_values[self.file_path] = inputs
        column_count = len(self.input_values[max(self.input_values,
                                                 key=lambda k: len(self.input_values[k]))]) + 1
        self.bigTableSetter(self.viewTable_1, len(self.input_values), column_count,
                            self.input_values)


    # def cellchanged(self):

    #     """ Function cellchanged: changes value of self.piek_height to 
    #         the new value that is changed in de table. """

    #     cor = self.dataTable.currentColumn()
    #     if cor > -1:
    #         self.piek_height[self.file_path][cor] = int(self.dataTable.currentItem().text())

    def table_values(self, path):
        """ Function table_values: takes as input the path of the file (str path); It calculates
            the percentage of the peak in comparison with the first peak. It corrects for Dye
            leakage bye substracting 10% of the first peak if the peak is further. """

        values = self.piek_height[path]
        table_data = []
        if len(values) > 0:
            percentage = 0.9
            table_data = [100]
            start_value = values[0]
            values = values[1:]
            for i in values:
                table_data.append((i/(start_value*percentage)*100))
                percentage -= 0.1
            self.piek_height[path] = table_data
        #column_count = len(self.piek_height[max(self.piek_height,
        #                   key=lambda k: len(self.piek_height[k]))]) + 1
        #self.tableSetter(self.dataTable, 1, len(table_data), table_data)
        #self.bigTableSetter(self.viewTable_2, len(self.piek_height), column_count,
        #                    self.piek_height)
        if len(self.labels) > 0:
            self.input_table_setter(self.inputTable, 1, len(self.labels[path]))
            self.save_user_input(len(self.labels[path]))
        else:
            self.input_table_setter(self.inputTable, 1, len(table_data))
            self.save_user_input(len(table_data))

    def case(self, table):
        def handle_save():
            path = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
            if all(path):
                with open(path[0], 'w') as stream:
                    writer = csv.writer(stream)
                    for row in range(table.rowCount()):
                        rowdata = []
                        for column in range(table.columnCount()):
                            item = table.item(row, column)
                            if item is not None:
                                rowdata.append(
                                    item.text().strip())
                            else:
                                rowdata.append('')
                        writer.writerow(rowdata)
        return handle_save



    def selected_file(self, index):
        self.index = index.row()
        self.file_path = self.file_list[self.index]
        if '~' in self.file_path:
            self.confocal_data_reader(self.file_path)
        else:
            try:
                self.data_read(self.file_path)
            except Exception:
                self.fig1.clf()
                print("invalid file")
                self.canvas.draw()
                #self.data_plot_Zeiss_ratio(self.file_path)

    def confocal_data_reader(self, file_path):
        if file_path not in self.labels:
            try:
                index = difflib.get_close_matches(file_path, list(self.stimulie_dataframe[0]),
                                                  cutoff=0)
                self.labels[file_path] = self.stimulie_dataframe[
                    self.stimulie_dataframe[0] == index[0]].dropna(axis=1).values[0][1:]
                if len(self.labels[file_path]) < 1:
                    self.toolbar.delete_plot()
                    return
            except Exception:
                pass
        file_path2, ind = file_path.split('~')
        self.data = pandas.read_csv(file_path2, ',', header=1)
        del self.data["Axis [s]"]
        self.data = self.data.replace(to_replace=',', value='.', regex=True)
        self.data = self.data.ix[:, int(ind)]
        data_ratio = np.array(self.data)
        if file_path not in self.data_memory:
            if len(self.labels) > 0:
                indexes = peakutils.indexes(data_ratio, thres=0.1, min_dist=250,
                                            max_ammount=
                                            len(self.labels[file_path]))
            else:
                indexes = peakutils.indexes(data_ratio, thres=0.1, min_dist=250)
            try:
                indexes = peakutils.interpolate(self.data.index.values, data_ratio, ind=indexes)
            except Exception:
                pass
            indexes = [int(elem) for elem in indexes]
            baseline_value = self.data[0:60].median()
            self.data_memory[file_path] = [indexes, baseline_value]
        self.data = self.data.to_frame()
        self.data.columns = ['ratio']
        self.signalBox.setChecked(False)
        self.plotter(file_path)

    def data_read(self, file_path):
        if file_path not in self.labels:
            try:
                index = difflib.get_close_matches(file_path, list(self.stimulie_dataframe[0]),
                                                  cutoff=0)
                self.labels[file_path] = self.stimulie_dataframe[
                    self.stimulie_dataframe[0] == index[0]].dropna(axis=1).values[0][1:]
                if len(self.labels[file_path]) < 1:
                    self.toolbar.delete_plot()
                    return
            except Exception:
                pass
        with open(file_path, 'r') as file:
            line = file.readline().strip()
        if line == "Time	CFP	YFP":
            self.data = pandas.read_csv(file_path, "\t")[2:]
        else:
            self.data = pandas.read_csv(file_path, "\t", header=3)
            del self.data["X.1"]
            self.data.columns = ["Time", "YFP", "CFP"]
        if "Unnamed: 3" in self.data.columns.values:
            del self.data["Unnamed: 3"]
        self.data['Time'] = self.data['Time'].astype(int)
        self.data = self.data.drop_duplicates(subset='Time', keep='last')
        self.data = self.data.set_index('Time')
        self.data = self.data.replace(to_replace=",", value=".", regex=True)
        self.data["YFP"] = scipy.signal.savgol_filter(np.array(
            self.data["YFP"].astype("float")), 17, 2)
        self.data["CFP"] = scipy.signal.savgol_filter(np.array(
            self.data["CFP"].astype("float")), 17, 2)
        self.data["ratio"] = self.data["YFP"] / self.data["CFP"]
        data_ratio = np.array(self.data["ratio"])
        if file_path not in self.data_memory:
            if len(self.labels) > 0:
                indexes = peakutils.indexes(data_ratio, thres=0.1, min_dist=250,
                                            max_ammount=len(self.labels[file_path]))
            else:
                indexes = peakutils.indexes(data_ratio, thres=0.1, min_dist=250)
            try:
                indexes = peakutils.interpolate(self.data.index.values, data_ratio, ind=indexes)
            except Exception:
                pass
            indexes = [int(elem) for elem in indexes]
            baseline_value = self.data['ratio'][0:60].median()
            self.data_memory[file_path] = [indexes, baseline_value]
        self.plotter(file_path)

    def plotter(self, file_path):
        self.fig1.clf()
        self.piek_height[file_path] = []
        try:
            data_y_index = self.data['ratio'].iloc[self.data_memory[file_path][0]]
            self.piek_height[file_path] = list(data_y_index - self.data_memory[file_path][1])
        except Exception:
            pass
        self.fig1.suptitle(file_path)
        if self.signalBox.isChecked() and self.ratioBox.isChecked():
            state_signal = 211
            state_ratio = 212
        else:
            state_signal = 111
            state_ratio = 111
        if self.signalBox.isChecked():
            self.ax1f1 = self.fig1.add_subplot(state_signal)
            if self.firstSignalBox.isChecked():
                self.ax1f1.plot(self.data.CFP, label=self.firstSignalText.text(), marker="o",
                                markevery=200)
            if self.secondSignalBox.isChecked():
                self.ax1f1.plot(self.data.YFP, label=self.secondSignalText.text(), marker="s",
                                markevery=200)
            self.ax1f1.set_xlim([0, max(self.data.index.values)])
            self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10),
                              fancybox=True, shadow=True)
        if self.ratioBox.isChecked():
            self.ax1f2 = self.fig1.add_subplot(state_ratio)
            self.ax1f2.plot(self.data.ratio, alpha=0.5, label='ratio')
            #self.ax1f2.scatter(self.data_memory[file_path][0], data_y_index.tolist(), marker='*', color='r', s=40)
            self.ax1f2.set_xlim([0, max(self.data.index.values)])
            self.ax1f2.set_xlabel("time (sec)")
            self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), 
                              fancybox=True, shadow=True)
        self.canvas.draw()
        self.table_values(file_path)

    def pickon(self, event):
        if event.button == 1:
            indexi = list(self.data_memory[self.file_path][0])
            indexi.append(int(event.xdata))
            indexi.sort()
            self.data_memory[self.file_path][0] = np.array(indexi)
            self.plotter(self.file_path)
            if len(self.labels) > 0:
                self.save_user_input(len(self.labels[self.file_path]))
            else:
                self.save_user_input(len(self.piek_height[self.file_path]))

        elif event.button == 3:
            rapo = range(int(event.xdata)-10, int(event.xdata)+10)
            indexi = list(self.data_memory[self.file_path][0])
            popo = [el for el in indexi if el in rapo]
            if len(popo) > 0:
                indexi.remove(popo[0])
            self.data_memory[self.file_path][0] = np.array(indexi)
            self.plotter(self.file_path)
            if len(self.labels) > 0:
                self.save_user_input(len(self.labels[self.file_path]))
            else:
                self.save_user_input(len(self.piek_height[self.file_path]))

    # def data_plot_Zeiss_ratio(self, file_path):
    #     self.fig1.clf()
    #     self.data = pandas.read_csv(file_path, "\t", header=3)
    #     self.data["X"] = self.data["X"].astype(int)
    #     self.data = self.data.drop_duplicates(subset='X', keep='last')
    #     self.data = self.data.set_index("X")
    #     datay = np.array(self.data["Y"])
    #     self.fig1.suptitle(file_path)

    #     if file_path in self.data_memory:
    #         indexes = self.data_memory[file_path][0]
    #         blIndexes = self.data_memory[file_path][1]
    #     else:
    #         indexes = peakutils.indexes(datay, thres=0.2, min_dist=200)
    #         try:
    #             indexes = peakutils.interpolate(self.data.index.values, datay, ind=indexes)
    #         except Exception:
    #             pass
    #         indexes = [int(elem) for elem in indexes]
    #         blIndexes = [self.data['ratio'][elem-20:elem].idxmin() for elem in indexes if elem > 20]
    #         self.data_memory[file_path] = [indexes, blIndexes]

    #     dataindex = self.data.loc[indexes]
    #     data_y_index = np.array(dataindex["Y"])
    #     blYindexes = self.data['Y'].loc[blIndexes]
    #     blYindexes = np.array(blYindexes)
    #     # piek_height = data_y_index - datablIndex
    #     # self.piek_height[file_path] = piek_height
    #     self.ax1f1 = self.fig1.add_subplot(111)
    #     self.ax1f1.plot(self.data.index.values, datay, label="ratio")
    #     self.ax1f1.scatter(indexes, data_y_index, marker='*', color='r', s=40)
    #     self.ax1f1.scatter(blIndexes, blYindexes, marker='o', color='g', s=40)
    #     self.ax1f1.set_xlim([0, max(self.data.index.values)])
    #     self.ax1f1.set_xlabel("time (sec)")
    #     self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
    #     self.canvas.draw()

    # def pickonRevamp(self, event):
    #     if event.button == 1:
    #         indexi = list(self.indexes)
    #         indexi.append(event.xdata)
    #         indexi.sort()
    #         self.indexes = np.array(indexi)
    #         self.dataindex = self.data.iloc[indexi]
    #         self.data_y_index = np.array(self.dataindex["ratio"])
    #         self.ax1f1.clear()
    #         self.ax1f1.plot(self.datax, self.datay, alpha=0.5, label='ratio')
    #         self.ax1f1.scatter(indexi, self.data_y_index, marker='*', color='r', s=40)
    #         self.ax1f1.set_xlim([0, max(self.datax)])
    #         self.canvas.draw()
    #     elif event.button == 3:
    #         rapo = range(int(event.xdata)-10, int(event.xdata)+10)
    #         po = [el for el in self.indexes if el in rapo]
    #         indexi = list(self.indexes)
    #         try:
    #             indexi.remove(po[0])
    #         except Exception:
    #             pass
    #         self.indexes = np.array(indexi)
    #         self.dataindex = self.data.loc[indexi]
    #         self.data_y_index = np.array(self.dataindex["ratio"])
    #         self.ax1f1.clear()
    #         self.ax1f1.plot(self.datax, self.datay, alpha=0.5, label='ratio')
    #         self.ax1f1.scatter(indexi, self.data_y_index, marker='*', color='r', s=40)
    #         self.ax1f1.set_xlim([0, max(self.datax)])
    #         self.canvas.draw()


class MyToolbar(NavigationToolbar):

    def __init__(self, figure_canvas, parent=None):
        self.toolitems = (('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
                          ('Back', 'consectetuer adipiscing elit', 'back', 'newBack'),
                          ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'newForward'),
                          (None, None, None, None),
                          ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
                          ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
                          (None, None, None, None),
                          ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
                          ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
                          ('print', 'print plot', DIRECTORY_PATH + "\\print", 'print_plot'),
                          ('delete', 'delete plot', DIRECTORY_PATH + "\\trash", 'delete_plot'),
                          ('piek', 'set and remove piek marker', DIRECTORY_PATH + '\\piek', 'piek'),
                         )
        super(MyToolbar, self).__init__(figure_canvas, parent=None)
        self.piek_status = False
        self.cid = None

    def print_plot(self):
        size = list(MYAPP.fig1.get_size_inches())
        MYAPP.fig1.set_size_inches(11.69, 8.27)
        MYAPP.fig1.savefig("temp.pdf", formta="pdf", orientation="landscape")
        MYAPP.fig1.set_size_inches(size[0], size[1], forward=True)
        MYAPP.canvas.draw()
        os.startfile("temp.pdf", "print")

    def delete_plot(self):
        item = MYAPP.listLijst.takeItem(MYAPP.index)
        # for row in range(MYAPP.viewTable_1.rowCount()):
        #     item = MYAPP.viewTable_1.item(row, 0).text()
        #     if item in MYAPP.file_path:
        #         MYAPP.viewTable_1.removeRow(row)
        file = str(MYAPP.file_path.split("\\")[-1])
        del item
        del MYAPP.file_list[MYAPP.index]
        del MYAPP.input_values[MYAPP.file_path]
        if MYAPP.index > len(MYAPP.file_list) - 1:
            MYAPP.index = 0
        MYAPP.file_path = MYAPP.directory + MYAPP.file_list[MYAPP.index]
        index = MYAPP.listLijst.model().index(MYAPP.index)
        MYAPP.listLijst.setCurrentIndex(index)
        if '~' in MYAPP.file_path:
            MYAPP.confocal_data_reader(MYAPP.file_path)
        else:
            try:
                MYAPP.data_read(MYAPP.file_path)
            except Exception:
                MYAPP.fig1.clf()
                print("invalid file")
                MYAPP.canvas.draw()
                #MYAPP.data_plot_Zeiss_ratio(MYAPP.file_path)

    def newForward(self):
        if len(MYAPP.labels) > 0:
            MYAPP.save_user_input(len(MYAPP.labels[MYAPP.file_path]))
        else:
            try:
                MYAPP.save_user_input(len(MYAPP.piek_height[MYAPP.file_path]))
            except KeyError:
                pass
        MYAPP.index += 1
        if MYAPP.index > len(MYAPP.file_list) - 1:
            MYAPP.index = 0
        MYAPP.file_path = MYAPP.directory + MYAPP.file_list[MYAPP.index]
        index = MYAPP.listLijst.model().index(MYAPP.index)
        MYAPP.listLijst.setCurrentIndex(index)
        if '~' in MYAPP.file_path:
            MYAPP.confocal_data_reader(MYAPP.file_path)
        else:
            try:
                MYAPP.data_read(MYAPP.file_path)
            except Exception:
                MYAPP.fig1.clf()
                print("invalid file")
                MYAPP.canvas.draw()
                #MYAPP.data_plot_Zeiss_ratio(MYAPP.file_path)

    def newBack(self):
        if len(MYAPP.labels) > 0:
            MYAPP.save_user_input(len(MYAPP.labels[MYAPP.file_path]))
        else:
            try:
                MYAPP.save_user_input(len(MYAPP.piek_height[MYAPP.file_path]))
            except KeyError:
                pass
        MYAPP.index += -1
        if MYAPP.index < 0:
            MYAPP.index = len(MYAPP.file_list) - 1
        MYAPP.file_path = MYAPP.directory + MYAPP.file_list[MYAPP.index]
        index = MYAPP.listLijst.model().index(MYAPP.index)
        MYAPP.listLijst.setCurrentIndex(index)
        if '~' in MYAPP.file_path:
            MYAPP.confocal_data_reader(MYAPP.file_path)
        else:
            try:
                MYAPP.data_read(MYAPP.file_path)
            except Exception:
                MYAPP.fig1.clf()
                print("invalid file")
                MYAPP.canvas.draw()
                #MYAPP.data_plot_Zeiss_ratio(MYAPP.file_path)

    def piek(self):
        self.piek_status = not self.piek_status
        if self.piek_status:
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
            try:
                self.cid = MYAPP.canvas.mpl_connect('button_press_event', MYAPP.pickon)
            except Exception:
                self.cid = MYAPP.canvas.mpl_connect('button_press_event', MYAPP.pickonRevamp)
        else:
            QApplication.restoreOverrideCursor()
            MYAPP.canvas.mpl_disconnect(self.cid)
        self._update_buttons_checked()


if __name__ == "__main__":
    APP = QApplication(sys.argv)
    MYAPP = MyApp()
    MYAPP.show()
    try:
        os.remove('temp.pdf')
    except Exception:
        pass
    sys.exit(APP.exec_())
