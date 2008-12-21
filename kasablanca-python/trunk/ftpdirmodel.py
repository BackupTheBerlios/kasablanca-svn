#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *

class FtpDirModel (QAbstractItemModel):
	
	def __init__ (self):
		QAbstractItemModel.__init__ (self)
		self.list = list()
		#self.list.append("hello")
		#self.list.append("world")

	def columnCount(self, parent = QModelIndex()):
		return 1

	def rowCount(self, index):
		return len(self.list)

	def index(self, row, column, parent = QModelIndex()):
		self.createIndex(row, 0, 0)

	def parent(child):
		return QModelIndex()

	def data(index, role = Qt.DisplayRole):
		if (index.isValid() == False):
			return QVariant()
		if (index.row() >= len(self.list)):
			return QVariant()
		if (role == Qt.DisplayRole):
			return self.list[index]
		else:
			return QVariant()