#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from PyKDE4.kdeui import KIconLoader

class IconButton (QLabel):
	
	def __init__ (self, iconName, parent):

		QLabel.__init__ (self, parent)

		self.iconName = iconName

		#self.setPixmap(configureIcon.pixmap(QSize(22, 22)))

		self.load()

		self.setMouseTracking(True)

	def load(self):

		configurePixmap = KIconLoader.global_().loadIcon(self.iconName, KIconLoader.NoGroup, self.height())

		self.setPixmap(configurePixmap)

	def mouseReleaseEvent(self, event):
		self.emit(SIGNAL("clicked()"))

	def mouseMoveEvent(self, event):
		self.setCursor(Qt.ArrowCursor) 

	def resizeEvent(self, event):
		self.load()