#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import ki18n, KAboutData, KCmdLineArgs, KUrl
from PyKDE4.kdeui import KApplication, KMainWindow
from PyKDE4.kio import *

from ftpdirmodel import FtpDirModel
from ui_kasablancamainwindow import Ui_KasablancaMainWindow

class KasablancaMainWindow (KMainWindow, Ui_KasablancaMainWindow):

	def __init__ (self):
		KMainWindow.__init__ (self)
		self.setupUi(self)
		self.ftpModel = FtpDirModel()
		self.treeView.setModel(self.ftpModel)
		self.connect (self.pushButton, SIGNAL("clicked()"), self.slotClicked)
	def slotClicked(self):
		listjob = KIO.listDir(KUrl("ftps://glftpd:glftpd@localhost" ))
		self.connect (listjob, SIGNAL("result (KJob *)"), self.slotResult)
		self.connect (listjob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)
	def slotResult(self, job):
		print "result"
		print len(self.ftpModel.list)
	def slotEntries(self, job, list):
		for entry in list:
			print entry.stringValue(KIO.UDSEntry.UDS_NAME)
			self.ftpModel.list.append(entry)
		self.ftpModel.emit(SIGNAL("const QModelIndex&, const QModelIndex&"))

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