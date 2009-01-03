#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *

class FtpDirModel (QAbstractItemModel):
	
	def __init__ (self):
		QAbstractItemModel.__init__ (self)
		self.list = list()

	def columnCount(self, parent = QModelIndex()):
		return 2

	def index(self, row, column, parent = QModelIndex()):
		return self.createIndex(row, column)

	def rowCount(self, index = QModelIndex()):
		return len(self.list)

	def parent(self, child):
		return QModelIndex()

	def setData(self, index, value, role = Qt.DisplayRole):
		
		if index.row() == len(self.list):
			self.list.append(value.toStringList())
			self.emit(SIGNAL('layoutChanged()'))
		else:
			self.list[index.row()] = value.toStringList()
			self.emit(SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), index, index)
		return True

	def data(self, index, role = Qt.DisplayRole):
		if index.isValid() == False:
			return QVariant()
		elif index.row() >= len(self.list):
			return QVariant()
		elif role == Qt.DisplayRole:
			return QVariant(self.list[index.row()][index.column()])
		else:
			return QVariant()

	def headerData(self, section, orientation, role = Qt.DisplayRole):
		if role != Qt.DisplayRole:
			return QVariant()
		if section == 0:
			return QVariant("Name")
		elif section == 1:
			return QVariant("User")
		else:
			return QVariant()