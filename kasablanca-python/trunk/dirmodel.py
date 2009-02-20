#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyKDE4.kdeui import KIconLoader
from PyQt4.QtCore import *

class DirModel (QAbstractItemModel):

	FILENAME, USER, GROUP, SIZE, DIRECTORY, LINK = range(6)

	def __init__ (self):

		QAbstractItemModel.__init__ (self)
		self.list = list()

		self.folderIcon = KIconLoader.global_().loadIcon("folder", KIconLoader.NoGroup, KIconLoader.SizeSmall)
		self.textplainIcon = KIconLoader.global_().loadIcon("text-plain", KIconLoader.NoGroup, KIconLoader.SizeSmall)

	def columnCount(self, parent = QModelIndex()):

		return 4

	def index(self, row, column, parent = QModelIndex()):

		return self.createIndex(row, column)

	def rowCount(self, index = QModelIndex()):
		return len(self.list)

	def sort(self, column, order):

		reverse = (order == Qt.DescendingOrder)

		if (column == self.FILENAME):
			self.list.sort(cmp = self.compareNames, reverse = reverse)
		elif (column == self.USER):
			self.list.sort(cmp = self.compareUsers, reverse = reverse)
		elif (column == self.GROUP):
			self.list.sort(cmp = self.compareGroups, reverse = reverse)
		elif (column == self.SIZE):
			self.list.sort(cmp = self.compareSizes, reverse = reverse)

		self.emit(SIGNAL('layoutChanged()'))
	
	def compare(self, column, x, y):

		if column == self.SIZE:
			xx = x.toList()[column].toLongLong()
			yy = y.toList()[column].toLongLong()
		else:
			xx = x.toList()[column].toString()
			yy = y.toList()[column].toString()

		if xx > yy:
			return 1
		elif xx == yy:
			return 0
		else:
			return -1

	def compareUsers(self, x, y):
		return self.compare(self.USER, x, y)

	def compareNames(self, x, y):
		return self.compare(self.FILENAME, x, y)

	def compareGroups(self, x, y):
		return self.compare(self.GROUP, x, y)

	def compareSizes(self, x, y):
		return self.compare(self.SIZE, x, y)

	def parent(self, child):

		return QModelIndex()

	def getField(self, row, column):
		
		if column == self.FILENAME or column == self.USER or column == self.GROUP:
			return self.list[row].toList()[column].toString()
		elif column == self.SIZE:
			return self.list[row].toList()[column].toLongLong()
		elif column == self.DIRECTORY or column == self.LINK:
			return self.list[row].toList()[column].toBool()
		else:
			return None

	def setData(self, index, value, role = Qt.DisplayRole):

		if index.row() == len(self.list):
			self.list.append(value)
			self.emit(SIGNAL('layoutChanged()'))
		else:
			self.list[index.row()] = value
			self.emit(SIGNAL('dataChanged(const QModelIndex &, const QModelIndex &)'), index, index)
		return True

	def data(self, index, role = Qt.DisplayRole):

		if index.isValid() == False:
			return QVariant()
		elif index.row() >= len(self.list):
			return QVariant()
		elif role == Qt.DisplayRole:
			return self.list[index.row()].toList()[index.column()]
		elif role == Qt.DecorationRole and index.column() == self.FILENAME:
			return QVariant((self.textplainIcon, self.folderIcon)[self.getField(index.row(), self.DIRECTORY)])
		else:
			return QVariant()

	def headerData(self, section, orientation, role = Qt.DisplayRole):

		if role != Qt.DisplayRole:
			return QVariant()
		if section == self.FILENAME:
			return QVariant("Name")
		elif section == self.USER:
			return QVariant("User")
		elif section == self.GROUP:
			return QVariant("Group")
		elif section == self.SIZE:
			return QVariant("Size")
		else:
			return QVariant()