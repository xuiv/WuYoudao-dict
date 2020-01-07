# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QTableWidgetItem
from PyQt5.QtGui import QFont,QColor
from PyQt5.QtCore import Qt,QDir
from Ui_MainWindow import Ui_MainWindow

from vocabulary import vocabulary
from pandas import DataFrame
import traceback
import threading
import os
class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)
        self.setupUi(self)
        self.file = ''
        self.learned_word_file = ''
        self.savepath = './'

        self.setWindowTitle('文本提词')

        #连接信号与槽
        self.pushButton_openfile.clicked.connect(self.openfile)#打开文本文件(utf-8)
        self.pushButton_savepath.clicked.connect(self.change_save_path)#改变保存路径
        self.pushButton_learnedfile.clicked.connect(self.openlearnedfile)#打开简单词汇文件（utf-8）
        self.pushButton_start.clicked.connect(self.run)#生成单词本
        self.tableWidget.cellClicked.connect(self.listen_one_new)#播放发音
        self.pushButton_download_audio.clicked.connect(self.download_audio)

    def openfile(self):
        #打开文件
        filename, _ = QFileDialog.getOpenFileName(self,'Open file','D:\\','Txt files(*.txt)')
        #print(filename)
        self.label_openfile.setText(filename)
        self.file = filename
    def change_save_path(self):
        #修改保存路径
        directory = QFileDialog.getExistingDirectory(self,'选取文件夹',self.savepath)
        self.savepath = QDir.toNativeSeparators(directory)# 路径以windows支持的显示方式进行显示。
        self.label_savepath.setText(self.savepath)
    def openlearnedfile(self):
        filename, _ = QFileDialog.getOpenFileName(self,'Open file','D:\\','Txt files(*.txt)')
        self.label_learnedfile.setText(filename)
        self.learned_word_file = filename
    def run(self):
        self.statusBar().showMessage('正在查词......')
        self.vocabulary = vocabulary(file=self.file,learned_words_file=self.learned_word_file,save_path=self.savepath)
        data = self.vocabulary.run()
        if data:
            self.show_tablewidget(data)
            self.vocabulary.write_words(self.data)
    def show_tablewidget(self, dict_data):
        '''在tableWidget显示dict_data'''
        tableWidget = self.tableWidget
        '''排序'''
        df = DataFrame(dict_data).sort_values(by='count',ascending = False)
        _temp = df.to_dict('index')
        dict_data = list(_temp.values())
        self.data = dict_data
        '''tableWidget的初始化'''
        list_col = ['key','count','ps','pron','pos','acceptation','sen']
        len_col = len(list_col)
        len_index = len(dict_data)
        tableWidget.setRowCount(len_index)#设置行数
        tableWidget.setColumnCount(len_col)#设置列数
        tableWidget.setHorizontalHeaderLabels(['单词', '词频', '音标','发音','词性','释义','例句']) # 设置垂直方向上的名字
        tableWidget.setVerticalHeaderLabels([str(i) for i in range(1, len_index + 1)]) # 设置水平方向上的名字
        '''填充数据'''
        for index in  range(len_index):
            for col in range(len_col):
                name_col = list_col[col]
                if name_col == 'pron':
                    item = QTableWidgetItem('播放')
                    item.setTextAlignment(Qt.AlignCenter)
                    font = QFont()
                    font.setBold(True)
                    font.setWeight(75)
                    item.setFont(font)
                    item.setBackground(QColor(218, 218, 218))
                    item.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
                    tableWidget.setItem(index, col, item)
                else:
                    tableWidget.setItem(index,col,QTableWidgetItem(str(dict_data[index][name_col])))
        tableWidget.resizeColumnsToContents()
        tableWidget.setColumnWidth(5, 500)
    def listen_one_new(self,row,column):
        if column == 3:
            download_one = self.data[row]
            listen_thread = threading.Thread(target = self.listen_one_new_thread,args=(download_one,),daemon=True)
            listen_thread.start()
    def listen_one_new_thread(self,download_one):
        key = download_one['key']
        url = download_one['pron']
        self.vocabulary.download_audio_one(key,url)
        filename = self.savepath + os.path.sep + 'audio' + os.sep + key + '.mp3'
        print(os.path.abspath(filename))
        os.system(os.path.abspath(filename))
    def download_audio(self):
        self.statusBar().showMessage('音频下载中...')
        try:
            self.vocabulary.download_audio(self.data)
            self.statusBar().showMessage('音频下载成功')
        except:
            self.statusBar().showMessage('音频下载失败')

if __name__=='__main__':
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
