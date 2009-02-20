#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from iconbutton import IconButton
from circlebutton import CircleButton

class LocationBar (QLineEdit):

	def __init__ (self, parent):
		
		QLineEdit.__init__ (self, parent)
		#self.configureButton = IconButton("configure", self)	
		self.configureButton = CircleButton(self)

		#self.returnButton = IconButton("go-jump-locationbar", self)
	
		self.normalColor = self.palette().color(QPalette.Text)
		self.brightColor = self.normalColor.lighter(500)

		self.currentUrl = ""

		self.connect(self, SIGNAL("textChanged(const QString&)"), self.slotTextChanged)

	def resizeEvent(self, event):
		self.configureButton.setGeometry(self.width() - self.height()/4*3, self.height()/4, self.height()/2, self.height()/2)
		#self.returnButton.setGeometry(self.width() - self.height()/4*3 - self.height()/2, self.height()/4, self.height()/2, self.height()/2)

	def slotTextChanged(self, text):

		self.setBrightText(text != self.currentUrl)

	def getUrlString(self):

		# a string beginning with / indicates a local directory

		text = self.text()
		pos = text.indexOf("/")
		if pos == 0: 
			return None;
		elif pos == -1:
			return text
		else:
			return text.left(pos)

	def setKurl(self, kurl):

		self.currentUrl = kurl.host() + kurl.path()
		self.setText(self.currentUrl)

		self.setBrightText(False)

	def setBrightText(self, bright):

		palette = QPalette()

		if bright == True:
			palette.setColor(QPalette.Text, self.brightColor)
		else:
			palette.setColor(QPalette.Text, self.normalColor)

		self.setPalette(palette)

	def getPathString(self):

		text = self.text()
		pos = text.indexOf("/")
		if pos == 0:
			return text;
		elif pos == -1:
			return ""
		else:
			return text.right(text.length() - pos)