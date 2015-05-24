# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CreateKeyDoneDialog.ui'
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

class Ui_CreateKeyDoneDialog(object):
    def setupUi(self, CreateKeyDoneDialog):
        CreateKeyDoneDialog.setObjectName(_fromUtf8("CreateKeyDoneDialog"))
        CreateKeyDoneDialog.resize(314, 172)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/register32.png"))
        CreateKeyDoneDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(CreateKeyDoneDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label = QtGui.QLabel(CreateKeyDoneDialog)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.groupBox = QtGui.QGroupBox(CreateKeyDoneDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout1.addWidget(self.label_2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.hboxlayout.addWidget(self.label_3)
        self.keyId = QtGui.QLineEdit(self.groupBox)
        self.keyId.setReadOnly(True)
        self.keyId.setObjectName(_fromUtf8("keyId"))
        self.hboxlayout.addWidget(self.keyId)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.vboxlayout.addWidget(self.groupBox)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.rememberKey = QtGui.QCheckBox(CreateKeyDoneDialog)
        self.rememberKey.setObjectName(_fromUtf8("rememberKey"))
        self.hboxlayout1.addWidget(self.rememberKey)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.goOnlineButton = QtGui.QPushButton(CreateKeyDoneDialog)
        self.goOnlineButton.setObjectName(_fromUtf8("goOnlineButton"))
        self.hboxlayout1.addWidget(self.goOnlineButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(CreateKeyDoneDialog)
        QtCore.QMetaObject.connectSlotsByName(CreateKeyDoneDialog)

    def retranslateUi(self, CreateKeyDoneDialog):
        CreateKeyDoneDialog.setWindowTitle(_translate("CreateKeyDoneDialog", "Private Key Created", None))
        self.label.setText(_translate("CreateKeyDoneDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:MS Shell Dlg 2; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Your RSA Private Key has been created.</span></p></body></html>", None))
        self.groupBox.setTitle(_translate("CreateKeyDoneDialog", "KeyID", None))
        self.label_2.setText(_translate("CreateKeyDoneDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:MS Shell Dlg 2; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Please send your KeyID to your friends so that they can add you to their contact list.</span></p></body></html>", None))
        self.label_3.setText(_translate("CreateKeyDoneDialog", "KeyID:", None))
        self.rememberKey.setText(_translate("CreateKeyDoneDialog", "&Remember password for this key", None))
        self.goOnlineButton.setText(_translate("CreateKeyDoneDialog", "&Go Online", None))

import images_rc
