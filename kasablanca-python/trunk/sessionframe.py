#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SessionFrame (QFrame):

	def __init__ (self, parent, ):
		
		QFrame.__init__ (self, parent)

	def resizeEvent(self, event):

		self.emit(SIGNAL("sizeChanged(int, int)"), self.width(), self.height())
