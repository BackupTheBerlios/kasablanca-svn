#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class DirView (QTreeView):

	def __init__ (self, parent):
		
		QTreeView.__init__ (self, parent)

	def dropEvent (self, event):

		if event.source() == self:
			return

		encodedData = event.encodedData("application/vnd.text.list")
		#stream = QDataStream(encodedData, QIODevice.ReadOnly)
		
		#while stream.atEnd() == False:
			#text = QString()
			#stream >> text
			#print "drop: " + text

		#dirModel = self.model()

		self.emit(SIGNAL("drop(QByteArray*)"), encodedData)




