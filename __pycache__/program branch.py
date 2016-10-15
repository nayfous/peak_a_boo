import sys
import pandas
import numpy as np
import os
#import peakutils
from math import factorial
from PyQt5 import QtWidgets
from PyQt5.uic import loadUiType
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
Ui_MainWindow, QMainWindow = loadUiType('design.ui')

class MyApp(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browse_folder)
        self.model = QtWidgets.QFileSystemModel()
        fig = Figure()
        self.canvasPlot(fig)
        

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
        except Exception:
            try:
                self.data_plot_Zeiss(filePath)
            except Exception:
                self.data_plot_Zeiss_ratio(filePath)
    
    def data_plot(self, filepath):
        data = pandas.read_csv(filepath, "\t")[2:]
        try:
            del data["Unnamed: 3"]
        except Exception:
            print()
        data = data.drop_duplicates(subset='Time', keep='last')
        data["CFP"] = data["CFP"].str.replace(",", ".")
        data["YFP"] = data["YFP"].str.replace(",", ".")
        data["ratio"] = data["YFP"][2:].astype("float") / data["CFP"][2:].astype("float")
        datax = [int(i) for i in data.index.values]
        datay = np.array(data["ratio"])
        datayHat = self.savitzky_golay(datay, 51, 3)
        self.removePlot()
        fig1 = Figure()
        fig1.suptitle(filepath)
        #indexes = peakutils.indexes(datay, thres=0.2, min_dist=200)
        #indexes = peakutils.interpolate(datax, datay, ind=indexes)
        self.ax1f1 = fig1.add_subplot(211)
        self.ax1f2  = fig1.add_subplot(212)
        self.ax1f2.plot(datax, datay, label="ratio")#, marker="*", markevery=list(indexes), markersize=10, mec="r", mew=2.0)
        self.ax1f1.plot(datax, data.CFP.tolist(), label="CFP")
        self.ax1f1.plot(datax, data.YFP.tolist(), label="YFP")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.canvasPlot(fig1)
    
    def data_plot_Zeiss(self, filepath):
        data = pandas.read_csv(filepath, "\t", header=3)
        del data["X.1"]
        try:
            del data["Unnamed: 3"]
        except Exception:
            print()
        data.columns = ["time", "YFP", "CFP"]
        data = data.set_index("time")
        data["ratio"] = data["YFP"][2:].astype("float") / data["CFP"][2:].astype("float")
        datax = [int(i) for i in data.index.values]
        datay = np.array(data["ratio"])
        datayHat = self.savitzky_golay(datay, 51, 3)
        self.removePlot()
        fig1 = Figure()
        fig1.suptitle(filepath)
        #indexes = peakutils.indexes(datay, thres=0.2, min_dist=200)
        #indexes = peakutils.interpolate(datax, datay, ind=indexes)
        self.ax1f1 = fig1.add_subplot(211)
        self.ax1f2  = fig1.add_subplot(212)
        self.ax1f2.plot(datax, datay, label='ratio')#, marker="*", markevery=list(indexes), markersize=10, mec="r", mew=2.0)
        self.ax1f1.plot(datax, data.CFP.tolist(), label="CFP")
        self.ax1f1.plot(datax, data.YFP.tolist(), label="YFP")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        self.canvasPlot(fig1)
    
    def data_plot_Zeiss_ratio(self, filepath):
        data = pandas.read_csv(filepath, "\t", header=3)
        data = data.set_index("X")
        datax = [int(i) for i in data.index.values]
        datay = np.array(data["Y"])
        datayHat = self.savitzky_golay(datay, 51, 3)
        self.removePlot()
        fig1 = Figure()
        fig1.suptitle(filepath)
        self.ax1f1 = fig1.add_subplot(111)
        self.ax1f1.plot(datax, datay, label="ratio")
        self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True) 
        self.canvasPlot(fig1)

    def canvasPlot(self, fig):
        self.canvas = FigureCanvas(fig)
        self.verticalLayout.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = MyToolbar(self.canvas)
        self.verticalLayout.addWidget(self.toolbar)
    
    def removePlot(self):
        self.verticalLayout.removeWidget(self.canvas)
        self.canvas.close()
        self.verticalLayout.removeWidget(self.toolbar)
        self.toolbar.close()
    
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
            ('print', 'print plot', 'print', 'print_plot'),
            )

        NavigationToolbar.__init__(self, figure_canvas, parent= None)

    def print_plot(self):
        print("je hebt de print knop gedrukt")
    
    def newForward(self):
        print(self.fileList[self.index])
        self.index += 1
        if self.index > len(self.fileList) - 1:
            self.index = 0
        try:
            self.data_plot(self.fileList[self.index])
        except Exception:
            try:
                self.data_plot_Zeiss(self.fileList[self.index])
            except Exception:
                self.data_plot_Zeiss_ratio(self.fileList[self.index])

    def newBack(self):
        self.index += -1
        if self.index < 0:
            self.index = len(self.fileList) - 1
        try:
            self.data_plot(self.fileList[self.index])
        except Exception:
            try:
                self.data_plot_Zeiss(self.fileList[self.index])
            except Exception:
                self.data_plot_Zeiss_ratio(self.fileList[self.index])



if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyApp()
    myapp.show()
    sys.exit(app.exec_())