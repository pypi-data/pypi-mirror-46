import time
from threading import Thread
import traceback

try:
    import data.lib.pyqt_customlib as pyqtlib
    from LoggerPlugin import LoggerPlugin
except ImportError:
    from RTOC.LoggerPlugin import LoggerPlugin
    import RTOC.data.lib.pyqt_customlib as pyqtlib

from PyQt5.QtCore import QCoreApplication

translate = QCoreApplication.translate

class SingleConnection(LoggerPlugin):
    def __init__(self, stream=None, plot= None, event=None, host='127.0.0.1',port=5050):
        # Plugin setup
        super(SingleConnection, self).__init__(stream, plot, event)
        self.setDeviceName(host)
        self.host = host
        self.port=port
        self.run = False  # False -> stops thread
        self.pause= False
        self.samplerate=1
        self.maxLength = 0

        self.siglist = []
        self.pluglist = []
        self.eventlist = {}
        #self.createTCPClient(host, None, port)
        self.tcppassword = None
        self.start()

    # THIS IS YOUR THREAD
    def updateT(self):
        diff = 0
        while self.run:
            if self.samplerate > 0:
                if diff < 1/self.samplerate:
                    time.sleep(1/self.samplerate-diff)
            start_time = time.time()
            if not self.pause:
                ans = self.sendTCP(getSignalList= True, getPluginList = True, logger={'info': True}, getEventList= True)
                if ans:
                    if 'signalList' in ans.keys():
                        if ans['signalList'] != self.siglist:
                            self.siglist = ans['signalList']
                            #self.updateList()
                    if 'pluginList' in ans.keys():
                        if ans['pluginList'] != self.pluglist:
                            self.pluglist = ans['pluginList']
                            #self.widget.updateDevices.emit(self.pluglist)
                    #if self.widget.streamButton.isChecked():
                        #self.plotSignals()
                    if 'logger' in ans.keys():
                        maxLength = ans['logger']['info']['recordLength']
                        if maxLength != self.maxLength:
                            self.maxLength = maxLength
                            #self.widget.maxLengthSpinBox.setValue(self.maxLength)
                    if 'events' in ans.keys():
                        if ans['events'] != self.eventlist:
                            #self.widget.updateDevices.emit(self.eventlist)
                            self.updateEvents(ans['events'])
                    if self.siglist != []:
                        selection = self.siglist
                        selection = [".".join(i) for i in selection]
                        ans = self.sendTCP(getSignal= selection)

                        if ans != False:
                            if 'signals' in ans.keys():
                                for sig in ans['signals'].keys():
                                    signame = sig.split('.')
                                    s = ans['signals'][sig]
                                    u = s[2]
                                    self.plot(s[0],s[1],sname = signame[1], dname=signame[0]+"_Remote", unit=u)
            diff = time.time() - start_time

    def updateEvents(self, newEventList):
        for dev in newEventList.keys():
            if dev not in self.eventlist.keys():
                self.eventlist[dev]=[[],[]]
            for idx, ev in enumerate(newEventList[dev][0]):
                if ev not in self.eventlist[dev][0]:
                    device = dev.split('.')
                    self.event(x = ev, text = newEventList[dev][1][idx], sname=device[1], dname=device[0]+"_Remote", priority=0)
        self.eventlist = newEventList

    def resizeLogger(self, newsize):
        ans = self.sendTCP(logger={'resize':newsize})
        if ans:
            self.maxLength = newsize
        return ans

    def toggleDevice(self, plugin, state):
        ans = self.sendTCP(plugin={plugin: {'start':state}})
        return ans

    def clear(self, signals=[]):
        if signals == []:
            signals='all'
        ans = self.sendTCP(logger={'clear': signals})
        #print(ans)

    def stop(self):
        self.run=False
        self.siglist = []
        self.pluglist = []
        self.eventlist = {}

    def start(self):
        if self.run:
            self.run = False
        else:
            self.createTCPClient(self.host, self.tcppassword, self.port)
            self.run = True
            try:
                ok = self.sendTCP()
                if ok is None:
                    text, ok2 = pyqtlib.text_message(self, translate('NetWoRTOC','Passwort'), translate('NetWoRTOC',"Der RTOC-Server ")+self.host+translate('NetWoRTOC'," ist passwortgeschützt. Bitte Passwort eintragen"), translate('NetWoRTOC','TCP-Passwort'))
                    if ok2:
                        self.tcppassword = text
                        self.start()
                        return
                    else:
                        ok = None
                elif ok != False:
                    ok = True
            except:
                ok = False
            if ok:
                self.run = True
                self.__updater = Thread(target=self.updateT)
                self.__updater.start()
                pyqtlib.info_message('Verbindung hergestellt', 'Verbindung zu '+self.host+' an Port '+str(self.port)+' hergestellt.','')
            elif ok is False:
                self.__base_address = ""
                self.run = False
                ok = pyqtlib.alert_message('Verbindungsfehler', 'Fehler. Verbindung zu '+self.host+' an Port '+str(self.port)+' konnte nicht hergestellt werden.','Erneut versuchen?')
                if ok:
                    self.start()
            else:
                self.__base_address = ""
                self.run = False
                pyqtlib.alert_message('Geschützt', 'Verbindung zu '+self.host+' an Port '+str(self.port)+' wurde nicht hergestellt.','Passwort ist falsch.')

    def callPluginFunction(self,device, function, parameter):
        ans = self.sendTCP(plugin={device: {function:parameter}})
        return ans


class RTRemote():
    def __init__(self, parent= None):
        # Data-logger thread

        #self.__updater = Thread(target=self.updateT)    # Actualize data
        # self.updater.start()
        self.logger= parent
        self.config = parent.config

        self.connections = []

    def stop(self):
        for c in self.connections:
            c.stop()
        self.connections=[]

    def setSamplerate(self,samplerate=1):
        for c in self.connections:
            c.samplerate=samplerate

    def connect(self, hostname='127.0.0.1', port=5050):
        if len(hostname.split(':'))==2:
            port = int(hostname.split(':')[1])
            hostname=hostname.split(':')[0]
        newConnection = SingleConnection(self.logger.addDataCallback, self.logger.plot, self.logger.addNewEvent, hostname, port)
        self.connections.append(newConnection)

    def disconnect(self, hostname):
        if len(hostname.split(':'))==2:
            hostname=hostname.split(':')[0]

        for idx, c in enumerate(self.connections):
            if c.host == hostname:
                self.connections[idx].stop()
                self.connections.pop(idx)
                return True
        return False

    def getConnection(self, host):
        for c in self.connections:
            if host == c.host:
                return c
        return None

    def getDevices(self):
        pass

    def getFuncOrParam(self, host, device, param):
        for c in self.connections:
            if host == c.host:
                pass

    def setFuncOrParam(self, host, device, param):
        for c in self.connections:
            if host == c.host:
                pass

    def resize(self, host, newsize):
        for c in self.connections:
            if host == c.host:
                c.resizeLogger(newsize)

    def clearHost(self, host, signals='all'):
        for c in self.connections:
            if host == c.host:
                c.clear(signals=signals)
                print('cleared')

    def toggleDevice(self, host, device,state):
        for c in self.connections:
            if host == c.host:
                c.toggleDevice(device,state)

    def downloadSession(self, host):
        pass

    def activeConnections(self):
        return [c.host for c in self.connections]

    def pauseHost(self, host, value):
        for c in self.connections:
            if host == c.host:
                c.pause=value
