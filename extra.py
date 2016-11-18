    # def baseline_selector(self):
    #     self.baseline_status = not self.baseline_status
    #     if self.baseline_status:
    #         self.cid = myapp.canvas.mpl_connect('button_press_event', myapp.baseLine)
    #     else:
    #         myapp.canvas.mpl_disconnect(self.cid)

        #niet meer nodig    
    # def baseLine(self, event):
    #     if event.button == 1:
    #         if len(self.indexes) == len(self.blIndexes):
    #             print("there is no piek for a baseline marker")
    #         else:
    #             blIndexi = list(self.blIndexes)
    #             blIndexi.append(int(event.xdata))
    #             blIndexi.sort()
    #             self.blIndexes = np.array(blIndexi)
    #             self.dataMemory[self.filePath][1] = self.blIndexes
    #             self.datablIndex = np.array(self.data.loc[blIndexi]['ratio'])
    #             self.ax1f2.clear()
    #             self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
    #             self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
    #             self.ax1f2.scatter(blIndexi, self.datablIndex, marker='o', color='g', s=40)
    #             self.ax1f2.set_xlim([0, max(self.datax)])
    #             self.canvas.draw()
    #     elif event.button == 3:
    #         rapo = range(int(event.xdata)-10, int(event.xdata)+10)
    #         po = [el for el in self.blIndexes if el in rapo]
    #         blIndexi = list(self.blIndexes)
    #         try:
    #             blIndexi.remove(po[0])
    #         except Exception:
    #             pass
    #         self.blIndexes = np.array(blIndexi)
    #         self.dataMemory[self.filePath][1] = self.blIndexes
    #         self.datablIndex = np.array(self.data.loc[blIndexi]['ratio'])
    #         self.ax1f2.clear()
    #         self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
    #         self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
    #         self.ax1f2.scatter(blIndexi, self.datablIndex, marker='o', color='g', s=40)
    #         self.ax1f2.set_xlim([0, max(self.datax)])
    #         self.canvas.draw()

                # ('baseline', 'set and remove baseline marker', dirPath + '\\baseline', 'baseline_selector')
    
        # def data_plot(self, filepath):
        # self.fig1.clf()
        # self.data = pandas.read_csv(filepath, "\t")[2:]
        # self.data['Time'] = self.data['Time'].astype(int)
        # self.data = self.data.set_index('Time')
        # try:
        #     del self.data["Unnamed: 3"]
        # except Exception:
        #     pass
        # self.data = self.data.replace(to_replace=",", value=".", regex=True)
        # self.data["ratio"] = self.data["YFP"].astype("float") / self.data["CFP"].astype("float")
        # self.datax = np.array(self.data.index.values)
        # print(self.data.index.values)
        # self.datay = np.array(self.data["ratio"])
        # self.fig1.suptitle(filepath)
        
        # try:
        #     self.indexes = self.dataMemory[filepath][0]
        #     self.blIndexes = self.dataMemory[filepath][1]
        # except Exception:
        #     self.indexes = peakutils.indexes(self.datay, thres=0.2, min_dist=200)
        #     try:
        #         self.indexes = peakutils.interpolate(self.datax, self.datay, ind=self.indexes)
        #     except Exception:
        #         pass
        #     print(self.indexes)
        #     self.indexes = [int(elem) for elem in self.indexes]
        #     self.blIndexes = [self.data['ratio'][elem-20:elem].idxmin() for elem in self.indexes if elem > 20]
        #     self.dataMemory[filepath] = [self.indexes, self.blIndexes]
        
        # self.dataindex = self.data['ratio'].iloc[self.indexes]
        # print(self.dataindex)
        # self.blYindexes = self.data['ratio'].loc[self.blIndexes]
        # self.datayIndex = np.array(self.dataindex)
        # self.datablIndex = np.array(self.blYindexes)
        # #piekHeight = self.datayIndex - self.datablIndex
        # #self.piekHeight[filepath] = piekHeight
        # #print(pandas.DataFrame.from_dict(self.piekHeight, orient='index'))
        # self.ax1f1 = self.fig1.add_subplot(211)
        # self.ax1f2  = self.fig1.add_subplot(212)
        # self.ax1f1.plot(self.datax, self.data.CFP.tolist(), label="CFP", marker="o", markevery=200)
        # self.ax1f1.plot(self.datax, self.data.YFP.tolist(), label="YFP", marker="s", markevery=200)
        # self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
        # #self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
        # #self.ax1f2.scatter(self.blIndexes, self.datablIndex, marker='o', color='g', s=40)
        # self.ax1f2.set_xlim([0, max(self.datax)])
        # self.ax1f1.set_xlim([0, max(self.datax)])
        # self.ax1f2.set_xlabel("time (sec)")
        # self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        # self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        # self.canvas.mpl_connect('button_press_event', self.pickon)
        # self.canvas.draw()
    
    # def data_plot_Zeiss(self, filepath):
        # print("neeeeeeeeee")
        # self.fig1.clf()
        # self.data = pandas.read_csv(filepath, "\t")#, header=3)
        # with open(filepath, 'r') as f:
        #     print(f.readline())
        # print(pandas.DataFrame(list(self.data["2"][3:])))
        # del self.data["X.1"]
        # try:
        #     del self.data["Unnamed: 3"]
        # except Exception:
        #     pass
        # self.data.columns = ["time", "YFP", "CFP"]
        # self.data['time'] = self.data['time'].astype(int)
        # self.data = self.data.drop_duplicates(subset='time', keep='last')
        # self.data = self.data.set_index('time')
        # self.data["ratio"] = self.data["YFP"].astype("float") / self.data["CFP"].astype("float")
        # self.datax = np.array(self.data.index.values)
        # self.datay = np.array(self.data["ratio"])
        # self.fig1.suptitle(filepath)
        
        # try:
        #     self.indexes = self.dataMemory[filepath][0]
        #     self.blIndexes = self.dataMemory[filepath][1]
        # except Exception:
        #     self.indexes = peakutils.indexes(self.datay, thres=0.2, min_dist=200)
        #     try:
        #         self.indexes = peakutils.interpolate(self.datax, self.datay, ind=self.indexes)
        #     except Exception:
        #         pass
        #     self.indexes = [int(elem) for elem in self.indexes]
        #     self.blIndexes = [self.data['ratio'][elem-20:elem].idxmin() for elem in self.indexes if elem > 20]
        #     self.dataMemory[filepath] = [self.indexes, self.blIndexes]

        # self.dataindex = self.data.loc[self.indexes]
        # self.datayIndex = np.array(self.dataindex["ratio"])
        # self.blYindexes = self.data['ratio'].loc[self.blIndexes]
        # self.blYindexes = np.array(self.blYindexes)
        # piekHeight = self.datayIndex - self.datablIndex
        # self.piekHeight[filepath] = piekHeight
        # self.ax1f1 = self.fig1.add_subplot(211)
        # self.ax1f2  = self.fig1.add_subplot(212)
        # self.ax1f1.plot(self.datax, self.data.CFP.tolist(), label="CFP", marker="o", markevery=200)
        # self.ax1f1.plot(self.datax, self.data.YFP.tolist(), label="YFP", marker="s", markevery=200)
        # self.ax1f2.plot(self.datax, self.datay, alpha=0.5, label='ratio')
        # self.ax1f2.scatter(self.indexes, self.datayIndex, marker='*', color='r', s=40)
        # self.ax1f2.scatter(self.blIndexes, self.blYindexes, marker='o', color='g', s=40)
        # self.ax1f1.set_xlim([0, max(self.datax)])
        # self.ax1f2.set_xlim([0, max(self.datax)])
        # self.ax1f2.set_xlabel("time (sec)")
        # self.ax1f1.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        # self.ax1f2.legend(loc="upper left", prop={'size':10}, bbox_to_anchor=(0.95, 1.10), fancybox=True, shadow=True)
        # self.canvas.mpl_connect('button_press_event', self.pickon)
        # self.canvas.draw()