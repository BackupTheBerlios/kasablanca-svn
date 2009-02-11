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
from settingswidget import SettingsWidget

class SessionFrame (QFrame):

	def __init__ (self, parent, ):
		
		QFrame.__init__ (self, parent)

	def init(self, locationBar, fileView, logEdit, siteButton):
		
		self.fileView = fileView
		self.locationBar = locationBar
		self.logEdit = logEdit
		self.siteButton = siteButton

		self.settingsWidget = SettingsWidget(self)
		self.settingsWidget.setVisible(False)

		self.ftpModel = FtpDirModel()
		self.fileView.setModel(self.ftpModel)

		self.connect(self.locationBar, SIGNAL("returnPressed()"), self.slotReturnPressed)
		self.connect(self.fileView, SIGNAL("doubleClicked(const QModelIndex&)"), self.slotDoubleClicked)
		self.connect(self.siteButton, SIGNAL("clicked()"), self.slotSiteClicked)
		self.connect(self.locationBar, SIGNAL("circleClicked()"), self.slotCircleClicked)

		self.kurl = KUrl()

	def resizeEvent(self, event):

		self.emit(SIGNAL("sizeChanged(int, int)"), self.width(), self.height())

	def slotCircleClicked(self):
		if self.settingsWidget.isHidden():
			self.settingsWidget.show()
		else:
			self.settingsWidget.hide()

	def slotReturnPressed(self):

		kurl = KUrl()
		kurl.setProtocol("ftps")
		kurl.setUser(self.settingsWidget.userEdit.text())
		kurl.setPass(self.settingsWidget.passEdit.text())
		kurl.setHost(self.locationBar.getUrl())
		kurl.setPort(int(self.settingsWidget.portEdit.text()))
		kurl.addPath(self.locationBar.getPath())
		kurl.cleanPath()

		self.attemptKurl = kurl

		# print self.attemptKurl

		self.listDir(self.attemptKurl)

	def slotResult(self, job):

		print "result"
		if job.error():
			KMessageBox.sorry(None, job.errorString())

		self.setEnabled(True)

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

		self.kurl = self.attemptKurl
		self.locationBar.setKurl(self.kurl)

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
		if self.settingsWidget.tlsCheck.isChecked():
			job.addMetaData("kasablanca-tls", "true")
			job.addMetaData("kasablanca-tls-data", "true")
		else:
			job.addMetaData("kasablanca-tls", "false")
			job.addMetaData("kasablanca-tls-data", "false")
		self.connect(job, SIGNAL("result (KJob *)"), self.slotResult)
		self.connect(job, SIGNAL("infoMessage(KJob*, const QString&, const QString&)"), self.slotInfoMessage)
		self.connect(job, SIGNAL("percent(KJob*, unsigned long)"), self.slotPercent)  

		self.setEnabled(False)

	def copyFile(self, srcKurl, dstKurl):
		
		copyJob = KIO.copy(srcKurl, dstKurl, KIO.HideProgressInfo)
		self.doJobDefaults(copyJob)
		self.progressWidget = ProgressWidget(self)
		self.progressWidget.show()

	def listDir(self, kurl):

		listJob = KIO.listDir(kurl, KIO.HideProgressInfo)
		self.doJobDefaults(listJob)
		self.connect(listJob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)