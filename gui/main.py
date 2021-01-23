from PyQt5 import QtGui
import pyqtgraph as pg


class Application(object):
    def __init__(self):
        self.app = QtGui.QApplication([])
        # window setup
        self.window = QtGui.QWidget()
        self.window.resize(1000, 800)
        self.window.setWindowTitle('Morphologies 3D')
        self.layout = QtGui.QGridLayout()
        self.window.setLayout(self.layout)
        
        # buttons setup
        self.button_erosion = QtGui.QPushButton('Erosion')
        self.button_dilation = QtGui.QPushButton('Dilation')

        self.plot = pg.PlotWidget()

        # add widgets to layout
        self.layout.addWidget(self.button_erosion, 0, 0)
        self.layout.addWidget(self.button_dilation, 1, 0)
        self.layout.addWidget(self.plot, 0, 2, 3, 4)

    def show(self):
        self.window.show()

    def close(self):
        self.app.exec_()


app = Application()
app.show()
app.close()
