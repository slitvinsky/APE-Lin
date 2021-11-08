import re
import sys
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtWidgets import qApp, QFileDialog, QMessageBox, QTableWidgetItem, QWidget, QVBoxLayout, QStyle
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QPixmap
import design
import insert
import togroup
import about
import openurl
import subprocess
import requests


class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.doubleClicked.connect(self.TableClick)
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setHorizontalHeaderLabels(["Название", "Группа", "URL"])
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Группа", "URL"])
        self.action_Quit.triggered.connect(qApp.quit)
        self.action_Open.triggered.connect(self.getFileName)
        self.actionSave.triggered.connect(self.saveFile)
        self.action_About.triggered.connect(self.msgabout)
        self.clearButton.clicked.connect(self.clearoffline)
        self.actionNew.triggered.connect(self.clearTableNew)
        self.openFromUrl.triggered.connect(self.showFromUrl)
        self.testButton.clicked.connect(self.checkStatus)
        self.insertButton.clicked.connect(self.showInsert)
        self.moveButton.clicked.connect(self.moveString)
        self.deleteButton.clicked.connect(self.deleteRow)
        self.moveallButton.clicked.connect(self.moveAll)
        self.groupButton.clicked.connect(self.showToGroup)
        self.lineEdit.returnPressed.connect(self.searchItem)
        self.moveUpButton.clicked.connect(self.moveUp)
        self.moveDownButton.clicked.connect(self.moveDown)
        self.winsert = None
        self.player = None
        self.wtogroup = None
        self.label.setText('Каналов: ')
        self.label_2.setText('Каналов: ')
        self.setStyleSheet('background-color: #636363;color: #fff;')
        #self.groupButton.setStyleSheet('background: #9da399; color: black; border-style: solid; border-width: 1.5px; border-radius: 8px')
        self.groupButton.setToolTip('Добавить выбранные каналы в группу')
        #self.insertButton.setStyleSheet('background: #9da399; color: black; border-style: solid; border-width: 1.5px; border-radius: 8px')
        self.insertButton.setToolTip('Добавить канал')
        #self.testButton.setStyleSheet('background: #9da399; color: black; border-style: solid; border-radius: 8px; border-width: 1.5px')
        self.testButton.setToolTip('Тестирование каналов')
        #self.deleteButton.setStyleSheet('background: #9da399; color: black; border-style: solid; border-radius: 8px; border-width: 1.5px')
        self.deleteButton.setToolTip('Удалить выбранные каналы')
        self.offlinelabel.setStyleSheet('color: red')
        self.moveButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.moveUpButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowUp))
        self.moveDownButton.setIcon(self.style().standardIcon(QStyle.SP_ArrowDown))
        self.testButton.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        self.moveButton.setStyleSheet('background: #9da399; border-style: solid; border-radius: 8px; border-width: 1.5px')
        self.moveallButton.setStyleSheet('background: #9da399; border-style: solid; border-radius: 8px; border-width: 1.5px')
        #self.searchButton.setStyleSheet('background: #9da399; color: white; border-style: solid; border-radius: 8px; border-width: 1.5px')
        self.searchButton.clicked.connect(self.searchItem)
        self.tableWidget.setStyleSheet('background-color: #9da399;color: #000;border-style: none; border-radius: 8px')
        self.tableWidget_2.setStyleSheet('background-color: #9da399;color: #000;border-style: none; border-radius: 8px')
        self.progressBar.setStyleSheet('background: #9da399; border-style: none; border-radius: 8px')
        self.progressBar.setStyleSheet("QProgressBar::chunk "
                      "{"
                      "background-color: #9da399;"
                      "}")
        self.lineEdit.setStyleSheet('background: #9da399; border-style: none; border-radius: 8px')
        self.progressBar.setVisible(False)
        self.testButton.setEnabled(False)
        self.groupButton.setEnabled(False)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.clearButton.setVisible(False)

    def clearoffline(self):
        indexes = sorted(self.offlinechannels, reverse=True)
        for rowidx in indexes:
            self.tableWidget.removeRow(rowidx)
        self.clearButton.setVisible(False)
        self.label.setText('Каналов: ' + str(self.tableWidget.rowCount()))
        self.offlinelabel.setVisible(False)
        self.onlinelabel.setVisible(False)
    def moveDown(self):
        row = self.tableWidget_2.currentRow()
        column = self.tableWidget_2.currentColumn();
        if row < self.tableWidget_2.rowCount() - 1:
            self.tableWidget_2.insertRow(row + 2)
            for i in range(self.tableWidget_2.columnCount()):
                self.tableWidget_2.setItem(row + 2, i, self.tableWidget_2.takeItem(row, i))
                self.tableWidget_2.setCurrentCell(row + 2, column)
            self.tableWidget_2.removeRow(row)

    def moveUp(self):
        row = self.tableWidget_2.currentRow()
        column = self.tableWidget_2.currentColumn();
        if row > 0:
            self.tableWidget_2.insertRow(row - 1)
            for i in range(self.tableWidget_2.columnCount()):
                self.tableWidget_2.setItem(row - 1, i, self.tableWidget_2.takeItem(row + 1, i))
                self.tableWidget_2.setCurrentCell(row - 1, column)
            self.tableWidget_2.removeRow(row + 1)
    def getFileName(self):
        self.progressBar.setValue(0)
        self.tableWidget.clear()
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["Название", "Группа", "URL"])
        self.fname = QFileDialog.getOpenFileName(self, 'Open file', '/home',"Playlist (*.m3u *.m3u8)")[0]
        try:
            self.my_file = open(self.fname, 'r')
        except FileNotFoundError:
            pass
        else:
            self.tableAction()
    def saveFile(self):
        try:
            self.filename = QFileDialog.getSaveFileName(self, 'Save File','/home',"Playlist(*.m3u8)")[0]
            with open(self.filename, "wt") as file:
                channelcount = str(self.tableWidget_2.rowCount())
                file.write('#EXTM3U\n')
                for i in range(int(channelcount)):
                    file.write('#EXTINF:0,' + self.tableWidget_2.item(i, 0).text() + \
                               '\n' + '#EXTGRP:' + self.tableWidget_2.item(i, 1).text() \
                               + '\n' + self.tableWidget_2.item(i, 2).text() + '\n')
        except FileNotFoundError:
            pass
    def moveString(self):
        if not self.tableWidget.selectedItems():
            return
        self.groupButton.setEnabled(True)
        rowtwo = []
        for ItemVal in self.tableWidget.selectedIndexes():
            rowtwo.append(ItemVal.row())
        urows = set(rowtwo)
        frows = (list(urows))
        nrows = 0
        for i in frows:
            self.tableWidget_2.setRowCount(self.tableWidget_2.rowCount() + 1)
            rows = self.tableWidget_2.rowCount() - 1
            self.tableWidget_2.setItem(rows, 0, QTableWidgetItem(self.tableWidget.item(frows[nrows], 0)))
            self.tableWidget_2.setItem(rows, 1, QTableWidgetItem(self.tableWidget.item(frows[nrows], 1)))
            self.tableWidget_2.setItem(rows, 2, QTableWidgetItem(self.tableWidget.item(frows[nrows], 2)))
            self.tableWidget_2.resizeColumnToContents(0)
            self.tableWidget_2.resizeColumnToContents(1)
            nrows += 1
        self.label_2.setText('Каналов: ' + str(rows + 1))
    def deleteRow(self):
        self.sel_items = []
        for i in self.tableWidget_2.selectedItems():
            self.sel_items.append(i.row())
        indexes_items = sorted(set(self.sel_items), reverse=True)
        try:
            for ItemVal in indexes_items:
                # rows = ItemVal.row()
                # print(self.sel_items[ItemVal])
                self.tableWidget_2.removeRow(ItemVal)
        except TypeError:
            pass
        self.label_2.setText('Каналов: ' + str(self.tableWidget_2.rowCount()))
    def searchItem(self):
        self.tableWidget.setSelectionMode(self.tableWidget.MultiSelection)
        result = []
        rows = self.tableWidget.rowCount()
        for i in range(rows):
            result.append(self.tableWidget.item(i,0).text())
        s = self.lineEdit.text()
        s_list = self.tableWidget.findItems(s,QtCore.Qt.MatchContains)
        row = []
        try:
            for i in range(len(s_list)):
                row.append(self.tableWidget.row(s_list[i]))
            row.reverse()
            for s in range(len(s_list)):
                self.tableWidget.selectRow(row[s])
        except:
            pass
        self.tableWidget.setSelectionMode(self.tableWidget.ExtendedSelection)
    def moveAll(self):
        self.groupButton.setEnabled(True)
        rowstwo = self.tableWidget_2.rowCount()
        rows = self.tableWidget.rowCount()
        self.tableWidget_2.setRowCount(rows + rowstwo)

        try:
            for i in range(rows):
                #print(i)
                name = self.tableWidget.item(i, 0).text()
                group = self.tableWidget.item(i, 1).text()
                url = self.tableWidget.item(i, 2).text()
                self.tableWidget_2.setItem(i+rowstwo, 0, QTableWidgetItem(name))
                self.tableWidget_2.setItem(i+rowstwo, 1, QTableWidgetItem(group))
                self.tableWidget_2.setItem(i+rowstwo, 2, QTableWidgetItem(url))
                self.tableWidget_2.item(i+rowstwo, 0).setBackground(QtGui.QColor(198, 201, 195))
                self.tableWidget_2.item(i+rowstwo, 1).setBackground(QtGui.QColor(218, 222, 215))
                self.tableWidget_2.item(i+rowstwo, 2).setBackground(QtGui.QColor(235, 235, 235))
        except AttributeError:
            pass
        self.label_2.setText('Каналов: ' + str(self.tableWidget_2.rowCount()))
        self.tableWidget_2.resizeColumnToContents(0)
        self.tableWidget_2.resizeColumnToContents(1)
    def checkStatus(self):
        self.offlinechannels = []
        self.progressBar.setVisible(True)
        channelcount = str(self.tableWidget.rowCount())
        self.progressBar.setMaximum(int(channelcount)-1)
        online_list = []
        offline_list = []
        for i in range(int(channelcount)):
            QtWidgets.qApp.processEvents()
            time.sleep(1)
            try:
                process = subprocess.run(
                    ['tools/./ffprobe', self.tableWidget.item(i, 2).text(), '-v', 'error', '-show_format'],
                    capture_output=True, text=True, timeout=10)
                check = re.compile(r'''format_name''').findall(process.stdout)
                if len(check) == 0:
                    self.tableWidget.item(i, 0).setBackground(QtGui.QColor(255, 110, 110))
                    self.progressBar.setValue(i)
                    offline_list.append('offline')
                    self.offlinechannels.append(i)
                else:
                    self.tableWidget.item(i, 0).setBackground(QtGui.QColor(96, 252, 143))
                    self.progressBar.setValue(i)
                    online_list.append('online')
            except:
                self.tableWidget.item(i, 0).setBackground(QtGui.QColor(255, 110, 110))
                self.progressBar.setValue(i)
                offline_list.append('offline')
                self.offlinechannels.append(i)
        self.tableWidget.resizeColumnToContents(0)
        self.tableWidget.resizeColumnToContents(1)
        self.onlinelabel.setVisible(True)
        self.offlinelabel.setVisible(True)
        self.onlinelabel.setText('Online: ' + str(len(online_list)))
        self.offlinelabel.setText('Offline: ' + str(len(offline_list)))
        msg = QMessageBox()
        msg.setWindowTitle("Итог проверки")
        msg.setText("Доступно каналов: " + str(len(online_list)) + "\n" + "Недоступно каналов: " + str(len(offline_list)))
        msg.setIcon(QMessageBox.Information)
        self.progressBar.setVisible(False)
        msg.exec_()
        if self.offlinechannels:
            self.clearButton.setVisible(True)
    def tableAction(self):
        self.testButton.setEnabled(True)
        self.testButton.setStyleSheet(
            'background: #60fc8f; color: black; border-style: solid; border-width: 1.5px')
        data = self.my_file.read()
        # rx = re.compile(r'''(?:-1,|-1 ,|0,|0 ,|0 tvg-rec="\S",|0 tvg-rec="\S" ,|-1 tvg-rec="\S",|-1 tvg-rec="\S" ,)+([^\n]+)''')
        rx = re.compile(r'''(?<=,).*''')
        channel_name = rx.findall(data)
        group = re.compile(r'''#EXTGRP:+([^\n]+)''').findall(data)
        # group = re.compile(r'''group-title="([\s\S]+?)"|#EXTGRP:+([^\n]+)''').findall(data)
        group_tag = re.compile(r'''group-title="([\s\S]+?)"''').findall(data)
        # group = list(map(lambda m: tuple(filter(bool, m)), re.findall(r'''group-title="([\s\S]+?)"|#EXTGRP:+([^\n]+)''', data)))
        logo_url = re.compile(r'''tvg-logo="([\s\S]+?)"''').findall(data)
        url = re.compile(r'''^http[^\s]+|rtmp[^\s]+|udp[^\s]+|rtsp[^\s]+''', re.MULTILINE).findall(data)
        check = re.compile(r'''#EXTM3U''').findall(data)
        if len(check) == 0:
            self.clearTable()
        else:
            try:
                start = -1
                self.label.setText('Каналов: ' + str(len(channel_name)))
                self.tableWidget.setRowCount(len(channel_name))
                self.tableWidget.setItem(0, 0, QTableWidgetItem("Text in column 1"))
                for i in range(len(channel_name)):
                    start += 1
                    self.tableWidget.setItem(start, 0, QTableWidgetItem(channel_name[start]))
                    self.tableWidget.setItem(start, 2, QTableWidgetItem(url[start]))
                    self.tableWidget.setItem(start, 1, QTableWidgetItem('Без группы'))
                    self.tableWidget.item(start, 0).setBackground(QtGui.QColor(198, 201, 195))
                    self.tableWidget.item(start, 1).setBackground(QtGui.QColor(218, 222, 215))
                    self.tableWidget.item(start, 2).setBackground(QtGui.QColor(235, 235, 235))
                    if len(group) != 0 and len(group_tag) == 0:
                        self.tableWidget.setItem(start, 1, QTableWidgetItem(group[start]))
                        self.tableWidget.item(start, 1).setBackground(QtGui.QColor(218, 222, 215))
                    elif len(group) == 0 and len(group_tag) != 0:
                        self.tableWidget.setItem(start, 1, QTableWidgetItem(group_tag[start]))
                        self.tableWidget.item(start, 1).setBackground(QtGui.QColor(218, 222, 215))

                self.tableWidget.resizeColumnToContents(0)
                self.tableWidget.resizeColumnToContents(1)
            except:
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Плейлист имеет неизвестный формат")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
        self.my_file.close()
        self.onlinelabel.setVisible(False)
        self.offlinelabel.setVisible(False)

    def showToGroup(self):
        self.wtogroup = ToGroup(self)
        self.wtogroup.show()

    def showFromUrl(self):
        self.fromurl = OpenFromUrl(self)
        self.fromurl.show()

    def showInsert(self):
        self.groupButton.setEnabled(True)
        if not self.winsert:
            self.winsert = InsertWindow(self)
        self.winsert.show()

    def clearTable(self):
        msg = QMessageBox()
        msg.setWindowTitle("Ошибка")
        msg.setText("Неверный формат плейлиста")
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    def clearTableNew(self):
        self.tableWidget_2.clear()
        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.setColumnCount(3)
        self.tableWidget_2.setHorizontalHeaderLabels(["Название", "Группа", "URL"])
        self.label_2.setText('Каналов: ')

    def msgabout(self):
        self.about = AboutWindow(self)
        self.about.show()

    def TableClick(self):
        self.player = VideoPlayer(self)
        self.player.resize(640, 480)
        self.player.close()
        self.player.show()


