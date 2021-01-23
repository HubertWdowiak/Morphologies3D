from PyQt5 import QtGui
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QSlider
from PyQt5.QtCore import Qt, QSize
import pyqtgraph as pg


class Application(object):
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.window = QtGui.QWidget()
        self.layout = QtGui.QGridLayout()

        # operations
        self.buttons_layout = QtGui.QVBoxLayout()
        self.operations_label = QtGui.QLabel("Morph operations", self.window)
        self.button_erosion = QtGui.QPushButton('Erosion')
        self.button_dilation = QtGui.QPushButton('Dilation')
        self.button_opening = QtGui.QPushButton('Opening')
        self.button_closing = QtGui.QPushButton('Closing')

        self.files_layout = QtGui.QVBoxLayout()
        self.files_label = QtGui.QLabel("Open/Save files", self.window)
        self.files_label.adjustSize()
        self.button_save = QtGui.QPushButton('Save')
        self.button_load = QtGui.QPushButton('Load')

        self.slider = QSlider(Qt.Horizontal)

        self.graph = pg.PlotWidget()
        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        self.graph.plot(hour, temperature)

        self.init()


    def init(self):
        # window setup
        self.window.resize(1000, 800)
        self.window.setWindowTitle('Morphologies 3D')
        self.window.setLayout(self.layout)

        # operations layout
        self.operations_label.setAlignment(Qt.AlignBottom)
        self.operations_label.adjustSize()
        self.buttons_layout.addWidget(self.operations_label)
        self.buttons_layout.addWidget(self.button_erosion)
        self.buttons_layout.addWidget(self.button_dilation)
        self.buttons_layout.addWidget(self.button_opening)
        self.buttons_layout.addWidget(self.button_closing)

        self.files_layout.addWidget(self.files_label)
        self.files_label.setAlignment(Qt.AlignBottom)
        self.files_layout.addWidget(self.button_save)
        self.files_layout.addWidget(self.button_load)

        self.slider.setFocusPolicy(Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.setTickInterval(1)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(1)
        self.slider.setMaximum(60)


        # main layout
        self.layout.addLayout(self.buttons_layout, 0, 0)
        self.layout.addLayout(self.files_layout, 1, 0)
        self.layout.addWidget(self.graph, 0, 1, 5, 6)
        self.layout.addWidget(self.slider, 5, 1, 1, 6, Qt.AlignTop)

        self.connect_buttons()


    def connect_buttons(self):
        self.button_save.clicked.connect(self.save_file_dialog)
        self.button_load.clicked.connect(self.load_file_dialog)


    def load_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.window, "Load image from disk", "",
                                                  "Pickle files(.pickle*);;CSV (*.csv)", options=options)
        if file_name:
            print(file_name)


    def save_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.window, "Save image on disk", "",
                                                  "Pickle files(.pickle*);;CSV (*.csv)", options=options)
        if file_name:
            print(file_name)

    def show(self):
        self.window.show()

    def close(self):
        self.app.exec_()


app = Application()
app.show()
app.close()
