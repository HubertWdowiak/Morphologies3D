import numpy as np
import matplotlib.pyplot as plt
from PyQt5 import QtGui
from PyQt5.QtWidgets import QInputDialog, QLineEdit, QFileDialog, QSlider, QComboBox
from PyQt5.QtCore import Qt, QSize
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import pyqtgraph as pg
from model.image3d import Image3d


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
        self.binarization_label = QtGui.QLabel("Binarization method", self.window)
        self.button_binarize = QtGui.QPushButton('Binarize')
        self.binarization_combo = QtGui.QComboBox(self.window)
        self.button_apply = QtGui.QPushButton('Apply')

        self.files_layout = QtGui.QVBoxLayout()
        self.files_label = QtGui.QLabel("Open/Save files", self.window)
        self.files_label.adjustSize()
        self.button_save = QtGui.QPushButton('Save')
        self.button_load = QtGui.QPushButton('Load')

        self.slider = QSlider(Qt.Horizontal)

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.ax_top_1d = None
        self.ax_top_2d = None
        self.ax_top_3d = None
        self.ax_bottom_1d = None
        self.ax_bottom_2d = None
        self.ax_bottom_3d = None

        self.image3d = Image3d()

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
        self.buttons_layout.addWidget(self.binarization_label)
        self.buttons_layout.addWidget(self.binarization_combo)
        self.buttons_layout.addWidget(self.button_binarize)

        self.binarization_combo.addItem("otsu")
        self.binarization_combo.addItem("li")
        self.binarization_combo.addItem("mean")
        self.binarization_combo.addItem("yen")
        self.buttons_layout.addWidget(self.button_apply)

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

        self.reset_figure()
        # main layout
        self.layout.addLayout(self.buttons_layout, 0, 0)
        self.layout.addLayout(self.files_layout, 1, 0)
        self.layout.addWidget(self.canvas, 0, 1, 5, 6)
        self.layout.addWidget(self.slider, 5, 1, 1, 6, Qt.AlignTop)

        self.connect_widgets()

    def connect_widgets(self):
        self.button_save.clicked.connect(self.save_file_dialog)
        self.button_load.clicked.connect(self.load_file_dialog)

        self.button_apply.clicked.connect(self.image3d.apply)
        self.button_apply.clicked.connect(self.update_image)

        self.button_binarize.clicked.connect(lambda: self.image3d.binarize('otsu'))
        self.button_binarize.clicked.connect(self.update_image)



        self.slider.valueChanged.connect(self.update_image)

    def load_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self.window, "Load image from disk", "",
                                                   "Pickle files(*.npy);;CSV (*.csv)", options=options)
        if file_name:
            with open(file_name, 'rb') as file:
                self.image3d.load_data(np.load(file))
                self.slider.setMaximum(self.image3d.images.shape[0] - 1)
                self.update_image()

    def save_file_dialog(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self.window, "Save image on disk", "",
                                                   "Pickle files(.npy*);;CSV (*.csv)", options=options)
        if file_name:
            with open(file_name, 'wb') as file:
                np.save(file, self.image3d.images)

    def show(self):
        self.window.show()

    def close(self):
        self.app.exec_()

    def update_image(self):
        self.reset_figure()
        index = self.slider.value()
        if self.image3d.images.any():
            self.ax_top_1d.imshow(self.image3d.images[index, :, :])
            self.ax_top_2d.imshow(self.image3d.images[:, index, :])
            self.ax_top_3d.imshow(self.image3d.images[:, :, index])
            if self.image3d.images_modified is not None:
                self.ax_bottom_1d.imshow(self.image3d.images_modified[index, :, :])
                self.ax_bottom_2d.imshow(self.image3d.images_modified[:, index, :])
                self.ax_bottom_3d.imshow(self.image3d.images_modified[:, :, index])

        self.canvas.draw()

    def reset_figure(self):
        self.figure.clear()
        self.ax_top_1d = self.figure.add_subplot(2, 3, 1)
        self.ax_top_2d = self.figure.add_subplot(2, 3, 2)
        self.ax_top_3d = self.figure.add_subplot(2, 3, 3)
        self.ax_bottom_1d = self.figure.add_subplot(2, 3, 4)
        self.ax_bottom_2d = self.figure.add_subplot(2, 3, 5)
        self.ax_bottom_3d = self.figure.add_subplot(2, 3, 6)

        self.ax_top_1d.axis("off")
        self.ax_top_1d.set_title("Plane(x, y) before apply")
        self.ax_top_2d.axis("off")
        self.ax_top_2d.set_title("Plane(z, y) before apply")
        self.ax_top_3d.axis("off")
        self.ax_top_3d.set_title("Plane(z, x) before apply")

        self.ax_bottom_1d.axis("off")
        self.ax_bottom_1d.set_title("Plane(x, y) after apply")
        self.ax_bottom_2d.axis("off")
        self.ax_bottom_2d.set_title("Plane(z, y) after apply")
        self.ax_bottom_3d.axis("off")
        self.ax_bottom_3d.set_title("Plane(z, x) after apply")


app = Application()
app.show()
app.close()
