# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plugin-x509clone.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_X509CloneGui(object):
    def setupUi(self, X509CloneGui):
        X509CloneGui.setObjectName("X509CloneGui")
        X509CloneGui.resize(597, 398)
        self.gridLayout = QtWidgets.QGridLayout(X509CloneGui)
        self.gridLayout.setObjectName("gridLayout")
        self.x509clone_casign_groupbox = QtWidgets.QGroupBox(X509CloneGui)
        self.x509clone_casign_groupbox.setTitle("")
        self.x509clone_casign_groupbox.setObjectName("x509clone_casign_groupbox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.x509clone_casign_groupbox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.x509clone_casign_groupbox)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        self.verticalLayout.addWidget(self.plainTextEdit_2)
        self.x509clone_load_cacert_button = QtWidgets.QPushButton(self.x509clone_casign_groupbox)
        self.x509clone_load_cacert_button.setObjectName("x509clone_load_cacert_button")
        self.verticalLayout.addWidget(self.x509clone_load_cacert_button)
        self.x509clone_load_cakey_button = QtWidgets.QPushButton(self.x509clone_casign_groupbox)
        self.x509clone_load_cakey_button.setObjectName("x509clone_load_cakey_button")
        self.verticalLayout.addWidget(self.x509clone_load_cakey_button)
        self.gridLayout.addWidget(self.x509clone_casign_groupbox, 1, 3, 1, 1)
        self.x509clone_ok_button = QtWidgets.QDialogButtonBox(X509CloneGui)
        self.x509clone_ok_button.setOrientation(QtCore.Qt.Horizontal)
        self.x509clone_ok_button.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.x509clone_ok_button.setObjectName("x509clone_ok_button")
        self.gridLayout.addWidget(self.x509clone_ok_button, 4, 3, 1, 1)
        self.x509clone_selfsign_groupbox = QtWidgets.QGroupBox(X509CloneGui)
        self.x509clone_selfsign_groupbox.setTitle("")
        self.x509clone_selfsign_groupbox.setObjectName("x509clone_selfsign_groupbox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.x509clone_selfsign_groupbox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.x509clone_selfsign_groupbox)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.gridLayout.addWidget(self.x509clone_selfsign_groupbox, 1, 2, 1, 1)
        self.x509clone_casign = QtWidgets.QRadioButton(X509CloneGui)
        self.x509clone_casign.setObjectName("x509clone_casign")
        self.gridLayout.addWidget(self.x509clone_casign, 0, 3, 1, 1)
        self.x509clone_selfsign = QtWidgets.QRadioButton(X509CloneGui)
        self.x509clone_selfsign.setObjectName("x509clone_selfsign")
        self.gridLayout.addWidget(self.x509clone_selfsign, 0, 2, 1, 1)

        self.retranslateUi(X509CloneGui)
        self.x509clone_ok_button.accepted.connect(X509CloneGui.accept)
        self.x509clone_ok_button.rejected.connect(X509CloneGui.reject)
        QtCore.QMetaObject.connectSlotsByName(X509CloneGui)

    def retranslateUi(self, X509CloneGui):
        _translate = QtCore.QCoreApplication.translate
        X509CloneGui.setWindowTitle(_translate("X509CloneGui", "Dialog"))
        self.plainTextEdit_2.setPlainText(_translate("X509CloneGui", "Sign the new certificate with an existing CA certificate. The private key of the existing CA must be available."))
        self.x509clone_load_cacert_button.setText(_translate("X509CloneGui", "Load CA certificate"))
        self.x509clone_load_cakey_button.setText(_translate("X509CloneGui", "Load CA private key"))
        self.plainTextEdit.setPlainText(_translate("X509CloneGui", "The new certificate will be self signed."))
        self.x509clone_casign.setText(_translate("X509CloneGui", "Sign wi&th existing CA"))
        self.x509clone_selfsign.setText(_translate("X509CloneGui", "Self si&gned"))

