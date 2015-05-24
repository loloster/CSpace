# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddContactDialog.ui'
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

class Ui_AddContactDialog(object):
    def setupUi(self, AddContactDialog):
        AddContactDialog.setObjectName(_fromUtf8("AddContactDialog"))
        AddContactDialog.resize(399, 474)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/images/user_add32.png"))
        AddContactDialog.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(AddContactDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.groupBox = QtGui.QGroupBox(AddContactDialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout1 = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.keyIdStatus = QtGui.QLabel(self.groupBox)
        self.keyIdStatus.setObjectName(_fromUtf8("keyIdStatus"))
        self.vboxlayout1.addWidget(self.keyIdStatus)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.hboxlayout.addWidget(self.label_2)
        self.keyId = QtGui.QLineEdit(self.groupBox)
        self.keyId.setObjectName(_fromUtf8("keyId"))
        self.hboxlayout.addWidget(self.keyId)
        self.fetchKeyButton = QtGui.QPushButton(self.groupBox)
        self.fetchKeyButton.setAutoDefault(False)
        self.fetchKeyButton.setObjectName(_fromUtf8("fetchKeyButton"))
        self.hboxlayout.addWidget(self.fetchKeyButton)
        self.vboxlayout1.addLayout(self.hboxlayout)
        self.vboxlayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(AddContactDialog)
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
        self.publicKey.setTabChangesFocus(True)
        self.publicKey.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        self.publicKey.setAcceptRichText(False)
        self.publicKey.setObjectName(_fromUtf8("publicKey"))
        self.vboxlayout2.addWidget(self.publicKey)
        self.vboxlayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(AddContactDialog)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.vboxlayout3 = QtGui.QVBoxLayout(self.groupBox_3)
        self.vboxlayout3.setMargin(9)
        self.vboxlayout3.setSpacing(6)
        self.vboxlayout3.setObjectName(_fromUtf8("vboxlayout3"))
        self.label_3 = QtGui.QLabel(self.groupBox_3)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.vboxlayout3.addWidget(self.label_3)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label_4 = QtGui.QLabel(self.groupBox_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.hboxlayout1.addWidget(self.label_4)
        self.contactName = QtGui.QLineEdit(self.groupBox_3)
        self.contactName.setObjectName(_fromUtf8("contactName"))
        self.hboxlayout1.addWidget(self.contactName)
        self.vboxlayout3.addLayout(self.hboxlayout1)
        self.vboxlayout.addWidget(self.groupBox_3)
        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName(_fromUtf8("hboxlayout2"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout2.addItem(spacerItem)
        self.addContactButton = QtGui.QPushButton(AddContactDialog)
        self.addContactButton.setAutoDefault(False)
        self.addContactButton.setObjectName(_fromUtf8("addContactButton"))
        self.hboxlayout2.addWidget(self.addContactButton)
        self.cancelButton = QtGui.QPushButton(AddContactDialog)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.hboxlayout2.addWidget(self.cancelButton)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(AddContactDialog)
        QtCore.QMetaObject.connectSlotsByName(AddContactDialog)

    def retranslateUi(self, AddContactDialog):
        AddContactDialog.setWindowTitle(_translate("AddContactDialog", "Add Contact...", None))
        self.groupBox.setTitle(_translate("AddContactDialog", "KeyID", None))
        self.keyIdStatus.setText(_translate("AddContactDialog", "Enter the KeyID for your contact.", None))
        self.label_2.setText(_translate("AddContactDialog", "KeyID:", None))
        self.fetchKeyButton.setText(_translate("AddContactDialog", "&Fetch Public Key...", None))
        self.groupBox_2.setTitle(_translate("AddContactDialog", "Public Key", None))
        self.groupBox_3.setTitle(_translate("AddContactDialog", "Contact Name", None))
        self.label_3.setText(_translate("AddContactDialog", "Enter a name for your contact. This name must be UNIQUE in your contact list. Only lowercase alphabets(a-z), digits(0-9) and underscore(\'_\') are allowed.", None))
        self.label_4.setText(_translate("AddContactDialog", "Contact Name:", None))
        self.addContactButton.setText(_translate("AddContactDialog", "&Add Contact", None))
        self.cancelButton.setText(_translate("AddContactDialog", "&Cancel", None))

import images_rc
