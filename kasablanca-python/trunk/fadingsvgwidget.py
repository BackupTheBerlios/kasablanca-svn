#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from svgwidget import SvgWidget

class FadingSvgWidget (SvgWidget):

	def __init__ (self, parent):
		
		SvgWidget.__init__ (self, parent)

		self.globalOpacity = 0.5

	def show(self):
		QSvgWidget.show(self)
		self.fade(True)

	def hide(self):
		self.fade(False)

	def fade(self, fadeIn):
		timeLine = QTimeLine(1000, self)
		timeLine.setCurveShape(QTimeLine.LinearCurve)
		timeLine.setFrameRange(0, 50)
		if fadeIn == True:
			self.connect(timeLine, SIGNAL("frameChanged(int)"), self.opacityUp)
		else:
			self.connect(timeLine, SIGNAL("frameChanged(int)"), self.opacityDown)
		timeLine.start()

	def opacityUp(self, value):

		self.globalOpacity = value/50.0
		self.load(QByteArray(self.xmlString()))

	def opacityDown(self, value):

		self.globalOpacity = 1.0 - value/50.0

		if self.globalOpacity == 0:
			QSvgWidget.hide(self)
		else:	
			self.load(QByteArray(self.xmlString()))