class InsertWindow(QtWidgets.QMainWindow, insert.Ui_insertForm, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(InsertWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.edittable)

    def edittable(self):
        rows = int(self.parent().tableWidget_2.rowCount())
        self.parent().tableWidget_2.setRowCount(rows+1)
        self.parent().tableWidget_2.setItem(rows, 0, QTableWidgetItem(self.lineEdit.text()))
        self.parent().tableWidget_2.setItem(rows, 1, QTableWidgetItem(self.lineEdit_2.text()))
        self.parent().tableWidget_2.setItem(rows, 2, QTableWidgetItem(self.lineEdit_3.text()))
        self.parent().tableWidget_2.item(rows, 0).setBackground(QtGui.QColor(198, 201, 195))
        self.parent().tableWidget_2.item(rows, 1).setBackground(QtGui.QColor(218, 222, 215))
        self.parent().tableWidget_2.item(rows, 2).setBackground(QtGui.QColor(235, 235, 235))
        self.parent().tableWidget_2.resizeColumnToContents(0)
        self.parent().tableWidget_2.resizeColumnToContents(1)
        self.parent().label_2.setText('Каналов: ' + str(rows+1))
        self.parent().winsert.close()


class VideoPlayer(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)
        self.setWindowTitle("Предпросмотр")
        self.setFixedSize(640, 480)
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        videoWidget = QVideoWidget()
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        currentrow = self.parent().tableWidget.currentItem().row()
        chanelurl = self.parent().tableWidget.item(currentrow, 2).text()
        self.mediaPlayer.setMedia(
            QMediaContent(QUrl(chanelurl)))
        try:
           if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
               self.mediaPlayer.stop()
           else:
               self.mediaPlayer.play()
        except:
           pass

    def play(self):
        self.mediaPlayer.setMedia(QMediaContent(QUrl('http://8f303af5.cbilant.com/iptv/HV8M5S8WZAFT4A/2139/index.m3u8')))
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.stop()
        else:
            self.mediaPlayer.play()


class ToGroup(QtWidgets.QMainWindow, togroup.Ui_Form, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ToGroup, self).__init__(parent)
        self.setupUi(self)
        self.lineEdit.setText('БЕЗ ГРУППЫ')
        self.lineEdit.returnPressed.connect(self.addtogroup)
        self.toGroupButton.clicked.connect(self.addtogroup)
        self.addGroupButton.clicked.connect(self.addgroup)
        groupitem = []
        for i in range(self.parent().tableWidget_2.rowCount()):
            groupitem.append(self.parent().tableWidget_2.item(i, 1).text())
        ugroupitem = set(groupitem)
        fgroupitem = (list(ugroupitem))
        self.comboBox.addItems(fgroupitem)

    def addgroup(self):
        self.comboBox.addItem(self.lineEdit.text())

    def addtogroup(self):
        rows = []
        for ItemVal in self.parent().tableWidget_2.selectedItems():
            rows.append(ItemVal.row())
        urows = set(rows)
        frows = (list(urows))
        nrows = 0
        for i in range(len(frows)):
            self.parent().tableWidget_2.setItem(frows[nrows], 1, QTableWidgetItem(self.comboBox.currentText()))
            self.parent().tableWidget_2.item(frows[nrows], 1).setBackground(QtGui.QColor(218, 222, 215))
            nrows += 1
        self.parent().wtogroup.close()


class AboutWindow(QtWidgets.QMainWindow, about.Ui_Form, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(AboutWindow, self).__init__(parent)
        self.setupUi(self)
        self.label_2.setText('v.0.2.5')


class OpenFromUrl(QtWidgets.QMainWindow, openurl.Ui_openFromUrlForm, design.Ui_MainWindow):
    def __init__(self, parent=None):
        super(OpenFromUrl, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.openurl)
        self.parent().tableWidget.clear()
        self.parent().tableWidget.setRowCount(0)
        self.parent().tableWidget.setColumnCount(3)
        self.parent().tableWidget.setHorizontalHeaderLabels(["Название", "Группа", "URL"])

    def openurl(self):
        self.parent().testButton.setEnabled(True)
        try:
            req = requests.get(self.lineEdit.text())
        except:
            msgurl = QMessageBox()
            msgurl.setWindowTitle("Ошибка")
            msgurl.setText("Плейлист недоступен, проверьте адрес")
            msgurl.setIcon(QMessageBox.Warning)
            msgurl.exec_()
            self.parent().fromurl.close()
            return
        data = req.text
        #rx = re.compile(
            #r'''(?:-1,|-1 ,|0,|0 ,|0 tvg-rec="\S",|0 tvg-rec="\S" ,|-1 tvg-rec="\S",|-1 tvg-rec="\S" ,)+([^\n]+)''')
        #channel_name = rx.findall(data)
        #group = re.compile(r'''#EXTGRP:+([^\n]+)''').findall(data)
        #url = re.compile(r'''^http[^\s]+|rtmp[^\s]+|udp[^\s]+|rtsp[^\s]+''', re.MULTILINE).findall(data)
        #check = re.compile(r'''#EXTM3U''').findall(data)
        rx = re.compile(r'''(?<=,).*''')
        channel_name = rx.findall(data)
        group = re.compile(r'''#EXTGRP:+([^\n]+)''').findall(data)
        # group = re.compile(r'''group-title="([\s\S]+?)"|#EXTGRP:+([^\n]+)''').findall(data)
        group_tag = re.compile(r'''group-title="([\s\S]+?)"''').findall(data)
        # group = list(map(lambda m: tuple(filter(bool, m)), re.findall(r'''group-title="([\s\S]+?)"|#EXTGRP:+([^\n]+)''', data)))
        logo_url = re.compile(r'''tvg-logo="([\s\S]+?)"''').findall(data)
        url = re.compile(r'''^http[^\s]+|rtmp[^\s]+|udp[^\s]+|rtsp[^\s]+''', re.MULTILINE).findall(data)
        check = re.compile(r'''#EXTM3U''').findall(data)
        if len(check) == 0:
            self.clearTable()
        else:
            try:
                start = -1
                self.parent().label.setText('Каналов: ' + str(len(channel_name)))
                self.parent().tableWidget.setRowCount(len(channel_name))
                self.parent().tableWidget.setItem(0, 0, QTableWidgetItem("Text in column 1"))
                for i in range(len(channel_name)):
                    start += 1
                    self.parent().tableWidget.setItem(start, 0, QTableWidgetItem(channel_name[start]))
                    self.parent().tableWidget.setItem(start, 2, QTableWidgetItem(url[start]))
                    self.parent().tableWidget.setItem(start, 1, QTableWidgetItem('Без группы'))
                    self.parent().tableWidget.item(start, 0).setBackground(QtGui.QColor(198, 201, 195))
                    self.parent().tableWidget.item(start, 1).setBackground(QtGui.QColor(218, 222, 215))
                    self.parent().tableWidget.item(start, 2).setBackground(QtGui.QColor(235, 235, 235))
                    if len(group) != 0 and len(group_tag) == 0:
                        self.parent().tableWidget.setItem(start, 1, QTableWidgetItem(group[start]))
                        self.parent().tableWidget.item(start, 1).setBackground(QtGui.QColor(218, 222, 215))
                    elif len(group) == 0 and len(group_tag) != 0:
                        self.parent().tableWidget.setItem(start, 1, QTableWidgetItem(group_tag[start]))
                        self.parent().tableWidget.item(start, 1).setBackground(QtGui.QColor(218, 222, 215))
                self.parent().tableWidget.resizeColumnToContents(0)
                self.parent().tableWidget.resizeColumnToContents(1)
                self.parent().fromurl.close()
            except:
                self.parent().fromurl.close()
                msg = QMessageBox()
                msg.setWindowTitle("Ошибка")
                msg.setText("Плейлист имеет неизвестный формат")
                msg.setIcon(QMessageBox.Warning)
                msg.exec_()
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()

