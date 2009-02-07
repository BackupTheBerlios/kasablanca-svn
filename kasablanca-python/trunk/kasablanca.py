#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs
from PyKDE4.kdeui import KApplication, KMainWindow

from guisession import GuiSession
from ui_kasablancamainwindow import Ui_KasablancaMainWindow

class KasablancaMainWindow (KMainWindow, Ui_KasablancaMainWindow):

	def __init__ (self):

		KMainWindow.__init__ (self)
		self.setupUi(self)

		self.guiSession = GuiSession(self.fileView, self.connectButton, self.siteButton, self.hostEdit, self.userEdit, self.passEdit, self.logEdit, self.tlsCheck)

		self.guiSession_2 = GuiSession(self.fileView_2, self.connectButton_2, self.siteButton_2, self.hostEdit_2, self.userEdit_2, self.passEdit_2, self.logEdit_2, self.tlsCheck_2)

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
		
	app = KApplication ()
	mainWindow = KasablancaMainWindow ()
	mainWindow.show()
	app.exec_ ()