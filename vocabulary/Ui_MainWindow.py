# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '文本提取单词.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QRect, QMetaObject,QCoreApplication
from PyQt5.QtWidgets import QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QLabel,QSpacerItem,QSizePolicy,QTableWidget,QStatusBar
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(833, 594)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_openfile = QPushButton(self.centralwidget)
        self.pushButton_openfile.setObjectName("pushButton_openfile")
        self.horizontalLayout.addWidget(self.pushButton_openfile)
        self.label_openfile = QLabel(self.centralwidget)
        self.label_openfile.setText("")
        self.label_openfile.setObjectName("label_openfile")
        self.horizontalLayout.addWidget(self.label_openfile)
        spacerItem = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_start = QPushButton(self.centralwidget)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_savepath = QPushButton(self.centralwidget)
        self.pushButton_savepath.setObjectName("pushButton_savepath")
        self.horizontalLayout_2.addWidget(self.pushButton_savepath)
        self.label_savepath = QLabel(self.centralwidget)
        self.label_savepath.setText("")
        self.label_savepath.setObjectName("label_savepath")
        self.horizontalLayout_2.addWidget(self.label_savepath)
        spacerItem1 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButton_learnedfile = QPushButton(self.centralwidget)
        self.pushButton_learnedfile.setObjectName("pushButton_learnedfile")
        self.horizontalLayout_2.addWidget(self.pushButton_learnedfile)
        self.label_learnedfile = QLabel(self.centralwidget)
        self.label_learnedfile.setText("")
        self.label_learnedfile.setObjectName("label_learnedfile")
        self.horizontalLayout_2.addWidget(self.label_learnedfile)
        spacerItem2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_download_audio = QPushButton(self.centralwidget)
        self.pushButton_download_audio.setObjectName("pushButton_download_audio")
        self.horizontalLayout_2.addWidget(self.pushButton_download_audio)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_openfile.setText(_translate("MainWindow", "打开文件"))
        self.pushButton_start.setText(_translate("MainWindow", "开始"))
        self.pushButton_savepath.setText(_translate("MainWindow", "保存路径"))
        self.pushButton_learnedfile.setText(_translate("MainWindow", "需要剔除的单词"))
        self.pushButton_download_audio.setText(_translate("MainWindow", "下载音频"))
