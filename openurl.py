# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'openurl.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_openFromUrlForm(object):
    def setupUi(self, openFromUrlForm):
        openFromUrlForm.setObjectName("openFromUrlForm")
        openFromUrlForm.resize(411, 88)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(41)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(openFromUrlForm.sizePolicy().hasHeightForWidth())
        openFromUrlForm.setSizePolicy(sizePolicy)
        openFromUrlForm.setMinimumSize(QtCore.QSize(411, 88))
        openFromUrlForm.setMaximumSize(QtCore.QSize(411, 88))
        self.lineEdit = QtWidgets.QLineEdit(openFromUrlForm)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 321, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(openFromUrlForm)
        self.pushButton.setGeometry(QtCore.QRect(360, 30, 31, 26))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(openFromUrlForm)
        QtCore.QMetaObject.connectSlotsByName(openFromUrlForm)

    def retranslateUi(self, openFromUrlForm):
        _translate = QtCore.QCoreApplication.translate
        openFromUrlForm.setWindowTitle(_translate("openFromUrlForm", "Открыть по ссылке"))
        self.pushButton.setText(_translate("openFromUrlForm", "OK"))
