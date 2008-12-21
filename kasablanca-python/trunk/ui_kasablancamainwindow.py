# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kasablancamainwindow.ui'
#
# Created: Sat Dec 20 12:53:00 2008
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_KasablancaMainWindow(object):
    def setupUi(self, KasablancaMainWindow):
        KasablancaMainWindow.setObjectName("KasablancaMainWindow")
        KasablancaMainWindow.resize(553, 423)
        self.centralwidget = QtGui.QWidget(KasablancaMainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)
        self.treeView = QtGui.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.gridLayout.addWidget(self.treeView, 0, 0, 1, 1)
        KasablancaMainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(KasablancaMainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 553, 23))
        self.menubar.setObjectName("menubar")
        self.menuHello = QtGui.QMenu(self.menubar)
        self.menuHello.setObjectName("menuHello")
        KasablancaMainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(KasablancaMainWindow)
        self.statusbar.setObjectName("statusbar")
        KasablancaMainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHello.menuAction())

        self.retranslateUi(KasablancaMainWindow)
        QtCore.QMetaObject.connectSlotsByName(KasablancaMainWindow)

    def retranslateUi(self, KasablancaMainWindow):
        KasablancaMainWindow.setWindowTitle(QtGui.QApplication.translate("KasablancaMainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("KasablancaMainWindow", "PushButton", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHello.setTitle(QtGui.QApplication.translate("KasablancaMainWindow", "Hello", None, QtGui.QApplication.UnicodeUTF8))

