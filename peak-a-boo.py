import sys
import pandas
import os
import numpy as np
import peakutils
from math import factorial
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
Ui_MainWindow, QMainWindow = loadUiType('design.ui')
plt.style.use('ggplot')
dirPath = sys.path[0]

class MyApp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browse_folder)
        self.model = QtWidgets.QFileSystemModel()
        self.fig1 = Figure()
        self.canvas = FigureCanvas(self.fig1)
        self.canvas.setFocusPolicy(Qt.ClickFocus)

        self.canvas.setFocus()
        self.verticalLayout.addWidget(self.canvas)
        self.toolbar = MyToolbar(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)
        

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                       "Pick a folder")
        self.fileList = self.fileLister(directory)
        self.index = 0
        self.model.setRootPath(directory)
        self.treeView.setModel(self.model)
        self.treeView.setRootIndex(self.model.index(directory))
        filepath = self.treeView.clicked.connect(self.selected_file)
    
    def selected_file(self, index):
        indexItem = self.model.index(index.row(), 0, index.parent())
        filePath = self.model.filePath(indexItem)
        try:
            self.data_plot(filePath)
        except Exception as e:
            try:
                self.data_plot_Zeiss(filePath)
            except Exception as e:
                self.data_plot_Zeiss_ratio(filePath)
    
    def data_plot(self, filepath):
        self.fig1.clf()
        self.data = pandas.read_csv(filepath, "\t")[2:]
        try:
            del self.data["Unnamed: 3"]
        except Exception:
            pass
        self.data = self.data.drop_duplicates(subset='Time', keep='last')
        self.data["CFP"] = self.data["CFP"].str.replace(",", ".")
        self.data["YFP"] = self.data["YFP"].str.replace(",", ".")
        self.data["ratio"] = self.data["YFP"].astype("float") / self.data["CFP"].astype("float")
        self.datax = np.array(self.data.index.values)
        self.datay = np.array(self.data["ratio"])
        self.fig1.suptitle(filepath)
        self.indexes = peakutils.indexes(self.datay, thres=0.2, min_dist=200)
        try:
            self.indexes = peakutils.interpolate(self.datax, self.datay, ind=self.indexes)
        except Exception:
            pass
        self.indexes = [int(elem) for elem in self.indexes]
        self.blIndexes = [self.data['ratio'][elem-20:elem].idxmin() for elem in self.indexes]
        self.dataindex = self.data.loc[self.indexes]
        self.blYindexes = self.data.loc[self.blIndexes]
        self.datayIndex = np.array(self.dataindex["ratio"])
        self.datablIndex = np.array(self.blYindexes['ratio'])
        self.ax1f1 = self.fig1.add_subplot(211)
        self.ax1f2  = self.fig1.add_subplot(212)
        self.ax1f1.plot(self.datax, self.data.CFP.tolist(), label="CFP", marker="o", markevery=200)
        self.ax1f1.plot(self.datax, self.data.YFP.tolist(), label="YFP", marker="s", markevery=200)
        self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
        self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
        self.ax1f2.scatter(self.blIndexes, self.datablIndex, marker='o', color='g', s=40)
        self.ax1f2.set_xlim([0, max(self.datax)])
        self.ax1f1.set_xlim([0, max(self.datax)])
        self.ax1f2.set_xlabel("time (sec)")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        #self.canvas.mpl_connect('button_press_event', self.pickon)
        self.canvas.draw()
        #self.canvasPlot(fig1)
    
    def data_plot_Zeiss(self, filepath):
        self.fig1.clf()
        self.data = pandas.read_csv(filepath, "\t", header=3)
        del self.data["X.1"]
        try:
            del self.data["Unnamed: 3"]
        except Exception:
            pass
        self.data.columns = ["time", "YFP", "CFP"]
        self.data = self.data.drop_duplicates(subset='time', keep='last')
        self.data["ratio"] = self.data["YFP"].astype("float") / self.data["CFP"].astype("float")
        self.datax = np.array(self.data.index.values)
        self.datay = np.array(self.data["ratio"])
        self.fig1.suptitle(filepath)
        self.indexes = peakutils.indexes(self.datay, thres=0.2, min_dist=200)
        try:
            self.indexes = peakutils.interpolate(self.datax, self.datay, ind=self.indexes)
        except Exception:
            pass
        self.indexes = [int(elem) for elem in self.indexes]
        self.dataindex = self.data.loc[self.indexes]
        self.datayIndex = np.array(self.dataindex["ratio"])
        self.ax1f1 = self.fig1.add_subplot(211)
        self.ax1f2  = self.fig1.add_subplot(212)
        self.ax1f1.plot(self.datax, self.data.CFP.tolist(), label="CFP", marker="o", markevery=200)
        self.ax1f1.plot(self.datax, self.data.YFP.tolist(), label="YFP", marker="s", markevery=200)
        self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
        self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
        self.ax1f1.set_xlim([0, max(self.datax)])
        self.ax1f2.set_xlim([0, max(self.datax)])
        self.ax1f2.set_xlabel("time (sec)")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        #self.canvas.mpl_connect('button_press_event', self.pickon)
        self.canvas.draw()
        #self.canvasPlot(fig1)
    
    def data_plot_Zeiss_ratio(self, filepath):
        self.fig1.clf()
        self.data = pandas.read_csv(filepath, "\t", header=3)
        self.data = self.data.set_index("X")
        self.datax = [int(i) for i in self.data.index.values]
        self.datay = np.array(self.data["Y"])
        self.fig1.suptitle(filepath)
        self.indexes = peakutils.indexes(self.datay, thres=0.2, min_dist=200)
        try:
            self.indexes = peakutils.interpolate(self.datax, self.datay, ind=self.indexes)
        except Exception:
            pass
        self.indexes = [int(elem) for elem in self.indexes]
        self.dataindex = self.data.loc[self.indexes]
        self.datayIndex = np.array(self.dataindex["Y"])
        self.ax1f1 = self.fig1.add_subplot(111)
        self.ax1f1.plot(self.datax, self.datay, label="ratio")
        self.ax1f1.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
        self.ax1f1.set_xlim([0, max(self.datax)])
        self.ax1f1.set_xlabel("time (sec)")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        #self.canvas.mpl_connect('button_press_event', self.pickonRevamp)
        self.canvas.draw()
    
    def savitzky_golay(self, y, window_size, order, deriv=0, rate=1):
        try:
            window_size = np.abs(np.int(window_size))
            order = np.abs(np.int(order))
        except ValueError:
            raise ValueError("window_size and order have to be of type int")
        if window_size % 2 != 1 or window_size < 1:
            raise TypeError("window_size size must be a positive odd number")
        if window_size < order + 2:
            raise TypeError("window_size is too small for the polynomials order")
        order_range = range(order+1)
        half_window = (window_size -1) // 2
        # precompute coefficients
        b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
        m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
        # pad the signal at the extremes with
        # values taken from the signal itself
        firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
        lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
        y = np.concatenate((firstvals, y, lastvals))
        return np.convolve( m[::-1], y, mode='valid')
    
    def pickon(self, event):
        if event.button == 1:
            indexi = list(self.indexes)
            blIndexi = list(self.blIndexes)
            indexi.append(int(event.xdata))
            blIndexi.append(self.data['ratio'][int(event.xdata)-20:int(event.xdata)].idxmin())
            indexi.sort()
            blIndexi.sort()
            self.indexes = np.array(indexi)
            self.blIndexes = np.array(blIndexi)
            self.dataindex = self.data.loc[indexi]
            self.datablIndex = np.array(self.data.loc[blIndexi]['ratio'])
            self.datayIndex = np.array(self.dataindex["ratio"])
            self.ax1f2.clear()
            self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
            self.ax1f2.scatter(indexi, self.datayIndex, marker='*', color='r', s=40)
            self.ax1f2.scatter(blIndexi, self.datablIndex, marker='o', color='g', s=40)
            self.ax1f2.set_xlim([0, max(self.datax)])
            self.canvas.draw()
        elif event.button == 3:
            rapo = range(int(event.xdata)-10, int(event.xdata)+10)
            po = [el for el in self.indexes if el in rapo]
            indexi = list(self.indexes)
            blindexi = list(self.blIndexes)
            try:
                ind = indexi.index(po[0])
                indexi.remove(po[0])
                blindexi.pop(ind)
            except Exception as e:
                pass
            self.indexes = np.array(indexi)
            self.blIndexes = np.array(blindexi)
            self.dataindex = self.data.loc[indexi]
            self.datayIndex = np.array(self.dataindex["ratio"])
            self.datablIndex = np.array(self.data.loc[blindexi]['ratio'])
            self.ax1f2.clear()
            self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
            self.ax1f2.scatter(indexi, self.datayIndex, marker='*', color='r', s=40)
            self.ax1f2.scatter(blindexi, self.datablIndex, marker='o', color='g', s=40)
            self.ax1f2.set_xlim([0, max(self.datax)])
            self.canvas.draw()
    
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
        
    def baseLine(self, event):
        if event.button == 1:
            if len(self.indexes) == len(self.blIndexes):
                print("there is no piek for a baseline marker")
            else:
                blIndexi = list(self.blIndexes)
                blIndexi.append(int(event.xdata))
                blIndexi.sort()
                self.blIndexes = np.array(blIndexi)
                self.datablIndex = np.array(self.data.loc[blIndexi]['ratio'])
                self.ax1f2.clear()
                self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
                self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
                self.ax1f2.scatter(blIndexi, self.datablIndex, marker='o', color='g', s=40)
                self.ax1f2.set_xlim([0, max(self.datax)])
                self.canvas.draw()
        elif event.button == 3:
            rapo = range(int(event.xdata)-10, int(event.xdata)+10)
            po = [el for el in self.blIndexes if el in rapo]
            blIndexi = list(self.blIndexes)
            try:
                blIndexi.remove(po[0])
            except Exception:
                pass
            self.blIndexes = np.array(blIndexi)
            self.datablIndex = np.array(self.data.loc[blIndexi]['ratio'])
            self.ax1f2.clear()
            self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
            self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
            self.ax1f2.scatter(blIndexi, self.datablIndex, marker='o', color='g', s=40)
            self.ax1f2.set_xlim([0, max(self.datax)])
            self.canvas.draw()


    def fileLister(self, dirPath):
        filelist = []
        for root, dirs, files in os.walk(dirPath):
            for file in files:
                if file.endswith(".txt"):
                    filelist.append(os.path.join(root, file))
        
        return filelist

