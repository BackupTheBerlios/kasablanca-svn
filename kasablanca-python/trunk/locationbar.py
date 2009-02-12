#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from iconbutton import IconButton

class LocationBar (QLineEdit):

	def __init__ (self, parent):
		
		QLineEdit.__init__ (self, parent)
		self.configureButton = IconButton("configure", self)	
	
	def resizeEvent(self, event):
		self.configureButton.setGeometry(self.width() - 19, self.height()/2 - 6, self.height()/2, self.height()/2)

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