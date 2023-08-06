# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugin-jwt.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_JwtCreateGui(object):
    def setupUi(self, JwtCreateGui):
        JwtCreateGui.setObjectName("JwtCreateGui")
        JwtCreateGui.resize(351, 461)
        self.dialogButtonBox = QtWidgets.QDialogButtonBox(JwtCreateGui)
        self.dialogButtonBox.setGeometry(QtCore.QRect(-50, 420, 391, 32))
        self.dialogButtonBox.setOrientation(QtCore.Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.dialogButtonBox.setObjectName("dialogButtonBox")
        self.label = QtWidgets.QLabel(JwtCreateGui)
        self.label.setGeometry(QtCore.QRect(10, 20, 141, 18))
        self.label.setObjectName("label")
        self.algo_combo = QtWidgets.QComboBox(JwtCreateGui)
        self.algo_combo.setGeometry(QtCore.QRect(190, 10, 151, 32))
        self.algo_combo.setObjectName("algo_combo")
        self.label_2 = QtWidgets.QLabel(JwtCreateGui)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 261, 18))
        self.label_2.setObjectName("label_2")
        self.read_secret_file_button = QtWidgets.QPushButton(JwtCreateGui)
        self.read_secret_file_button.setGeometry(QtCore.QRect(10, 370, 331, 34))
        self.read_secret_file_button.setObjectName("read_secret_file_button")
        self.secret_base64_checkbox = QtWidgets.QCheckBox(JwtCreateGui)
        self.secret_base64_checkbox.setGeometry(QtCore.QRect(10, 320, 231, 22))
        self.secret_base64_checkbox.setObjectName("secret_base64_checkbox")
        self.secret_input_field = QtWidgets.QTextEdit(JwtCreateGui)
        self.secret_input_field.setGeometry(QtCore.QRect(10, 100, 331, 211))
        self.secret_input_field.setObjectName("secret_input_field")
        self.line = QtWidgets.QFrame(JwtCreateGui)
        self.line.setGeometry(QtCore.QRect(20, 350, 321, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(JwtCreateGui)
        self.dialogButtonBox.accepted.connect(JwtCreateGui.accept)
        self.dialogButtonBox.rejected.connect(JwtCreateGui.reject)
        QtCore.QMetaObject.connectSlotsByName(JwtCreateGui)

    def retranslateUi(self, JwtCreateGui):
        _translate = QtCore.QCoreApplication.translate
        JwtCreateGui.setWindowTitle(_translate("JwtCreateGui", "Create JWT Token"))
        self.label.setText(_translate("JwtCreateGui", "Signature algorithm:"))
        self.label_2.setText(_translate("JwtCreateGui", "Secret (symmetric) or Key (asymmetric):"))
        self.read_secret_file_button.setText(_translate("JwtCreateGui", "Read secret from file"))
        self.secret_base64_checkbox.setText(_translate("JwtCreateGui", "secret base64 encoded"))

