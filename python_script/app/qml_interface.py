from PyQt5.QtGui import QGuiApplication
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtQml import QQmlListProperty, QQmlApplicationEngine
from sys import argv
from total_main import *

from walk_dir import get_list_project_with_value
import os
# dict_initial_data= {'project': '1','station': '1', 'report':'1' }
ini = open_ini_file.inst()
class Qmlinterface():
    def __init__(self):
        self.project ={}
        self.project_out ={}
        # ini.BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path_to_qml = os.path.join(ini.BASE_DIR, 'qml', 'Main.qml')
        self.list_pr=[]
        self.list_st=[]
        self.list_rp=[]
        self.dict_st={}
        self.set_project=''


    def list_station_for_inreface(self):
        for pr in self.project.keys():
            project.channels = Pars_project([pr])
            list_st = self.project.get(pr)
            for st in list_st.keys():
                station.channels = Pars_project([st])
                for rp in list_st.get(st):
                    report.channels = Pars_project([rp])

    def update_project_out(self,name_checked_item):
        self.project = get_list_project_with_value()
        self.dict_st = self.project.get(name_checked_item)

    def prints(self,name_checked_component, name_checked_item):
        if name_checked_component=='project':
            project.prj_or_st = []
            station.prj_or_st = []
            self.set_project=name_checked_item
            self.dict_st=self.project.get(name_checked_item)
            self.list_st = sorted(list(self.dict_st.keys()))
            self.project_out.clear()

            for pr in self.project.keys():
                self.project_out.update({pr : self.list_st})
            if not self.list_pr:
                self.list_pr = self.project_out.keys()
                for pr in self.list_pr:
                    project.channels = Pars_project(pr)

            for pr in self.list_st:
                station.channels = Pars_project(pr)

            self.prints('station', self.list_st[0])

        if name_checked_component == 'station':
            self.list_rp=self.dict_st.get(name_checked_item)
            report.prj_or_st = []
            if self.list_rp:
                for rp in self.list_rp:
                    report.channels = Pars_project(rp)
            else: report.channels = Pars_project(None)



class Pars_project(QObject):
    name_prj_or_st = pyqtSignal()

    def __init__(self, name, *args, **kwargs):
        # print('Channel')
        super().__init__(*args, **kwargs)

        self._name = name

    @pyqtProperty('QString', notify=name_prj_or_st)
    def name(self):
        return self._name

class Pars_station(QObject):
    Pars_project_Changed = pyqtSignal()

    def  __init__(self, *args, **kwargs):
        # print('Store')
        super().__init__(*args, **kwargs)
        self.prj_or_st = []


    @pyqtSlot(str, str, name="sum")
    def sum(self, index, checked):
        qmli.prints(index, checked)

    @pyqtSlot(str, str, name="openfile")
    def openfile(self, index, checked):
        print(index,checked)
        if index=='station':

            ini.set_path_and_station(qmli.set_project, checked)
            total_main()
            qmli.update_project_out(qmli.set_project)
            qmli.prints(index, checked)


    @pyqtProperty(QQmlListProperty, notify=Pars_project_Changed)
    def channels(self):
        return QQmlListProperty(Pars_project, self, self.prj_or_st)

    @channels.setter
    def channels(self, value):
        if value: self.prj_or_st.append(value)
        self.Pars_project_Changed.emit()
app = QGuiApplication(argv)
project = Pars_station()
station = Pars_station()
report = Pars_station()
qmli = Qmlinterface()
def qml():

    view = QQmlApplicationEngine()
    view.rootContext().setContextProperty('store', project)
    view.rootContext().setContextProperty('station', station)
    view.rootContext().setContextProperty('report', report)
    view.load(qmli.path_to_qml)
    qmli.project=get_list_project_with_value()
    if qmli.project:
        list_pr = list(qmli.project.keys())[0]
        qmli.prints('project', list_pr)

    app.exec_()



