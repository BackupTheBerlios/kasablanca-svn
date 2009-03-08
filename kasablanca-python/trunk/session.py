#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSvg import *
from PyKDE4.kdeui import KMessageBox
from PyKDE4.kdecore import KUrl
from PyKDE4.kio import *

from progresswidget import ProgressWidget
from dirmodel import DirModel
from settingswidget import SettingsWidget

class Session (QObject):

	def __init__(self, frame, locationBar, dirView, logEdit, siteButton):

		QObject.__init__(self)

		self.frame = frame
		self.dirView = dirView
		self.locationBar = locationBar
		self.logEdit = logEdit
		self.siteButton = siteButton

		self.settingsWidget = SettingsWidget(self.frame)
		self.settingsWidget.setVisible(False)

		self.progressWidget = ProgressWidget(self.frame)
		self.progressWidget.setVisible(False)

		self.dirModel = DirModel()
		self.dirView.setModel(self.dirModel)

		# enable sorting

		self.connect(self.dirView.header(), SIGNAL("sectionClicked(int)"), self.dirView.sortByColumn)

		# set filename & ascending to default

		self.dirView.header().setSortIndicator(DirModel.FILENAME, Qt.AscendingOrder)

		self.connect(self.locationBar, SIGNAL("returnPressed()"), self.slotReturnPressed)
		self.connect(self.dirView, SIGNAL("doubleClicked(const QModelIndex&)"), self.slotDoubleClicked)
		self.connect(self.siteButton, SIGNAL("clicked()"), self.slotSiteClicked)
		self.connect(self.locationBar.configureButton, SIGNAL("clicked()"), self.slotConfigureButtonClicked)

		# connect drop signal

		self.connect(self.dirView, SIGNAL("drop(QByteArray*)"), self.slotDrop)

		# default to home directory

		kurl = KUrl()
		kurl.setProtocol("file");
		kurl.setPath(QDir.homePath());
		
		self.attemptKurl = kurl;
		self.listDir(self.attemptKurl);

	def slotDrop(self, encodedData):
		
		stream = QDataStream(encodedData, QIODevice.ReadOnly)

		fileInfoList = list()

		while stream.atEnd() == False:

			fileInfos = QVariant()
			stream >> fileInfos
			fileInfoList.append(fileInfos)

		self.emit(SIGNAL("transfer(PyQt_PyObject, QString, bool)"), self, fileInfoList[0].toList()[DirModel.FILENAME].toString(), False)

		# TODO: queue rest

		#print "filename: " + fileInfos.toList()[DirModel.FILENAME].toString() + " directory: " + str(fileInfos.toList()[DirModel.DIRECTORY].toBool()) + " link: " + str(fileInfos.toList()[DirModel.LINK].toBool())

	def slotConfigureButtonClicked(self):
		if self.settingsWidget.isHidden():
			self.settingsWidget.show()
		else:
			self.settingsWidget.hide()

	def slotReturnPressed(self):

		kurl = KUrl()
		if (self.locationBar.getUrlString() != None):
			kurl.setProtocol("ftps")
			kurl.setHost(self.locationBar.getUrlString())
		else:
			kurl.setProtocol("file")
		kurl.setUser(self.settingsWidget.userEdit.text())
		kurl.setPass(self.settingsWidget.passEdit.text())
		kurl.setPort(int(self.settingsWidget.portEdit.text()))
		kurl.addPath(self.locationBar.getPathString())
		kurl.cleanPath()

		self.attemptKurl = kurl

		# print self.attemptKurl

		self.listDir(self.attemptKurl)

	def slotResult(self, job):

		print "result"
		if job.error():
			KMessageBox.sorry(None, job.errorString())
			if self.progressWidget.isVisible():
				self.progressWidget.hide()

		self.frame.setEnabled(True)

	def slotEntries(self, job, entries):

		print "entries"

		self.dirModel.list = []

		for entry in entries:

			# the last to entries do not appear as columns in dirview

			variantList = [
				entry.stringValue(KIO.UDSEntry.UDS_NAME),
				entry.stringValue(KIO.UDSEntry.UDS_USER),
				entry.stringValue(KIO.UDSEntry.UDS_GROUP),
				entry.numberValue(KIO.UDSEntry.UDS_SIZE),
				entry.isDir(),
				entry.isLink()
			]

			modelIndex = self.dirModel.createIndex(self.dirModel.rowCount(), 0)

			if (entry.stringValue(KIO.UDSEntry.UDS_NAME) != "."):
				self.dirModel.setData(modelIndex, QVariant(variantList))

		self.dirView.sortByColumn(self.dirView.header().sortIndicatorSection(), self.dirView.header().sortIndicatorOrder())

		self.kurl = self.attemptKurl
		self.locationBar.setKurl(self.kurl)

	def slotDoubleClicked(self, index):

		print "doubleClicked"

		fileName = self.dirModel.getField(index.row(), DirModel.FILENAME)

		if self.dirModel.getField(index.row(), DirModel.DIRECTORY) == True:

			# attempt to change the dir

			self.attemptKurl = KUrl(self.kurl)
			self.attemptKurl.addPath(fileName)
			self.attemptKurl.cleanPath()

			# print self.attemptKurl
	
			self.listDir(self.attemptKurl)
		else:

			self.emit(SIGNAL("transfer(PyQt_PyObject, QString, bool)"), self, fileName, True)

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

		self.frame.setEnabled(False)

	def copyFile(self, srcKurl, dstKurl):
		
		copyJob = KIO.copy(srcKurl, dstKurl, KIO.HideProgressInfo)
		self.doJobDefaults(copyJob)
		self.connect(copyJob, SIGNAL("percent(KJob*, unsigned long)"), self.slotPercent)	
		self.progressWidget.show()

	def listDir(self, kurl):

		listJob = KIO.listDir(kurl, KIO.HideProgressInfo)
		self.doJobDefaults(listJob)
		self.connect(listJob, SIGNAL("entries (KIO::Job *, const KIO::UDSEntryList&)"), self.slotEntries)