class MyToolbar(NavigationToolbar):
    def __init__(self, figure_canvas, parent= None):
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
            ('piek', 'set and remove piek marker', dirPath + '\piek', 'piek_selector'),
            ('baseline', 'set and remove baseline marker', dirPath + '\\baseline', 'baseline_selector')
            )
        self.piek_status = False
        self.baseline_status = False

        NavigationToolbar.__init__(self, figure_canvas, parent= None)

    def print_plot(self):
        pp=PdfPages('temp.pdf')
        size = myapp.fig1.get_size_inches()
        print(size)
        myapp.fig1.set_size_inches(11.69,8.27)
        pp.savefig(myapp.fig1)
        myapp.fig1.set_size_inches(8.925, 4.6875)
        myapp.removePlot()
        myapp.canvasPlot(myapp.fig1)
        pp.close()
        os.startfile("temp.pdf", "print")
    
    def delete_plot(self):
        del myapp.fileList[myapp.index]
        try:
            myapp.data_plot(myapp.fileList[myapp.index])
        except Exception:
            try:
                myapp.data_plot_Zeiss(myapp.fileList[myapp.index])
            except Exception:
                myapp.data_plot_Zeiss_ratio(myapp.fileList[myapp.index])
    
    def newForward(self):
        myapp.index += 1
        if myapp.index > len(myapp.fileList) - 1:
            myapp.index = 0
        try:
            myapp.data_plot(myapp.fileList[myapp.index])
        except Exception:
            try:
                myapp.data_plot_Zeiss(myapp.fileList[myapp.index])
            except Exception:
                myapp.data_plot_Zeiss_ratio(myapp.fileList[myapp.index])

    def newBack(self):
        myapp.index += -1
        if myapp.index < 0:
            myapp.index = len(myapp.fileList) - 1
        try:
            myapp.data_plot(myapp.fileList[myapp.index])
        except Exception:
            try:
                myapp.data_plot_Zeiss(myapp.fileList[myapp.index])
            except Exception:
                myapp.data_plot_Zeiss_ratio(myapp.fileList[myapp.index])
    
    def piek_selector(self):
        self.piek_status = not self.piek_status
        if self.piek_status:
            try:
                self.cid = myapp.canvas.mpl_connect('button_press_event', myapp.pickon)
            except Exception:
                self.cid = myapp.canvas.mpl_connect('button_press_event', myapp.pickonRevamp)
        else:
            myapp.canvas.mpl_disconnect(self.cid)
    
    def baseline_selector(self):
        self.baseline_status = not self.baseline_status
        if self.baseline_status:
            self.cid = myapp.canvas.mpl_connect('button_press_event', myapp.baseLine)
        else:
            myapp.canvas.mpl_disconnect(self.cid)


if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    try:
        os.remove('temp.pdf')
    except Exception:
        pass
    sys.exit(app.exec_())