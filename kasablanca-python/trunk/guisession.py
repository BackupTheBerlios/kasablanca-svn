#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyKDE4.kdeui import KMessageBox
from PyKDE4.kdecore import KUrl
from PyKDE4.kio import *

from progresswidget import ProgressWidget
from ftpdirmodel import FtpDirModel

class GuiSession (QObject):

	def __init__ (self, frame, fileView, connectButton, siteButton, hostEdit, userEdit, passEdit, logEdit, tlsCheck):
		self.frame = frame
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

		self.progressWidget = ProgressWidget(frame)
		self.progressWidget.hide()
	
	def slotClicked(self):

		kurl = KUrl()
		kurl.setProtocol("ftps")
		kurl.setUser(self.userEdit.text())
		kurl.setPass(self.passEdit.text())
		kurl.setHost(self.hostEdit.text())
		
		self.attemptKurl = kurl

		# print self.attemptKurl

		self.listDir(self.attemptKurl)

	def slotResult(self, job):

		print "result"
		if job.error():
			KMessageBox.sorry(None, job.errorString())

		self.progressWidget.hide()
		self.frame.setEnabled(True)

	def slotEntries(self, job, entries):

		print "entries"

		self.ftpModel.list = []

		for entry in entries:

			variantList = [
				entry.stringValue(KIO.UDSEntry.UDS_NAME),
				entry.stringValue(KIO.UDSEntry.UDS_USER),
				entry.stringValue(KIO.UDSEntry.UDS_GROUP),
				entry.numberValue(KIO.UDSEntry.UDS_SIZE),
				entry.isDir(),
				entry.isLink()
			]

			modelIndex = self.ftpModel.createIndex(self.ftpModel.rowCount(), 0)

			self.ftpModel.setData(modelIndex, QVariant(variantList))

		self.kurl = self.attemptKurl;
	
	def slotDoubleClicked(self, index):

		print "doubleClicked"

		fileName = self.ftpModel.getField(index.row(), FtpDirModel.FILENAME)

		if self.ftpModel.getField(index.row(), FtpDirModel.DIRECTORY) == True:

			# attempt to change the dir

			self.attemptKurl = KUrl(self.kurl)
			self.attemptKurl.addPath(fileName)
			self.attemptKurl.cleanPath()

			# print self.attemptKurl
	
			self.listDir(self.attemptKurl)
		else:
			filePath = KFileDialog.getSaveFileName(KUrl(QDir.homePath() + "/" + fileName))

			if filePath != "":
				srcKurl = KUrl(self.kurl)
				srcKurl.addPath(fileName)
				self.copyFile(srcKurl, KUrl(filePath))

	def slotSiteClicked(self):
		
		if self.kurl == "":
			return

		specialJob = KIO.special(self.kurl, "SITE HELP", KIO.HideProgressInfo)
		self.doJobDefaults(specialJob)

	def slotData(self, job, bytearray):

		print bytearray

	def slotInfoMessage(self, job, plain, rich):

		self.logEdit.appendPlainText(plain)
		#print plain

	def slotPercent(self, job, percent):

		self.progressWidget.setPercent(percent)

	def doJobDefaults(self, job):
		
		job.addMetaData("kasablanca-logging", "true")
		if self.tlsCheck.isChecked():
			job.addMetaData("kasablanca-tls", "true")
			job.addMetaData("kasablanca-tls-data", "true")
		else:
			job.addMetaData("kasablanca-tls", "false")
			job.addMetaData("kasablanca-tls-data", "false")
		self.connect(job, SIGNAL("result (KJob *)"), self.slotResult)
		self.connect(job, SIGNAL("infoMessage(KJob*, const QString&, const QString&)"), self.slotInfoMessage)
		self.connect(job, SIGNAL("percent(KJob*, unsigned long)"), self.slotPercent)  

		self.frame.setEnabled(False)

	def copyFile(self, srcKurl, dstKurl):
		
		copyJob = KIO.copy(srcKurl, dstKurl, KIO.HideProgressInfo)
		self.doJobDefaults(copyJob)
		self.progressWidget.setPercent(0)
		self.progressWidget.show()

	def listDir(self, kurl):

		listJob = KIO.listDir(kurl, KIO.HideProgressInfo)
		self.doJobDefaults(listJob)
		self.connect(listJob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)