# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design-2.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(696, 673)
        Dialog.setStyleSheet("#Dialog{background:#D3D3D3}")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.Tab = QtWidgets.QTabWidget(Dialog)
        self.Tab.setMinimumSize(QtCore.QSize(678, 0))
        self.Tab.setStyleSheet("#tab {\n"
"background: #F5F5F5;\n"
"border: 1px solid gray\n"
"}")
        self.Tab.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.Tab.setObjectName("Tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setStyleSheet("#tab{border:2px solid gray}")
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.widget_2 = QtWidgets.QWidget(self.tab)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 490))
        self.widget_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.widget_2.setStyleSheet("#frame_2{background:#F5F5F5; border-left: 3px solid gray; border-right: 3px solid gray; border-bottom: 4px solid gray}")
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listLijst = QtWidgets.QListWidget(self.widget_2)
        self.listLijst.setMinimumSize(QtCore.QSize(0, 480))
        self.listLijst.setStyleSheet("#listLijst {\n"
"border: 2px solid gray;\n"
"border-radius: 10px;\n"
"background: white;\n"
"}")
        self.listLijst.setObjectName("listLijst")
        self.horizontalLayout.addWidget(self.listLijst)
        self.graphWindowLayout = QtWidgets.QVBoxLayout()
        self.graphWindowLayout.setContentsMargins(0, 10, 10, -1)
        self.graphWindowLayout.setObjectName("graphWindowLayout")
        self.horizontalLayout.addLayout(self.graphWindowLayout)
        self.verticalLayout.addWidget(self.widget_2)
        self.frame_3 = QtWidgets.QFrame(self.tab)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 100))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 84))
        self.frame_3.setStyleSheet("#frame_3{border-top: 4px solid gray; border-left:3px solid gray; border-right: 3px solid gray; background: #F5F5F5}")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame = QtWidgets.QFrame(self.frame_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setMinimumSize(QtCore.QSize(50, 25))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.SaveKnop = QtWidgets.QPushButton(self.frame)
        self.SaveKnop.setStyleSheet("#SaveKnop{background:white;border:2px solid gray}")
        self.SaveKnop.setObjectName("SaveKnop")
        self.verticalLayout_4.addWidget(self.SaveKnop)
        self.fileKnop = QtWidgets.QPushButton(self.frame)
        self.fileKnop.setMinimumSize(QtCore.QSize(50, 25))
        self.fileKnop.setStyleSheet("#fileKnop{background:white;border:2px solid gray}")
        self.fileKnop.setObjectName("fileKnop")
        self.verticalLayout_4.addWidget(self.fileKnop)
        self.horizontalLayout_2.addWidget(self.frame)
        self.tabWidget = QtWidgets.QTabWidget(self.frame_3)
        self.tabWidget.setMinimumSize(QtCore.QSize(520, 80))
        self.tabWidget.setStyleSheet("#tabWidget {\n"
"background: #F5F5F5;\n"
"border: 1px solid gray\n"
"}")
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setStyleSheet("")
        self.tab_3.setObjectName("tab_3")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_3)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.inputTable = QtWidgets.QTableWidget(self.tab_3)
        self.inputTable.setMinimumSize(QtCore.QSize(0, 50))
        self.inputTable.setStyleSheet("#inputTable{border:2px solid gray}")
        self.inputTable.setObjectName("inputTable")
        self.inputTable.setColumnCount(0)
        self.inputTable.setRowCount(0)
        self.verticalLayout_5.addWidget(self.inputTable)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.dataTable = QtWidgets.QTableWidget(self.tab_4)
        self.dataTable.setMinimumSize(QtCore.QSize(0, 50))
        self.dataTable.setMaximumSize(QtCore.QSize(16777215, 61))
        self.dataTable.setStyleSheet("#dataTable{border:2px solid gray}")
        self.dataTable.setObjectName("dataTable")
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.verticalLayout_2.addWidget(self.dataTable)
        self.dataTable.raise_()
        self.dataTable.raise_()
        self.tabWidget.addTab(self.tab_4, "")
        self.horizontalLayout_2.addWidget(self.tabWidget, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.frame_3)
        self.Tab.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.tab_2)
        self.tabWidget_2.setTabShape(QtWidgets.QTabWidget.Triangular)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.tab_5)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.viewTable_1 = QtWidgets.QTableWidget(self.tab_5)
        self.viewTable_1.setStyleSheet("#viewTable_1{border: 2px solid gray;\n"
"border-radius: 10px;\n"
"background: white;}")
        self.viewTable_1.setObjectName("viewTable_1")
        self.viewTable_1.setColumnCount(0)
        self.viewTable_1.setRowCount(0)
        self.verticalLayout_8.addWidget(self.viewTable_1)
        self.tabWidget_2.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.tab_6)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.viewTable_2 = QtWidgets.QTableWidget(self.tab_6)
        self.viewTable_2.setStyleSheet("#viewTable_2{border: 2px solid gray;\n"
"border-radius: 10px;\n"
"background: white;}")
        self.viewTable_2.setObjectName("viewTable_2")
        self.viewTable_2.setColumnCount(0)
        self.viewTable_2.setRowCount(0)
        self.verticalLayout_7.addWidget(self.viewTable_2)
        self.tabWidget_2.addTab(self.tab_6, "")
        self.verticalLayout_3.addWidget(self.tabWidget_2)
        self.Tab.addTab(self.tab_2, "")
        self.verticalLayout_6.addWidget(self.Tab)

        self.retranslateUi(Dialog)
        self.Tab.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.SaveKnop.setText(_translate("Dialog", "Save data table"))
        self.fileKnop.setText(_translate("Dialog", "Pick a folder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Dialog", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Dialog", "Tab 2"))
        self.Tab.setTabText(self.Tab.indexOf(self.tab), _translate("Dialog", "Data"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_5), _translate("Dialog", "Tab 1"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_6), _translate("Dialog", "Tab 2"))
        self.Tab.setTabText(self.Tab.indexOf(self.tab_2), _translate("Dialog", "Table"))
