# -*- coding: utf-8 -*-
import os
import pickle
#from PyQt5 import QtCore
#from PyQt5.QtWidgets import (QMainWindow, QApplication)

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
#from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (QWidget, QAction, QDockWidget,
                              QMenu, QHBoxLayout, QVBoxLayout, QCheckBox,
                              QLabel, QMenuBar, QToolBar, QComboBox,
                              QLineEdit, QStackedWidget, QGroupBox,
                             QGridLayout, QSpacerItem, QSizePolicy,
                             QGraphicsScene, QGraphicsView,
                             QGraphicsPixmapItem, QGraphicsItemGroup,
                             QGraphicsRectItem, QFrame
                             )
from PyQt5.QtWidgets import (QMainWindow, QApplication)

import fractalshades.gui as fsgui
import typing
#
from model import Model, Func_submodel, Image_presenter
from guimodel import Func_widget, Image_widget
#
def getapp():
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QApplication([])
    return app


def test_image_widget():
    pass
# 'Software': 'fractalshades 0.1.0', 'fractal_type': 'Perturbation_mandelbrot', 'datetime': '2021-05-19_21:37:53',
    rep = "/home/geoffroy/Pictures/math/github_fractal_rep/Fractal-shades/examples/perturb"
    im = "dev.png"
    model = Model({"model_folder": rep,
                   "model_image": im,
                   "model_xy_ratio": 1.0,
                   "model_x": '-1.74928893611435556407228',
                   "model_y": '0.',
                   "model_dx": '5.e-20'})
    mapping = {"folder": ("model_folder",),
               "image": ("model_image",),
               "xy_ratio": ("model_xy_ratio",),
               "x": ("model_x",),
               "y": ("model_y",),
               "dx": ("model_dx",)}
    presenter = Image_presenter(model, mapping)
    
    class Mywindow(QMainWindow):
        def __init__(self, im):
            super().__init__(parent=None)
            self.setWindowTitle('Testing Image of Fractalshades')
            #self.setWindowState(Qt.WindowMaximized)
    
            # And don't forget to call setCentralWidget to your main layout widget.
            mw =  Image_widget(self, presenter) # fsgui.
            self.setCentralWidget(mw)

    app = getapp()
    win = Mywindow(im)
    win.show()
    app.exec()
#
#def test_QDict_viewer_widget():
#    from collections import OrderedDict
#    #from widgets import QDict_viewer
##    class Mywindow(QMainWindow):
##    # https://doc.qt.io/qt-5/qmainwindow.html
##        def __init__(self, odict):
##            super().__init__(parent=None)
##            self.setWindowTitle('Testing Image of Fractalshades')
##            mw =  QDict_viewer(self, odict)
##            self.setCentralWidget(mw)
#    app = getapp()
#    odict = OrderedDict([("a", 1.), ("b", 2.), ("c", 3.)])
#    win = QDict_viewer(None, odict)
#    win.show()
#    win.values_update({"b": "voilou"})
#    app.exec()
    

def test_():
    pass



def test_im_info():
    # what do we have in fractal.param ?
    rep = "/home/geoffroy/Pictures/math/github_fractal_rep/Fractal-shades/examples/perturb"
    param_file = os.path.join(rep, "data/dev.params")
    with open(param_file, 'rb') as tmpfile:
        params = pickle.load(tmpfile)
        print("params", params)
    
    from PIL import Image
    image_file = os.path.join(rep, "dev.png")
    with Image.open(image_file) as im:
        # im.load()
        info = im.info #()
    print("info", info)


def test_func_widget():
    
    def f_atomic(x: int=1, yyyy: float=10., y: str="aa", z:float=1.0):
        pass 

    def f_union(x: int=1, yyyy: float=10., y: str="aa", z: typing.Union[int, float, str]="abc"):
        pass 

    def f_optional(x: int=1, yyyy: float=10., y: str="aa", z: typing.Union[int, float, str]="abc",
                option: typing.Optional[float]=12.354, option2: typing.Optional[float]=None):
        pass 
    
    def f_listed(x: int=1, yyyy: float=10., y: str="aa", z: typing.Union[int, float, str]="abc",
                option: typing.Optional[float]=12.354, option2: typing.Optional[float]=None,
                listed: typing.Literal["a", "b", "c", 1, None]="c"):
        pass
        
    def f_listed2(x: int, yyyy: float, y: str, z: typing.Union[int, float, str],
                option: typing.Optional[float]=12.354, option2: typing.Optional[float]=None,
                listed: typing.Literal["a", "b", "c", 1, None]="c"):
        pass 
    
    func = f_listed2
    model = Model()
    func_smodel = Func_submodel(model, tuple(["func"]), func)
    
    
    class Mywindow(QMainWindow):
        def __init__(self):
            super().__init__(parent=None)

            self.setWindowTitle('Testing inspector')
            tb = QToolBar(self)
            self.addToolBar(tb)
#            print_dict = QAction("print dict")
            tb.addAction("print_dict")
            
            # tb.actionTriggered[QAction].connect(self.on_tb_action)
            tb.actionTriggered.connect(self.on_tb_action)
            #self.setWindowState(Qt.WindowMaximized)
            # And don't forget to call setCentralWidget to your main layout widget.
             # fsgui.

            wget = Func_widget(self, func_smodel)
            self._wget = wget
            
#            im = os.path.join("/home/geoffroy/Pictures/math/github_fractal_rep/Fractal-shades/tests/images_REF",
#                      "test_M2_antialias_E0_2.png")
#            mw =  Image_widget(self, im)
            
#            main_frame = QFrame(self)
#            main_frame.setFixedSize(800, 800)
            
            dock_widget = QDockWidget(None, Qt.SubWindow)
            dock_widget.setWidget(wget)
            dock_widget.setWindowTitle(func.__name__)
            dock_widget.setStyleSheet("QDockWidget {color: white; font: bold 14px; border: 3px solid  #4583b6;}"
                                      "QDockWidget::title {text-align: left; background: #4583b6; padding-left: 5px;}");
            
            # self.setCentralWidget(mw)
            
            self.addDockWidget(Qt.RightDockWidgetArea, dock_widget)
            self._wget = wget
            # self.setFixedSize(800, 800)

        def on_tb_action(self, qa):
            print("qa", qa)
            d = self._wget._submodel._dict
            for k, v in d.items():
                print(k, " --> ", v)


    app = getapp()
    win = Mywindow()
    win.show()
    app.exec()
    

if __name__ == "__main__":
    # test_func_widget()
    test_im_info()
    test_image_widget()
