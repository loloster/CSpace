# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ContactInfoDialog.ui'
#
# Created: Sun May 24 16:09:44 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_ContactInfoDialog(object):
    def setupUi(self, ContactInfoDialog):
        ContactInfoDialog.setObjectName(_fromUtf8("ContactInfoDialog"))
        ContactInfoDialog.resize(392, 363)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/contact_info32.png"))
        ContactInfoDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(ContactInfoDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox_2 = QtGui.QGroupBox(ContactInfoDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.hboxlayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.name = QtGui.QLineEdit(self.groupBox_2)
        self.name.setObjectName(_fromUtf8("name"))
        self.hboxlayout.addWidget(self.name)
        self.updateNameButton = QtGui.QPushButton(self.groupBox_2)
        self.updateNameButton.setAutoDefault(False)
        self.updateNameButton.setObjectName(_fromUtf8("updateNameButton"))
        self.hboxlayout.addWidget(self.updateNameButton)
        self.vboxlayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(ContactInfoDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.publicKey = QtGui.QTextEdit(self.groupBox)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.publicKey.setFont(font)
        self.publicKey.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.publicKey.setReadOnly(True)
        self.publicKey.setAcceptRichText(False)
        self.publicKey.setObjectName(_fromUtf8("publicKey"))
        self.vboxlayout1.addWidget(self.publicKey)
        self.vboxlayout.addWidget(self.groupBox)

        self.retranslateUi(ContactInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(ContactInfoDialog)

    def retranslateUi(self, ContactInfoDialog):
        ContactInfoDialog.setWindowTitle(_translate("ContactInfoDialog", "Contact Information", None))
        self.groupBox_2.setTitle(_translate("ContactInfoDialog", "Contact Name", None))
        self.updateNameButton.setText(_translate("ContactInfoDialog", "Update Name", None))
        self.groupBox.setTitle(_translate("ContactInfoDialog", "RSA Public Key", None))
        self.publicKey.setHtml(_translate("ContactInfoDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Courier New; font-size:10pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Public Key Data...</p></body></html>", None))

import images_rc
