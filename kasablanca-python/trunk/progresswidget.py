#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *

class ProgressWidget (QSvgWidget):

	def __init__ (self, frame):
		
		QSvgWidget.__init__ (self, frame)

		self.opacity0 = 1.0
		self.opacity1 = 1.0
		self.opacity2 = 1.0
		self.opacity3 = 1.0

		self.load(QByteArray(self.xmlString()))
		#self.load("progress.svg");
		self.move(60, 120)
		self.setFixedSize(300, 170)

	def setPercent(self,percent):
		
		opacity = 1.00 - ((percent % 25) / 25.0)

		if percent < 25:
			self.opacity0, self.opacity1, self.opacity2, self.opacity3 = opacity, 1, 1, 1 
		elif percent < 50:
			self.opacity0, self.opacity1, self.opacity2, self.opacity3 = 0, opacity, 1, 1
		elif percent < 75:
			self.opacity0, self.opacity1, self.opacity2, self.opacity3 = 0, 0, opacity, 1
		elif percent < 100:
			self.opacity0, self.opacity1, self.opacity2, self.opacity3 = 0, 0, 0, opacity
		else:
			self.opacity0, self.opacity1, self.opacity2, self.opacity3 = 0, 0, 0, 0

		self.load(QByteArray(self.xmlString()))

	def minimumSizeHint(self):
		return QSize(100, 100)

	def xmlString(self):

		return '<?xml version="1.0" encoding="UTF-8" standalone="no"?> <!-- Created with Inkscape (http://www.inkscape.org/) --> <svg    xmlns:dc="http://purl.org/dc/elements/1.1/"    xmlns:cc="http://creativecommons.org/ns#"    xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"    xmlns:svg="http://www.w3.org/2000/svg"    xmlns="http://www.w3.org/2000/svg"    xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd"    xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape"    width="1040"    height="600"    id="svg2"    sodipodi:version="0.32"    inkscape:version="0.46"    version="1.0"    sodipodi:docname="progress.svg"    inkscape:output_extension="org.inkscape.output.svg.inkscape">   <defs      id="defs4">     <inkscape:perspective        sodipodi:type="inkscape:persp3d"        inkscape:vp_x="0 : 526.18109 : 1"        inkscape:vp_y="6.1230318e-14 : 1000 : 0"        inkscape:vp_z="744.09448 : 526.18109 : 1"        inkscape:persp3d-origin="372.04724 : 350.78739 : 1"        id="perspective10" />   </defs>   <sodipodi:namedview      id="base"      pagecolor="#ffffff"      bordercolor="#666666"      borderopacity="1.0"      inkscape:pageopacity="0.0"      inkscape:pageshadow="2"      inkscape:zoom="0.24748737"      inkscape:cx="303.30691"      inkscape:cy="42.283092"      inkscape:document-units="px"      inkscape:current-layer="layer1"      showgrid="true"      width="400px"      inkscape:snap-global="true"      objecttolerance="5"      gridtolerance="10"      guidetolerance="10"      inkscape:snap-bbox="true"      inkscape:snap-center="true"      inkscape:snap-intersection-line-segments="true"      inkscape:bbox-nodes="true"      inkscape:bbox-paths="true"      inkscape:object-nodes="true"      inkscape:object-paths="true"      inkscape:window-width="843"      inkscape:window-height="692"      inkscape:window-x="0"      inkscape:window-y="0">     <inkscape:grid        type="xygrid"        id="grid2393"        visible="true"        enabled="true" />   </sodipodi:namedview>   <metadata      id="metadata7">     <rdf:RDF>       <cc:Work          rdf:about="">         <dc:format>image/svg+xml</dc:format>         <dc:type            rdf:resource="http://purl.org/dc/dcmitype/StillImage" />       </cc:Work>     </rdf:RDF>   </metadata>   <g      inkscape:label="Ebene 1"      inkscape:groupmode="layer"      id="layer1">     <rect        style="opacity:0.5;fill:#505050;fill-opacity:1;fill-rule:evenodd;stroke:none;stroke-width:1.80810523px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:0.36734697"        id="rect2435"        width="1040"        height="600"        x="-2.0428104e-14"        y="-2.3790494e-14"        rx="89.858063"        ry="84.813347" />     <rect        style="fill:#c8c8c8;fill-opacity:' + str(self.opacity0) + ';fill-rule:evenodd;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"        id="bar0"        width="160"        height="440"        x="80"        y="80"        rx="41.157276"        ry="38.599133"        inkscape:label="#rect3253" />     <rect        style="fill:#c8c8c8;fill-opacity:' + str(self.opacity1) + ';fill-rule:evenodd;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"        id="bar1"        width="160"        height="440"        x="320"        y="80"        rx="41.157276"        ry="38.599133"        inkscape:label="#rect3297" />     <rect        style="fill:#c8c8c8;fill-opacity:' + str(self.opacity2) + ';fill-rule:evenodd;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1"        id="bar2" width="160" height="440" x="560" y="80" rx="41.157276" ry="38.599133" inkscape:label="#rect3299" /><rect style="fill:#c8c8c8;fill-opacity:' + str(self.opacity3) + ';fill-rule:evenodd;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;opacity:1" id="bar3"        width="160" height="440" x="800" y="80" rx="41.157276" ry="38.599133" inkscape:label="#rect3301" /></g></svg>'