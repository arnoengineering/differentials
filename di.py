
from PyQt5.QtWidgets import *


import sys

from functools import partial

from PyQt5.QtCore import Qt

import numpy as np
import pyqtgraph as pg


class Arrow:
    def __init__(self,st,end):
        self.base = st
        self.head = end
        self.len = self.head - self.base

    def print(self,paint):


# class vect(pg.ArrowItem):
#     def __init__(self, start,end):  # TODO class overload
#         super().__init__()
#         self.setPos()
#
#     def paint(self, p, *args):


class AvePlot(pg.widgets.MatplotlibWidget.MatplotlibWidget):
    def __init__(self, side=Qt.LeftDockWidgetArea):
        super().__init__()
        self.win = QDockWidget('Roll', side)
        # self.side =
        self.x0 = 5
        self.y0= 20
        self.init_p()

    def _init_plot(self):
        # fig, ax = plt.subplots()

        plt.xlim(0, 20)
        plt.ylim(10, 40)
        plt.ylabel('Prey')
        plt.xlabel('Pred')
        plt.title('Pred, Prey')
        plt.grid()
        plt.show()
        pass

    def run_plot(self):
        plt.quiver(pred, prey, d_pred, d_prey, color='g')

        xi, yi = ddd(pred_0, prey_0)
        plt.plot(xi, yi)

    def _init_var(self):
        self.pred_0 = 5
        self.prey_0 = 20

        self.pred_d = 0.8
        self.pred_b = -1.1
        self.prey_d = -1.2
        self.prey_b = 1.618

        self.d_prey_f = self.df(self.prey_d, self.prey_b)
        self.d_pred_f = self.df(self.pred_b, self.pred_d)

        pred, prey = np.meshgrid(np.linspace(0, 20, 25),
                                 np.linspace(10, 40, 25))
        d_pred = self.d_pred_f(pred, prey)
        d_prey = self.d_prey_f(prey, pred)

    def df(self, b, d):
        def dft(x, y):
            return x * (b * y + d)

        return dft

    def ddd(self, t=10, dt=1):
        time = np.arange(0, t, dt)
        xiii = [self.pred_0]
        yiii = [self.prey_0]
        for _ in time:
            x_1 = self.d_pred_f(self.pred_0, self.prey_0)
            y_1 = self.d_prey_f(self.prey_0, self.pred_0)
            x_0 += x_1
            y_0 += y_1
            xiii.append(x_0)
            yiii.append(y_0)
        return xiii, yiii


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot = AvePlot()

        pass



if __name__ == '__main__':

    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())