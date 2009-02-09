#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class SessionFrame (QFrame):

	def resizeEvent(self, event):

		self.emit(SIGNAL("sizeChanged(int, int)"), self.width(), self.height())