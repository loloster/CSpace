# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GoOnlineDialog.ui'
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

class Ui_GoOnlineDialog(object):
    def setupUi(self, GoOnlineDialog):
        GoOnlineDialog.setObjectName(_fromUtf8("GoOnlineDialog"))
        GoOnlineDialog.resize(279, 155)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/connect32.png"))
        GoOnlineDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(GoOnlineDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(GoOnlineDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.password = QtGui.QLineEdit(self.groupBox)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.gridlayout.addWidget(self.password, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.keys = QtGui.QComboBox(self.groupBox)
        self.keys.setObjectName(_fromUtf8("keys"))
        self.gridlayout.addWidget(self.keys, 0, 1, 1, 1)
        self.vboxlayout1.addLayout(self.gridlayout)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.rememberKey = QtGui.QCheckBox(self.groupBox)
        self.rememberKey.setObjectName(_fromUtf8("rememberKey"))
        self.hboxlayout.addWidget(self.rememberKey)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.vboxlayout.addWidget(self.groupBox)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.goOnlineButton = QtGui.QPushButton(GoOnlineDialog)
        self.goOnlineButton.setDefault(True)
        self.goOnlineButton.setObjectName(_fromUtf8("goOnlineButton"))
        self.hboxlayout1.addWidget(self.goOnlineButton)
        self.cancelButton = QtGui.QPushButton(GoOnlineDialog)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout1.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.label_2.setBuddy(self.password)
        self.label.setBuddy(self.keys)

        self.retranslateUi(GoOnlineDialog)
        QtCore.QMetaObject.connectSlotsByName(GoOnlineDialog)
        GoOnlineDialog.setTabOrder(self.keys, self.password)
        GoOnlineDialog.setTabOrder(self.password, self.rememberKey)
        GoOnlineDialog.setTabOrder(self.rememberKey, self.goOnlineButton)
        GoOnlineDialog.setTabOrder(self.goOnlineButton, self.cancelButton)

    def retranslateUi(self, GoOnlineDialog):
        GoOnlineDialog.setWindowTitle(_translate("GoOnlineDialog", "Go Online...", None))
        self.groupBox.setTitle(_translate("GoOnlineDialog", "Select Key", None))
        self.label_2.setText(_translate("GoOnlineDialog", "&Password:", None))
        self.label.setText(_translate("GoOnlineDialog", "&Key:", None))
        self.rememberKey.setText(_translate("GoOnlineDialog", "&Remember password for this key", None))
        self.goOnlineButton.setText(_translate("GoOnlineDialog", "&Go Online", None))
        self.cancelButton.setText(_translate("GoOnlineDialog", "&Cancel", None))

import images_rc
