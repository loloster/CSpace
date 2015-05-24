# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'KeyInfoDialog.ui'
#
# Created: Sun May 24 16:09:45 2015
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

class Ui_KeyInfoDialog(object):
    def setupUi(self, KeyInfoDialog):
        KeyInfoDialog.setObjectName(_fromUtf8("KeyInfoDialog"))
        KeyInfoDialog.resize(425, 353)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/key_info32.png"))
        KeyInfoDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(KeyInfoDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(KeyInfoDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout1.addWidget(self.label)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout.addWidget(self.label_2)
        self.keyId = QtGui.QLineEdit(self.groupBox)
        self.keyId.setReadOnly(True)
        self.keyId.setObjectName(_fromUtf8("keyId"))
        self.hboxlayout.addWidget(self.keyId)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.vboxlayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(KeyInfoDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.publicKey = QtGui.QTextEdit(self.groupBox_2)
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
        self.vboxlayout2.addWidget(self.publicKey)
        self.vboxlayout.addWidget(self.groupBox_2)

        self.retranslateUi(KeyInfoDialog)
        QtCore.QMetaObject.connectSlotsByName(KeyInfoDialog)

    def retranslateUi(self, KeyInfoDialog):
        KeyInfoDialog.setWindowTitle(_translate("KeyInfoDialog", "Key Information", None))
        self.groupBox.setTitle(_translate("KeyInfoDialog", "KeyID", None))
        self.label.setText(_translate("KeyInfoDialog", "Send your KeyID to your friends so that they can add you to their contact list.", None))
        self.label_2.setText(_translate("KeyInfoDialog", "KeyID:", None))
        self.groupBox_2.setTitle(_translate("KeyInfoDialog", "RSA Public Key", None))
        self.publicKey.setHtml(_translate("KeyInfoDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:Courier New; font-size:10pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Public Key Data...</p></body></html>", None))

import images_rc
