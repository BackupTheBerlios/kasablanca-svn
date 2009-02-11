#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from svgwidget import SvgWidget

class CircleButton (SvgWidget):
	
	def __init__ (self, parent):
		
		SvgWidget.__init__ (self, parent)

		self.setMouseTracking(True)
		
	def xmlString(self):

		xml = '<?xml version="1.0" standalone="no"?>'
		xml += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
		xml += '<svg viewBox = "0 0 12 12" version = "1.1">'
		xml += '<circle cx="6" cy="6" r="6" fill = "grey"/>'
		#xml += '<polygon points="2,3 10,3 6,11" fill = "lightgray"/>'
		xml += '</svg>'

		return QByteArray(xml)

	def mouseReleaseEvent(self, event):
		self.emit(SIGNAL("clicked()"))

	def mouseMoveEvent(self, event):
		self.setCursor(Qt.ArrowCursor) 

	def slotSizeChanged(self, width, height):
		self.load(self.xmlString())