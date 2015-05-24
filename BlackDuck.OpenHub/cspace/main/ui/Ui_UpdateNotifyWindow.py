# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UpdateNotifyWindow.ui'
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

class Ui_UpdateNotifyWindow(object):
    def setupUi(self, UpdateNotifyWindow):
        UpdateNotifyWindow.setObjectName(_fromUtf8("UpdateNotifyWindow"))
        UpdateNotifyWindow.resize(364, 110)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/cspace32.png"))
        UpdateNotifyWindow.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(UpdateNotifyWindow)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(UpdateNotifyWindow)
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/images/cspace48.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.label_2 = QtGui.QLabel(UpdateNotifyWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5), QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout.addWidget(self.label_2)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem)
        self.installUpdateButton = QtGui.QPushButton(UpdateNotifyWindow)
        self.installUpdateButton.setObjectName(_fromUtf8("installUpdateButton"))
        self.hboxlayout1.addWidget(self.installUpdateButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout1.addItem(spacerItem1)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.retranslateUi(UpdateNotifyWindow)
        QtCore.QMetaObject.connectSlotsByName(UpdateNotifyWindow)

    def retranslateUi(self, UpdateNotifyWindow):
        UpdateNotifyWindow.setWindowTitle(_translate("UpdateNotifyWindow", "CSpace Update", None))
        self.label_2.setText(_translate("UpdateNotifyWindow", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:MS Shell Dlg; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">A new version of CSpace has been downloaded and is ready to install.</span><br /><span style=\" font-weight:600;\">Click the button below after closing all CSpace windows</span></p></body></html>", None))
        self.installUpdateButton.setText(_translate("UpdateNotifyWindow", "Stop CSpace, Install Update, and Restart CSpace", None))

import images_rc
