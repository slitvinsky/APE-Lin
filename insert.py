# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'insert.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_insertForm(object):
    def setupUi(self, insertForm):
        insertForm.setObjectName("insertForm")
        insertForm.resize(400, 185)
        self.pushButton = QtWidgets.QPushButton(insertForm)
        self.pushButton.setGeometry(QtCore.QRect(10, 140, 381, 31))
        self.pushButton.setObjectName("pushButton")
        self.widget = QtWidgets.QWidget(insertForm)
        self.widget.setGeometry(QtCore.QRect(10, 30, 71, 91))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.widget1 = QtWidgets.QWidget(insertForm)
        self.widget1.setGeometry(QtCore.QRect(120, 30, 271, 92))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_2.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout_2.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.widget1)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout_2.addWidget(self.lineEdit_3)

        self.retranslateUi(insertForm)
        QtCore.QMetaObject.connectSlotsByName(insertForm)

    def retranslateUi(self, insertForm):
        _translate = QtCore.QCoreApplication.translate
        insertForm.setWindowTitle(_translate("insertForm", "Добавление канала"))
        self.pushButton.setText(_translate("insertForm", "Добавить канал"))
        self.label.setText(_translate("insertForm", "Название"))
        self.label_2.setText(_translate("insertForm", "Группа"))
        self.label_3.setText(_translate("insertForm", "URL"))
