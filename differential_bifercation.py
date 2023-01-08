import sys

from PyQt5.QtWidgets import *
import numpy as np
from numpy import sin, cos, tan, arctan, pi
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import pyqtgraph as pg
from functools import partial
# import pyqtgraph.opengl as gl

# plot by x vs t, x vs r,
"""y/x vs {y/t, x/t}
chart x vs t at r
xhart x vs r at eq--> find dif<e or just choose number
anumation of r increasing
rvs time to eq"""


class DispWin(pg.PlotWidget):
    def __init__(self):
        super().__init__()

        pg.setConfigOptions(antialias=True)
        self._create_plots()

    def _create_plots(self):
        self.waveform_plot =pg.ScatterPlotItem(pen='c', width=1)
        self.addItem(self.waveform_plot)

    def reset(self, x,y):
        self.waveform_plot.setData(x,y)

class PitchWin(DispWin):
    def __init__(self):
        super().__init__()

    def reset(self, x,y):
        self.waveform_plot.setData(x,y)

    def _create_plots(self):
        self.waveform_plot = self.plot(pen='c', width=3)


class Window(QMainWindow):
    # noinspection PyArgumentList
    def __init__(self):
        super().__init__()
        # self.setAcceptDrops(True)
        # self.file = r'N:\PC stuff\Programs\Python\Fourier\4th.jpg'

        self.setWindowTitle('Prop')

        self.start = QWidget()
        self.layout0 = QHBoxLayout()
        self.layout = QGridLayout()
        self.start.setLayout(self.layout0)
        self.layout1 = QGridLayout()
        self.layout0.addLayout(self.layout)
        self.layout0.addLayout(self.layout1)
        self.setCentralWidget(self.start)
        # todo on start
        # self.prop_eq = [prop ]
        # self.menu_items = {'R': 20, 'naca': '2414', 'r_hub': 8, 'points': 100, 'cord_max': 8, 'secs': 100, 'p_ang': 20}

        self.running = False

        self._create_controls()
        self._wins()
        self._docks()
        self.timer = QtCore.QTimer()

    def _wins(self):
        # [self.R, self.na, self.r_0, self.points, self.c_max, self.sec_cnt, self.pangle]


        self.cord = DispWin()  # todo rep with func to set
        self.section = PitchWin()
        # self.tools = Tab()
        self.widgets = [self.section, self.cord]

    def _docks(self):

        self.cord_dock = QDockWidget('x vs r at t')
        self.section_dock = QDockWidget('x vs t at r')

        # self.AllowTabbedDocks()

        self.cord_dock.setWidget(self.cord)

        self.section_dock.setWidget(self.section)

        self.addDockWidget(Qt.LeftDockWidgetArea, self.cord_dock)

        self.addDockWidget(Qt.RightDockWidgetArea, self.section_dock)

    # noinspection PyArgumentList
    def _create_controls(self):

        self.but = {}
        self.but_d = {}
        n = 0
        for i in ['r', 'x0']:
            li = QDoubleSpinBox()
            li.setSingleStep(0.1)

            lab = QLabel(i)
            cur = QSlider(Qt.Vertical)
            cur.setMinimum(0)
            cur.setMaximum(100)
            # cur.sliderReleased.connect(partial(self.update_cmd, i+'_slide'))

            self.layout.addWidget(lab, n, 0)
            self.layout.addWidget(li, n+1, 0)
            self.layout.addWidget(cur, n, 1,2,1)
            li.valueChanged.connect(partial(self.update_cmd, i))
            self.but[i] = li
            self.but[i+'_slide'] = cur
            n += 2

        self.layout.addWidget(cur, n, 0, 1, 2)

    def update_cmd(self, typ):
        print('update, ', typ)
        # val = self.but[typ].value()
        # if typ.endswith('slide'):
        #     typ = typ.remove('_slide')
        #     val *=0.01
        #
        # else:
        #     typ +='_slide'
        #     val *=100
        # self.but[typ].setValue(val)
        self.fx()

    def fx(self):
        r,x = self.x_vs_r()
        t,xt = self.x_vs_t()
        self.cord.reset(r,x)
        self.section.reset(t,xt)
        self.update()

    def x_vs_r(self):
        # teq
        r_ls = np.arange(0,4,0.01)
        # it

        xf = []
        it = 100
        for r in r_ls:
            x = self.but['x0'].value()
            for _ in range(it):
                x = r*(1-x)*x

            xf.append(x)

        return r_ls,xf


    def x_vs_t(self):
        r = self.but['r'].value()
        x = [self.but['x0'].value()]
        it = np.arange(0,100)

        for _ in it[1:]:
            x.append(r * (1 - x[-1]) * x[-1])
        return it, x
    # def animation(self):
    #     print('Animation starting')
    #     self.timer.setInterval(20)
    #     self.timer.timeout.connect(self.upd)
    #
    # def on_stop(self):
    #     print('stopped')
    #     if self.running:
    #         self.running = False
    #         self.timer.stop()
    #
    # def on_start(self):
    #     print('started')
    #     if not self.running:
    #         self.running = True
    #         # self.update_cmd()
    #         self.timer.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    audio_app = Window()
    audio_app.show()
    sys.exit(app.exec_())
