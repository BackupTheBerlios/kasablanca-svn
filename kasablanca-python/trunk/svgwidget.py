#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

class SvgWidget (QSvgWidget):

	def __init__ (self, parent):
		
		QSvgWidget.__init__ (self, parent)

		self.connect(parent, SIGNAL("sizeChanged(int, int)"), self.slotSizeChanged)
		self.slotSizeChanged(parent.width(), parent.height())

	def slotSizeChanged(self, width, height):
		pass

	def xmlString(self):
		pass