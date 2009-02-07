#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pickle
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdeui import KMessageBox
from PyKDE4.kdecore import KUrl
from PyKDE4.kio import *
from ftpdirmodel import FtpDirModel

class GuiSession (QObject):

	def __init__ (self, fileView, connectButton, siteButton, hostEdit, userEdit, passEdit, logEdit, tlsCheck):
		self.fileView = fileView
		self.connectButton = connectButton
		self.siteButton = siteButton
		self.hostEdit = hostEdit
		self.userEdit = userEdit
		self.passEdit = passEdit
		self.logEdit = logEdit
		self.tlsCheck = tlsCheck

		self.ftpModel = FtpDirModel()

		self.fileView.setModel(self.ftpModel)

		self.connect(self.connectButton, SIGNAL("clicked()"), self.slotClicked)
		self.connect(self.fileView, SIGNAL("doubleClicked(const QModelIndex&)"), self.slotDoubleClicked)

		#customJob = KIO.get(self.kurl, KIO.Reload, KIO.HideProgressInfo)
		#customJob.addMetaData("kasablanca-cmd", "test")
		#self.connect(customJob, SIGNAL("data (KIO::Job *, const QByteArray &)"), self.slotData)
		#self.connect(customJob, SIGNAL("result (KJob *)"), self.slotResult)

		self.connect(self.siteButton, SIGNAL("clicked()"), self.slotSiteClicked)

		self.kurl = KUrl()

	def slotClicked(self):

		kurl = KUrl()
		kurl.setProtocol("ftps")
		kurl.setUser(self.userEdit.text())
		kurl.setPass(self.passEdit.text())
		kurl.setHost(self.hostEdit.text())
		
		self.attemptKurl = kurl

		print self.attemptKurl

		self.listDir(self.attemptKurl)

	def slotSiteClicked(self):
		
		if self.kurl == "":
			return

		specialJob = KIO.special(self.kurl, "PWD", KIO.HideProgressInfo)
		specialJob.addMetaData("kasablanca-logging", "true")
		self.connect(specialJob, SIGNAL("infoMessage(KJob*, const QString&, const QString&)"), self.slotInfoMessage)
		self.connect(specialJob, SIGNAL("result (KJob *)"), self.slotResult)

	def slotResult(self, job):

		print "result"
		if job.error():
			KMessageBox.sorry(None, job.errorString())

	def slotEntries(self, job, list):

		print "entries"

		self.ftpModel.list = []

		for entry in list:

			name = entry.stringValue(KIO.UDSEntry.UDS_NAME)
			user = entry.stringValue(KIO.UDSEntry.UDS_USER)
			modelIndex = self.ftpModel.createIndex(self.ftpModel.rowCount(), 0)
			self.ftpModel.setData(modelIndex, QVariant([name, user]))

		self.kurl = self.attemptKurl;
	
	def slotDoubleClicked(self, index):

		print "doubleClicked"

		# attempt to change the dir

		self.attemptKurl = KUrl(self.kurl)
		self.attemptKurl.addPath(self.ftpModel.list[index.row()][0])
		self.attemptKurl.cleanPath()

		print self.attemptKurl
	
		self.listDir(self.attemptKurl)

	def slotData(self, job, bytearray):

		print bytearray

	def slotInfoMessage(self, job, plain, rich):

		self.logEdit.appendPlainText(plain)
		#print plain

	def listDir(self, kurl):

		listjob = KIO.listDir(kurl, KIO.HideProgressInfo)
		listjob.addMetaData("kasablanca-logging", "true")
		if self.tlsCheck.isChecked():
			listjob.addMetaData("kasablanca-tls", "true")
			listjob.addMetaData("kasablanca-tls-data", "true")
		else:
			listjob.addMetaData("kasablanca-tls", "false")
			listjob.addMetaData("kasablanca-tls-data", "false")
		self.connect(listjob, SIGNAL("result (KJob *)"), self.slotResult)
		self.connect(listjob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)
		self.connect(listjob, SIGNAL("infoMessage(KJob*, const QString&, const QString&)"), self.slotInfoMessage)