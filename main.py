from PyQt4 import QtCore, QtGui
import Interface
import sys
import platform
import cpuinfo
import wmi
import psutil
import os


class MainUiClass(QtGui.QMainWindow, Interface.Ui_MainWindow):
    def __init__(self, parent = None):
        super(MainUiClass, self).__init__(parent)
        self.setupUi(self)
        try:
            self.UiThread = UiThread()
            self.UiThread.start()
        except Exception as e:
            print(e)
        self.PCinfo()
        '''
        Conectores de sinais

        '''
        self.usoCpuBar.setValue(0)
        self.usoMemBar.setValue(0)
        self.memLivreBar.setValue(0)
        self.connect(self.UiThread, QtCore.SIGNAL("USO_CPU"), self.atualizaCpuBar)
        self.connect(self.UiThread, QtCore.SIGNAL("USO_MEM"), self.atualizaMemBar)
        self.connect(self.UiThread, QtCore.SIGNAL("FREE_MEM"), self.atualizaMemLivre)
        self.connect(self.UiThread, QtCore.SIGNAL("DISK_USE"), self.atualizaUsoDisco)



    def atualizaCpuBar(self, valor):
        self.usoCpuBar.setValue(float(valor))

    def atualizaMemBar(self, valor):
        self.usoMemBar.setValue(float(valor))

    def atualizaMemLivre(self, valor):
        self.memLivreBar.setValue(float(valor))

    def atualizaUsoDisco(self, valor):
        self.usoDiscoBar.setValue(valor)

    def PCinfo(self):
        self.nomeProcessador.setText(format(cpuinfo.get_cpu_info()['brand']))
        self.numCores.setText(str(os.cpu_count()))
        self.totalRam.setText(str(psutil.virtual_memory()[0] // 1000000000) + " GB")
        computer = wmi.WMI()
        gpu_info = computer.Win32_VideoController()[0]
        self.gpuNome.setText(str(gpu_info.name))
        self.so.setText(platform.platform())
        self.usoDiscoBar.setVisible(False)
        self.MEMORIALIVRELABEL_2.setVisible(False)


class UiThread(QtCore.QThread):
    def __init__(self, parent = None):
        super(UiThread, self).__init__(parent)

    def run(self):

        while True:
            usocpu = psutil.cpu_percent(interval=1)
            usoMem = float(psutil.virtual_memory().percent)
            memLivre = 100 - usoMem
            self.emit(QtCore.SIGNAL("USO_CPU"), str(usocpu))
            self.emit(QtCore.SIGNAL("USO_MEM"), str(usoMem))
            self.emit(QtCore.SIGNAL("FREE_MEM"), str(memLivre))
















if __name__ == '__main__':
    a = QtGui.QApplication(sys.argv)
    app = MainUiClass()
    app.show()
    app.setFixedSize(1142, 347)
    a.exec_()