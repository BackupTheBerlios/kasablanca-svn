#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from circlebutton import CircleButton

class LocationBar (QLineEdit):

	def __init__ (self, parent):
		
		QLineEdit.__init__ (self, parent)
		self.circle = CircleButton(self)
		self.connect(self.circle, SIGNAL("clicked()"), self.slotCircleClicked)

	def slotCircleClicked(self): 
		self.emit(SIGNAL("circleClicked()"))	
	
	def resizeEvent(self, event):
		self.circle.setGeometry(self.width() - 19, self.height()/2 - 6, self.height()/2, self.height()/2)

	def getUrl(self):

		text = self.text()
		pos = text.indexOf("/")
		if pos == -1:
			return text
		else:
			return text.left(pos)

	def setKurl(self, kurl):

		self.setText(kurl.host() + kurl.path())

	def getPath(self):

		text = self.text()
		pos = text.indexOf("/")
		if pos == -1:
			return ""
		else:
			return text.right(text.length() - pos)