
from PyQt5.QtWidgets import *


import sys

from functools import partial

from PyQt5.QtCore import Qt
# from PyQt5.QtWidgits import *
import numpy as np
import pyqtgraph as pg



class AvePlot(pg.GraphicsLayoutWidget):
    def __init__(self):
        super().__init__()
        #self.win = QDockWidget('Roll', side)

        # self.side =
        self.seed_d = {'seed': 1, 'n': 2, 'delta': 5,'length': 10}
        self._init_p()

    def _init_p(self):
        self.plot = self.addPlot(0,0)
        # self.mean_line = self.plot.plot()  # todo ave bar '--[]--'
        self.plot.addLegend()
        self.plot.setLabels(**{'title': 'Teperature vs entropy'})
        self.mean_line = self.plot.plot(pen='c', width=3)
        self.data = self.plot.plot(pen='r', width=3)
        self.ave_data = self.plot.plot(pen='g', width=3)  # todo add legend with numper, seed, delta

    def first_data(self):
        dtt = [0, self.seed_d['length']]
        # print(x_000)
        ave,ni,li = self.roll_ave()
        # print(y_000)

        self.data.setData(li, self.p_0)
        self.ave_data.setData(ni, ave)

        mean_x = np.mean(self.p_0)
        self.mean_line.setData(dtt, [mean_x, mean_x])

    def _init_roll_func(self):  # todo static
        self.p_0 = [self.seed_d['seed']]
        for i in range(self.seed_d['length']):
            seed_2 = self.p_0[-1] + (np.random.rand() - 0.5) * self.seed_d['delta']  # todo gaus
            self.p_0.append(seed_2)
        # return p_0

    def roll_ave(self):
        pp = []
        ni = self.seed_d['n'] // 2
        li = len(self.p_0)

        xi = np.arange(ni,  li- ni)
        for p in xi:
            pi = np.mean(self.p_0[p - ni:p + ni])
            pp.append(pi)

        print(f'len p_0;{len(self.p_0)} pp:{pp}, xi:{xi.size}, li{li}')  # todo numpy size, return sise of class
        return pp,xi,np.arange(0,li)

    def plot_fun(self):  # todo change sseed otr other
        self.plot.setData()

    def data_x(self, box,val):
        self.seed_d[box] = val
        self._init_roll_func()
        self.first_data()



class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot = AvePlot()
        self._set_tools()

    def _set_tools(self):
        self.cen = QWidget()
        self.setCentralWidget(self.cen)
        self.plot_wig = QDockWidget( 'Plot')
        self.plot_wig.setWidget(self.plot)
        self.addDockWidget(Qt.RightDockWidgetArea,self.plot_wig)
        self.slide_lay = QGridLayout()
        self.box_lay = QGridLayout()
        self.lay = QHBoxLayout()

        self.lay.addLayout(self.slide_lay)
        self.lay.addLayout(self.box_lay)
        self.cen.setLayout(self.lay)

        slide = ['delta', 'n', 'seed', 'length']
        self.slide = {}
        self.box = {}
        ni = 0  # todo throw tooltip

        for n in slide:
            i = QSlider()
            j = QLabel(n)
            box = QLineEdit()
            self.slide[n] = i
            self.box[n] = box
            self.slide_lay.addWidget(j,ni,0)
            self.box_lay.addWidget(j, ni, 0)
            self.slide_lay.addWidget(i, ni, 1)
            self.box_lay.addWidget(box, ni, 1)
            i.valueChanged.connect(partial(self.con2, n))
            box.editingFinished.connect(partial(self.con, n))
            i.setValue(self.plot.seed_d[n])
            ni += 1

    def con(self, i):
        # assum box
        box = self.box[i]
        try:
            ij = int(box.text())
        except ValueError:
            print('i must be number int')
            return
        self.slide[i].setValue(ij)

    def con2(self, i):
        v = self.slide[i].value()
        self.box[i].setText(str(v))
        self.plot.data_x(i,v)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())
