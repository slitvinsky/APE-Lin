from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 142)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(400, 142))
        Form.setMaximumSize(QtCore.QSize(400, 142))
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(20, 20, 321, 26))
        self.lineEdit.setObjectName("lineEdit")
        self.toGroupButton = QtWidgets.QPushButton(Form)
        self.toGroupButton.setGeometry(QtCore.QRect(130, 100, 131, 26))
        self.toGroupButton.setObjectName("toGroupButton")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(20, 60, 361, 26))
        self.comboBox.setObjectName("comboBox")
        self.addGroupButton = QtWidgets.QPushButton(Form)
        self.addGroupButton.setGeometry(QtCore.QRect(350, 20, 31, 26))
        self.addGroupButton.setObjectName("addGroupButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Добавить в группу"))
        self.toGroupButton.setText(_translate("Form", "Добавить в группу"))
        self.addGroupButton.setText(_translate("Form", "+"))
