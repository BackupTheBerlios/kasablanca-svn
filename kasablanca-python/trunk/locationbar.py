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
		self.circle.setGeometry(self.width() - 20, self.height()/2 - 6, self.height()/2, self.height()/2)