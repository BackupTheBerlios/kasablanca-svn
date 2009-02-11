#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from fadingsvgwidget import FadingSvgWidget

class ProgressWidget (FadingSvgWidget):

	def __init__ (self, frame):
		
		FadingSvgWidget.__init__ (self, frame)

		self.containerOpacity = 0.5
		self.barOpacity = [1.0, 1.0, 1.0, 1.0]

	def center(self, width, height):
		
		self.setGeometry((width*20)/100, (height*32)/100, (width*60)/100, (height*30)/100)

	def slotSizeChanged(self, width, height):
	
		self.center(width, height)

	def setPercent(self, percent):
		
		if percent == 100:
			self.hide()
		else:
			opacity = 1.00 - ((percent % 25) / 25.0)
			bar = percent / 25
			self.barOpacity[bar] = opacity
			self.load(QByteArray(self.xmlString()))

	def xmlString(self):

		xml = '<?xml version="1.0" standalone="no"?>'
		xml += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
		xml += '<svg viewBox = "0 0 525 300" version = "1.1" opacity = "' + str(self.globalOpacity) + '">'
		xml += '<rect id="container" x = "0" y = "0" width = "525" height = "300" rx = "25" ry = "25" fill = "grey" fill-opacity = "' + str(self.containerOpacity) + '"/>'
		xml += '<rect id="bar0" x = "25" y = "25" width = "100" height = "250" rx = "10" ry = "10" fill = "lightgray" fill-opacity = "' + str(self.barOpacity[0]) + '"/>'
		xml += '<rect id="bar1" x = "150" y = "25" width = "100" height = "250" rx = "10" ry = "10" fill = "lightgray" fill-opacity = "' + str(self.barOpacity[1]) + '"/>'
		xml += '<rect id="bar2" x = "275" y = "25" width = "100" height = "250" rx = "10" ry = "10" fill = "lightgray" fill-opacity = "' + str(self.barOpacity[2]) + '"/>'
		xml += '<rect id="bar3" x = "400" y = "25" width = "100" height = "250" rx = "10" ry = "10" fill = "lightgray" fill-opacity = "' + str(self.barOpacity[3]) + '"/>'
		xml += '</svg>'

		return xml