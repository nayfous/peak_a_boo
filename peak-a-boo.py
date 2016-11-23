import sys, csv, os, pandas, peakutils, scipy.signal
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
Ui_MainWindow, QMainWindow = loadUiType('design-2.ui')
plt.style.use('ggplot')
dirPath = sys.path[0]

class MyApp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.fileKnop.clicked.connect(self.browse_folder)
        self.SaveKnop.clicked.connect(self.handleSave)
        self.model = QFileSystemModel()
        self.fig1 = Figure()
        self.canvas = FigureCanvas(self.fig1)
        self.canvas.setFocusPolicy(Qt.ClickFocus)
        self.canvas.setFocus()
        self.graphWindowLayout.addWidget(self.canvas)
        self.toolbar = MyToolbar(self.canvas)
        self.graphWindowLayout.addWidget(self.toolbar)
        self.dataMemory = {}
        self.piekHeight = {}
        self.inputValues = {}

    def fileLister(self, dirPath):

        """ Function fileLister: Takes as input the directory path (string dirPath);
            Returns a list containing paths of all txt files in the directory.
            Walks through all folders in de directory and adds the paths ending with .txt to the filelist."""

        filelist = []
        for root, dirs, files in os.walk(dirPath):
            for file in files:
                if file.endswith(".txt"):
                    filelist.append(root.replace(dirPath, "") + "\\" + file)

        return filelist

    def tableSetter(self, table, rowCount, columnCount, columnData):

        """ Function tableSetter: Takes as input the table instant (tableWidget table),
            the ammount of rowes (int rowCount), the ammount of columns (int columnCount),
            the data for the table (list columnData). Initialize the table and fills it with the items of columnData. """

        table.setRowCount(rowCount)
        table.setColumnCount(columnCount)
        for i in range(len(columnData)):
            table.setItem(0, i, QTableWidgetItem(str(columnData[i])))
        table.resizeColumnsToContents()
        table.resizeRowsToContents()
        table.cellChanged.connect(self.cellchanged)

    def inputTableSetter(self, table, rowCount, columnCount):

        """ Function inputTableSetter: takes as input the table instant (tableWidget table),
            the ammount of rows (int rowCount), the ammount of columns (int columnCount).
             Initialize the table and fills it with a combo_box with multiple options. """

        table.setRowCount(rowCount)
        table.setColumnCount(columnCount)
        combo_box_options = [" ", "++", "+", "+/-", "-", "--"]
        for i in range(columnCount):
            combo = QComboBox()
            combo.addItems(combo_box_options)
            table.setCellWidget(0, i, combo)
        table.resizeColumnsToContents()
        table.resizeRowsToContents()

    def bigTableSetter(self, table, rowCount, columnCount, data):

        """ Function bigTableSetter: takes as input the table instant (tableWidget table),
            the ammount of rows (int rowCount), the ammount of columns (int columnCount),
            the data for the table (dict data). Initialize the table and fills it with the data. """

        table.setRowCount(rowCount)
        table.setColumnCount(columnCount)
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

    def saveUserInput(self, columnCount):

        """ Function saveUserInput: takes as input the ammount of columns (int columnCount).
        Saves input of userInputTable in dict """

        inputs = []
        for i in range(columnCount):
            inputs.append(self.inputTable.cellWidget(0, i).currentText())
        self.inputValues[self.filePath] = inputs
        columnCount = len(self.inputValues[max(self.inputValues, key=lambda k: len(self.inputValues[k]))]) + 1
        self.bigTableSetter(self.viewTable_1, len(self.inputValues), columnCount, self.inputValues)


    def cellchanged(self):

        """ Function cellchanged: changes value of self.piekHeight to 
            the new value that is changed in de table. """

        cor = self.dataTable.currentColumn()
        if cor > -1:
            self.piekHeight[self.filePath][cor] = int(self.dataTable.currentItem().text())

    def tableValues(self, path):
        """ Function tableValues: takes as input the path of the file (str path); It calculates 
            the percentage of the piek in comparison with the first peak. It corrects for Dye 
            leakage bye substracting 10% of the first peak if the peak is further. """

        values = self.piekHeight[path]
        percentage = 0.9
        tableData = [100]
        startValue = values[0]
        values = values[1:]
        for i in values:
            tableData.append((i/(startValue*percentage)*100))
            percentage -= 0.1
        self.piekHeight[path] = tableData
        columnCount = len(self.piekHeight[max(self.piekHeight, key=lambda k: len(self.piekHeight[k]))]) + 1
        self.tableSetter(self.dataTable, 1, len(tableData), tableData)
        self.bigTableSetter(self.viewTable_2, len(self.piekHeight), columnCount, self.piekHeight)
        self.inputTableSetter(self.inputTable, 1, len(tableData))
        self.saveUserInput(len(tableData))

    def handleSave(self):
        path = QFileDialog.getSaveFileName(
            self, 'Save File', '', 'CSV(*.csv)')
        if all(path):
            with open(path[0], 'w') as stream:
                writer = csv.writer(stream)
                for row in range(self.viewTable_2.rowCount()):
                    rowdata = []
                    for column in range(self.viewTable_2.columnCount()):
                        item = self.viewTable_2.item(row, column)
                        if item is not None:
                            rowdata.append(
                                item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

    def browse_folder(self):
        self.directory = QFileDialog.getExistingDirectory(self,
                                                          "Pick a folder")
        self.fileList = self.fileLister(self.directory)
        self.index = 0
        self.listLijst.addItems(self.fileList)
        self.listLijst.clicked.connect(self.selected_file)

    def selected_file(self, index):
        self.index = index.row()
        self.filePath = self.directory + index.data()
        try:
            self.Data_read(self.filePath)
        except Exception as e:
            self.data_plot_Zeiss_ratio(self.filePath)

    def Data_read(self, filepath):
        with open(filepath, 'r') as f:
            line = f.readline().strip()
        if line == "Time	CFP	YFP":
            self.data = pandas.read_csv(filepath, "\t")[2:]
        else:
            self.data = pandas.read_csv(filepath, "\t", header=3)
            del self.data["X.1"]
            self.data.columns = ["Time", "YFP", "CFP"]
        if "Unnamed: 3" in self.data.columns.values:
            del self.data["Unnamed: 3"]
        self.data['Time'] = self.data['Time'].astype(int)
        self.data = self.data.drop_duplicates(subset='Time', keep='last')
        self.data = self.data.set_index('Time')
        self.data = self.data.replace(to_replace=",", value=".", regex=True)
        self.data["YFP"] = scipy.signal.savgol_filter(np.array(self.data["YFP"].astype("float")), 17, 2)
        self.data["CFP"] = scipy.signal.savgol_filter(np.array(self.data["CFP"].astype("float")), 17, 2)
        self.data["ratio"] = self.data["YFP"] / self.data["CFP"]
        dataRatio = np.array(self.data["ratio"])
        if filepath in self.dataMemory:
            indexes = self.dataMemory[filepath][0]
            blValue = self.dataMemory[filepath][1]
        else:
            indexes = peakutils.indexes(dataRatio, thres=0.2, min_dist=200)
            try:
                indexes = peakutils.interpolate(self.data.index.values, dataRatio, ind=indexes)
            except Exception:
                pass
            indexes = [int(elem) for elem in indexes]
            blValue = self.data['ratio'][0:60].median()
            self.dataMemory[filepath] = [indexes, blValue]
        self.plotter(filepath)

    def plotter(self, filepath):
        self.fig1.clf()
        datayIndex = self.data['ratio'].iloc[self.dataMemory[filepath][0]]
        self.fig1.suptitle(filepath)
        self.piekHeight[filepath] = list(datayIndex - self.dataMemory[filepath][1])
        self.ax1f1 = self.fig1.add_subplot(211)
        self.ax1f2 = self.fig1.add_subplot(212)
        self.ax1f1.plot(self.data.CFP, label="CFP", marker="o", markevery=200)
        self.ax1f1.plot(self.data.YFP, label="YFP", marker="s", markevery=200)
        self.ax1f2.plot(self.data.ratio, alpha=0.5, label='ratio')
        self.ax1f2.scatter(self.dataMemory[filepath][0], datayIndex.tolist(), marker='*', color='r', s=40)
        self.ax1f2.set_xlim([0, max(self.data.index.values)])
        self.ax1f1.set_xlim([0, max(self.data.index.values)])
        self.ax1f2.set_xlabel("time (sec)")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.canvas.draw()
        self.tableValues(filepath)

    def data_plot_Zeiss_ratio(self, filepath):
        self.fig1.clf()
        self.data = pandas.read_csv(filepath, "\t", header=3)
        self.data["X"] = self.data["X"].astype(int)
        self.data = self.data.drop_duplicates(subset='X', keep='last')
        self.data = self.data.set_index("X")
        datay = np.array(self.data["Y"])
        self.fig1.suptitle(filepath)

        if filepath in self.dataMemory:
            indexes = self.dataMemory[filepath][0]
            blIndexes = self.dataMemory[filepath][1]
        else:
            indexes = peakutils.indexes(datay, thres=0.2, min_dist=200)
            try:
                indexes = peakutils.interpolate(self.data.index.values, datay, ind=indexes)
            except Exception:
                pass
            indexes = [int(elem) for elem in indexes]
            blIndexes = [self.data['ratio'][elem-20:elem].idxmin() for elem in indexes if elem > 20]
            self.dataMemory[filepath] = [indexes, blIndexes]

        dataindex = self.data.loc[indexes]
        datayIndex = np.array(dataindex["Y"])
        blYindexes = self.data['Y'].loc[blIndexes]
        blYindexes = np.array(blYindexes)
        # piekHeight = datayIndex - datablIndex
        # self.piekHeight[filepath] = piekHeight
        self.ax1f1 = self.fig1.add_subplot(111)
        self.ax1f1.plot(self.data.index.values, datay, label="ratio")
        self.ax1f1.scatter(indexes, datayIndex, marker='*', color='r', s=40)
        self.ax1f1.scatter(blIndexes, blYindexes, marker='o', color='g', s=40)
        self.ax1f1.set_xlim([0, max(self.data.index.values)])
        self.ax1f1.set_xlabel("time (sec)")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.canvas.draw()

    def pickon(self, event):
        if event.button == 1:
            indexi = list(self.dataMemory[self.filePath][0])
            indexi.append(int(event.xdata))
            indexi.sort()
            self.dataMemory[self.filePath][0] = np.array(indexi)
            self.plotter(self.filePath)
            self.saveUserInput(len(self.piekHeight[self.filePath]))

        elif event.button == 3:
            rapo = range(int(event.xdata)-10, int(event.xdata)+10)
            indexi = list(self.dataMemory[self.filePath][0])
            po = [el for el in indexi if el in rapo]
            if len(po) > 0:
                ind = indexi.index(po[0])
                indexi.remove(po[0])
            self.dataMemory[self.filePath][0] = np.array(indexi)
            self.plotter(self.filePath)
            self.saveUserInput(len(self.piekHeight[self.filePath]))

#moet verbeterd worden
    def pickonRevamp(self, event):
        if event.button == 1:
            indexi = list(self.indexes)
            indexi.append(event.xdata)
            indexi.sort()
            self.indexes = np.array(indexi)
            self.dataindex = self.data.iloc[indexi]
            self.datayIndex = np.array(self.dataindex["ratio"])
            self.ax1f1.clear()
            self.ax1f1.plot(self.datax, self.datay, alpha=0.5, label='ratio')
            self.ax1f1.scatter(indexi, self.datayIndex, marker='*', color='r', s=40)
            self.ax1f1.set_xlim([0, max(self.datax)])
            self.canvas.draw()
        elif event.button == 3:
            rapo = range(int(event.xdata)-10, int(event.xdata)+10)
            po = [el for el in self.indexes if el in rapo]
            indexi = list(self.indexes)
            try:
                indexi.remove(po[0])
            except Exception:
                pass
            self.indexes = np.array(indexi)
            self.dataindex = self.data.loc[indexi]
            self.datayIndex = np.array(self.dataindex["ratio"])
            self.ax1f1.clear()
            self.ax1f1.plot(self.datax, self.datay, alpha=0.5, label='ratio')
            self.ax1f1.scatter(indexi, self.datayIndex, marker='*', color='r', s=40)
            self.ax1f1.set_xlim([0, max(self.datax)])
            self.canvas.draw()


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
                          ('print', 'print plot', dirPath + "\print", 'print_plot'),
                          ('delete', 'delete plot', dirPath + "\\trash", 'delete_plot'),
                          ('piek', 'set and remove piek marker', dirPath + '\piek', 'piek'),
                         )
        super(MyToolbar, self).__init__(figure_canvas, parent=None)
        self.piek_status = False

    def print_plot(self):
        size = list(myapp.fig1.get_size_inches())
        myapp.fig1.set_size_inches(11.69, 8.27)
        myapp.fig1.savefig("temp.pdf", formta="pdf", orientation="landscape")
        myapp.fig1.set_size_inches(size[0], size[1], forward=True)
        myapp.canvas.draw()
        os.startfile("temp.pdf", "print")

    def delete_plot(self):
        del myapp.fileList[myapp.index]
        myapp.listLijst.clear()
        myapp.listLijst.addItems(myapp.fileList)
        myapp.filePath = myapp.directory + myapp.fileList[myapp.index]
        try:
            myapp.Data_read(myapp.filePath)
        except Exception:
            myapp.data_plot_Zeiss_ratio(myapp.filePath)

    def newForward(self):
        myapp.saveUserInput(len(myapp.piekHeight[myapp.filePath]))
        myapp.index += 1
        if myapp.index > len(myapp.fileList) - 1:
            myapp.index = 0
        myapp.filePath = myapp.directory + myapp.fileList[myapp.index]
        index = myapp.listLijst.model().index(myapp.index)
        myapp.listLijst.setCurrentIndex(index)
        try:
            myapp.Data_read(myapp.filePath)
        except Exception as e:
            myapp.data_plot_Zeiss_ratio(myapp.filePath)

    def newBack(self):
        myapp.saveUserInput(len(myapp.piekHeight[myapp.filePath]))
        myapp.index += -1
        if myapp.index < 0:
            myapp.index = len(myapp.fileList) - 1
        myapp.filePath = myapp.directory + myapp.fileList[myapp.index]
        index = myapp.listLijst.model().index(myapp.index)
        myapp.listLijst.setCurrentIndex(index)
        try:
            myapp.Data_read(myapp.filePath)
        except Exception as e:
            myapp.data_plot_Zeiss_ratio(myapp.filePath)

    def piek(self):
        self.piek_status = not self.piek_status
        if self.piek_status:
            QApplication.setOverrideCursor(QCursor(Qt.CrossCursor))
            try:
                self.cid = myapp.canvas.mpl_connect('button_press_event', myapp.pickon)
            except Exception:
                self.cid = myapp.canvas.mpl_connect('button_press_event', myapp.pickonRevamp)
        else:
            QApplication.restoreOverrideCursor()
            myapp.canvas.mpl_disconnect(self.cid)
        self._update_buttons_checked()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    try:
        os.remove('temp.pdf')
    except Exception:
        pass
    sys.exit(app.exec_())
