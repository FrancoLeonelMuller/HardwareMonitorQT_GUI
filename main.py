

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QFileDialog
from PyQt5 import QtSvg
import os
#os.system('pyuic5 -x /home/daff/PycharmProjects/pythonProject/Screen.ui -o '
#          '/home/daff/PycharmProjects/pythonProject/Screen.py')



from Screen import *
from ScriptAnalisis import *

fileGraph = 'Graph.svg'

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        self.w = None
        #self.fileDirectory = ""
        #self.fileList = ""
        #self.fileSelect = ""

        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        #self.label.setText("Haz clic en el botón")



        self.btn_SelectDirectory.clicked.connect(self.actualizar)
        self.btn_ShowGraph.clicked.connect(self.SVGRender)

        self.btn_Analisis.clicked.connect(self.analisis)


    def actualizar(self):
        #print(self.label.text())
        #self.listDataShow.clear()
        self.fileDirectory = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.fileList = ListaTotal(self.fileDirectory)
        self.listDataShow.addItems(self.fileList)
        self.lbl_statusAnalisis.setText("")

        #msgSelectRow = f"Selected items: {ListaTotal(file)[self.listDataShow.currentRow()]}"
        #print(msgSelectRow)
        #self.label.setText(msgSelectRow)

    def analisis(self):


        self.fileSelect = self.fileList[self.listDataShow.currentRow()]
        self.lbl_NombreArchivo.setText(f"OpenHardwareMonitorLog-{self.fileSelect}.csv")
        self.fileSelect = f"{self.fileDirectory}/OpenHardwareMonitorLog-{self.fileSelect}.csv"

        Analitic(self.fileSelect , self.spin_Date.value())
        self.lbl_statusAnalisis.setText("Completo")








    def SVGRender(self, checked):
        #self.listDataShow.clear()

        #if self.w is None:
        self.w = SVGWindow()
        self.w.show()


class SVGWindow(QWidget):

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.svg_widget = QtSvg.QSvgWidget(fileGraph)
        layout.addWidget(self.svg_widget)
        self.setLayout(layout)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
