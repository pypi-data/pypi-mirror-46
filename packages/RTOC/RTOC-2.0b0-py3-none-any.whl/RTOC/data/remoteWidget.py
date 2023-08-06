from PyQt5 import QtCore
from PyQt5 import uic
from PyQt5 import QtWidgets, QtGui
import pyqtgraph as pg
import os
import sys

from . import define as define
from .lib import pyqt_customlib as pyqtlib

class RemoteWidget(QtWidgets.QWidget):
    def __init__(self, selfself, remotehost="", parent=None):
        super(RemoteWidget, self).__init__()
        if getattr(sys, 'frozen', False):
            # frozen
            packagedir = os.path.dirname(sys.executable)+'/RTOC/data'
        else:
            # unfrozen
            packagedir = os.path.dirname(os.path.realpath(__file__))
        uic.loadUi(packagedir+"/ui/remoteHostWidget.ui", self)
        self.setWindowTitle(remotehost)
        #elf.setWindowFlags(self.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
        self.self=selfself
        self.hostname=remotehost
        self.parent=parent
        self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.listItemRightClicked)

        self.disconnectButton.clicked.connect(self.disconnect)
        self.maxLengthSpinBox.editingFinished.connect(self.resizeRemoteLogger)
        self.clearButton.clicked.connect(self.clear)
        self.pauseButton.clicked.connect(self.pause)
        self.remote = self.self.logger.remote.getConnection(self.hostname)
        if self.remote!=None:
            self.maxLengthSpinBox.setValue(self.remote.maxLength)
            self.updateList()
            self.pauseButton.setChecked(self.remote.pause)
            if self.remote.run==True:
                self.statusLabel.setText('Verbunden')
            else:
                self.statusLabel.setText('Fehler')

    def disconnect(self):
        ans = pyqtlib.alert_message('Verbindung trennen', 'Möchtest du die Verbindung zu '+self.hostname+' trennen?', 'Übertragene Signale bleiben bestehen', "", "Ja", "Nein")
        if ans:
            ans = self.self.logger.remote.disconnect(self.hostname)
            if ans == False:
                ans = pyqtlib.info_message('Fehler', 'Konnte die Verbindung zu '+self.hostname+' nicht trennen.', '')
            self.close()

    def resizeRemoteLogger(self):
        self.self.logger.remote.resize(self.hostname, self.maxLengthSpinBox.value())

    def something(self):
        if self.checkBox.isChecked():
            selection = self.remote.siglist
            selection = [".".join(i) for i in selection]
        else:
            selection = []
            for o in self.listWidget.selectedItems():
                selection.append(o.text())

    def updateList(self):
        t = []
        for o in self.listWidget.selectedItems():
            t.append(o.text())
        self.listWidget.clear()
        for sig in self.remote.siglist:
            self.listWidget.addItem('.'.join(sig))
        for idx in range(self.listWidget.count()):
            sig = self.listWidget.item(idx)
            if sig.text() in t:
                self.listWidget.item(idx).setSelected(True)
        # now tell RTRemote to only listen to selected Items

    def plotSignals(self):
        pass

    def closeEvent(self, event, *args, **kwargs):
        self.parent.close()
        super(RemoteWidget, self).closeEvent(event)

    def toggleCheckAll(self, state):
        for idx in range(self.listWidget.count()):
            self.listWidget.item(idx).setSelected(state)

    def listItemRightClicked(self, QPos):
        self.listMenu= QtGui.QMenu()
        menu_item = self.listMenu.addAction("Signal löschen")
        menu_item.triggered.connect(self.menuItemClicked)
        parentPosition = self.listWidget.mapToGlobal(QtCore.QPoint(0, 0))
        self.listMenu.move(parentPosition + QPos)
        self.listMenu.show()

    def menuItemClicked(self):
        currentItemName=str(self.listWidget.currentItem().text() )
        self.self.logger.remote.clearHost(self.hostname,[currentItemName])

    def clear(self):
        self.self.logger.remote.clearHost(self.hostname,'all')

    def pause(self, value):
        self.self.logger.remote.pauseHost(self.hostname,value)
