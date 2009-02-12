#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

from svgwidget import SvgWidget
from ui_settingswidget import Ui_SettingsWidget

class SettingsWidget (SvgWidget, Ui_SettingsWidget):

	def __init__ (self, parent):
		
		SvgWidget.__init__ (self, parent)
		self.setupUi(self)

		self.containerOpacity = 0.75
		self.load(QByteArray(self.xmlString()))

	def slotSizeChanged(self, width, height):
	
		self.setGeometry((width*20)/100, (height*17)/100, (width*60)/100, (height*20)/100)
		#self.setGeometry(20, 25, width - 40, height/4 - 20)

	def xmlString(self):

		xml = '<?xml version="1.0" standalone="no"?>'
		xml += '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
		xml += '<svg viewBox = "0 0 525 150" version = "1.1">'
		xml += '<rect id="container" x = "0" y = "0" width = "525" height = "150" rx = "10" ry = "10" fill = "lightgray" fill-opacity = "' + str(self.containerOpacity) + '"/>'
		xml += '</svg>'

		return xml