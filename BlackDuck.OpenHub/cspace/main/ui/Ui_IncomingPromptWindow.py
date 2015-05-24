# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'IncomingPromptWindow.ui'
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

class Ui_IncomingPromptWindow(object):
    def setupUi(self, IncomingPromptWindow):
        IncomingPromptWindow.setObjectName(_fromUtf8("IncomingPromptWindow"))
        IncomingPromptWindow.resize(344, 130)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/cspace32.png"))
        IncomingPromptWindow.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(IncomingPromptWindow)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.prompt = QtGui.QLabel(IncomingPromptWindow)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.prompt.setFont(font)
        self.prompt.setTextFormat(QtCore.Qt.RichText)
        self.prompt.setAlignment(QtCore.Qt.AlignCenter)
        self.prompt.setWordWrap(True)
        self.prompt.setObjectName(_fromUtf8("prompt"))
        self.vboxlayout.addWidget(self.prompt)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.allowButton = QtGui.QPushButton(IncomingPromptWindow)
        self.allowButton.setObjectName(_fromUtf8("allowButton"))
        self.hboxlayout.addWidget(self.allowButton)
        self.denyButton = QtGui.QPushButton(IncomingPromptWindow)
        self.denyButton.setObjectName(_fromUtf8("denyButton"))
        self.hboxlayout.addWidget(self.denyButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(IncomingPromptWindow)
        QtCore.QMetaObject.connectSlotsByName(IncomingPromptWindow)

    def retranslateUi(self, IncomingPromptWindow):
        IncomingPromptWindow.setWindowTitle(_translate("IncomingPromptWindow", "Incoming Connection", None))
        self.prompt.setText(_translate("IncomingPromptWindow", "<b>Prompt</b>", None))
        self.allowButton.setText(_translate("IncomingPromptWindow", "&Allow", None))
        self.denyButton.setText(_translate("IncomingPromptWindow", "&Deny", None))

import images_rc
