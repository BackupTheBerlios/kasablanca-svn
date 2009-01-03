#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import sys
import pickle
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
		self.fileView.setModel(self.ftpModel)
		self.connect(self.connectButton, SIGNAL("clicked()"), self.slotClicked)
		self.connect(self.fileView, SIGNAL("doubleClicked(const QModelIndex&)"), self.slotDoubleClicked)

		kurl = KUrl()
		kurl.setProtocol("ftps")
		kurl.setUser(self.userEdit.text())
		kurl.setPass(self.passEdit.text())
		kurl.setHost(self.hostEdit.text())
		self.kurl = kurl

		print self.kurl

	def slotClicked(self):

		listjob = KIO.listDir(self.kurl, KIO.HideProgressInfo)
		self.connect (listjob, SIGNAL("result (KJob *)"), self.slotResult)
		self.connect (listjob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)
	def slotResult(self, job):

		print "result"

	def slotEntries(self, job, list):

		print "entries"

		self.ftpModel.list = []

		for entry in list:

			name = entry.stringValue(KIO.UDSEntry.UDS_NAME)
			user = entry.stringValue(KIO.UDSEntry.UDS_USER)
			modelIndex = self.ftpModel.createIndex(self.ftpModel.rowCount(), 0)
			self.ftpModel.setData(modelIndex, QVariant([name, user]))
	
	def slotDoubleClicked(self, index):

		print "doubleClicked"

		# attempt to change the dir

		newkurl = KUrl(self.kurl)
		newkurl.setPath(self.ftpModel.list[index.row()][0])

		print newkurl
	
		listjob = KIO.listDir(newkurl, KIO.HideProgressInfo)
		self.connect (listjob, SIGNAL("result (KJob *)"), self.slotResult)
		self.connect (listjob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)

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