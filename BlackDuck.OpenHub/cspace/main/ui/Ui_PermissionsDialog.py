# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PermissionsDialog.ui'
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

class Ui_PermissionsDialog(object):
    def setupUi(self, PermissionsDialog):
        PermissionsDialog.setObjectName(_fromUtf8("PermissionsDialog"))
        PermissionsDialog.resize(569, 414)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/edit_permissions32.png"))
        PermissionsDialog.setWindowIcon(icon)
        PermissionsDialog.setSizeGripEnabled(False)
        self.vboxlayout = QtGui.QVBoxLayout(PermissionsDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(PermissionsDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setWordWrap(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout1.addWidget(self.label)
        self.predefinedPermissions = QtGui.QTextEdit(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(5), QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.predefinedPermissions.sizePolicy().hasHeightForWidth())
        self.predefinedPermissions.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.predefinedPermissions.setFont(font)
        self.predefinedPermissions.setTabChangesFocus(True)
        self.predefinedPermissions.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.predefinedPermissions.setReadOnly(True)
        self.predefinedPermissions.setObjectName(_fromUtf8("predefinedPermissions"))
        self.vboxlayout1.addWidget(self.predefinedPermissions)
        self.vboxlayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(PermissionsDialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.vboxlayout2 = QtGui.QVBoxLayout(self.groupBox_2)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.status = QtGui.QLabel(self.groupBox_2)
        self.status.setObjectName(_fromUtf8("status"))
        self.vboxlayout2.addWidget(self.status)
        self.permissions = QtGui.QTextEdit(self.groupBox_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.permissions.setFont(font)
        self.permissions.setTabChangesFocus(True)
        self.permissions.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.permissions.setAcceptRichText(False)
        self.permissions.setObjectName(_fromUtf8("permissions"))
        self.vboxlayout2.addWidget(self.permissions)
        self.vboxlayout.addWidget(self.groupBox_2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.applyButton = QtGui.QPushButton(PermissionsDialog)
        self.applyButton.setEnabled(False)
        self.applyButton.setDefault(True)
        self.applyButton.setObjectName(_fromUtf8("applyButton"))
        self.hboxlayout.addWidget(self.applyButton)
        self.closeButton = QtGui.QPushButton(PermissionsDialog)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.hboxlayout.addWidget(self.closeButton)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem1)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.retranslateUi(PermissionsDialog)
        QtCore.QMetaObject.connectSlotsByName(PermissionsDialog)

    def retranslateUi(self, PermissionsDialog):
        PermissionsDialog.setWindowTitle(_translate("PermissionsDialog", "Modify Permissions", None))
        self.groupBox.setTitle(_translate("PermissionsDialog", "Predefined rules", None))
        self.label.setText(_translate("PermissionsDialog", "These rules are hard coded, and may not be modified.", None))
        self.groupBox_2.setTitle(_translate("PermissionsDialog", "User defined rules", None))
        self.status.setText(_translate("PermissionsDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /></head><body style=\" white-space: pre-wrap; font-family:MS Shell Dlg 2; font-size:8.25pt; font-weight:400; font-style:normal; text-decoration:none;\"><p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Set user defined rules to override predefined rules, and to define new rules.</span></p></body></html>", None))
        self.applyButton.setText(_translate("PermissionsDialog", "&Apply", None))
        self.closeButton.setText(_translate("PermissionsDialog", "&Close", None))

import images_rc
