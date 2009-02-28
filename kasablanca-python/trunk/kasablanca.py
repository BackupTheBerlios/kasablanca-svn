#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KUrl
from PyKDE4.kdeui import KApplication, KMainWindow

from session import Session
from ui_kasablancamainwindow import Ui_KasablancaMainWindow

class KasablancaMainWindow (KMainWindow, Ui_KasablancaMainWindow):

	def __init__ (self):

		KMainWindow.__init__ (self)
		self.setupUi(self)

		self.session = Session(self.frame, self.locationBar, self.dirView, self.logEdit, self.siteButton)
		self.session_2 = Session(self.frame_2, self.locationBar_2, self.dirView_2, self.logEdit_2, self.siteButton_2)

		self.connect(self.session, SIGNAL("transfer(PyQt_PyObject, QString)"), self.transfer)
		self.connect(self.session_2, SIGNAL("transfer(PyQt_PyObject, QString)"), self.transfer)

	def transfer(self, session, fileName):
	
		srcSession = (self.session, self.session_2)[session != self.session]
		dstSession = (self.session_2, self.session)[session != self.session]

		srcKurl = KUrl(srcSession.kurl)
		srcKurl.addPath(fileName)

		dstKurl = KUrl(dstSession.kurl)
		dstKurl.addPath(fileName)

		print "transfer " + srcKurl.prettyUrl() + " to " + dstKurl.prettyUrl()

		session.copyFile(srcKurl, dstKurl)

if __name__ == '__main__':

	appName     = "kasablanca"
	catalog     = ""
	programName = ki18n ("kasablanca")
	version     = "0.5"
	description = ki18n ("kasablanca ftp client")
	license     = KAboutData.License_GPL
	copyright   = ki18n ("(c) 2008 Magnus Kulke")
	text        = ki18n ("none")
	homePage    = "kasablanca.berlios.de"
	bugEmail    = "mkulke@bla.com"

	aboutData   = KAboutData (appName, catalog, programName, version, description, license, copyright, text, homePage, bugEmail)
			
	KCmdLineArgs.init (sys.argv, aboutData)
		
	app = KApplication()
	mainWindow = KasablancaMainWindow()
	mainWindow.show()
	app.exec_ ()