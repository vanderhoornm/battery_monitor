#!/usr/bin/python

import os
import struct
import sys
from time import time
from PyQt4 import QtGui, QtCore

class Main(QtGui.QWidget):
    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Battery Monitor Plot");
        self.show()
        self.points = []
        self.min_time = time()
        self.max_time = 0
        with open(os.path.expanduser('~/.battery_monitor'), 'rb') as f:
            try:
                while True:
                    level = float(struct.unpack('i', f.read(4))[0])
                    ptime = float(struct.unpack('l', f.read(8))[0])
                    self.points.append([ptime, level])
                    if ptime < self.min_time:
                        self.min_time = ptime
                    if ptime > self.max_time:
                        self.max_time = ptime
            except:
                pass

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        pen = QtGui.QPen(QtCore.Qt.black, 1)
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.red)
        size = self.size()
        px = size.width()/(self.max_time - self.min_time)
        py = size.height()/4800000.0
        for y in xrange(0, 4800000, 480000):
            qp.drawLine(0, y*py, size.width(), y*py)
        for x in xrange(int(self.max_time - self.min_time), 0, -3600):
            qp.drawLine(x*px, 0, x*px, self.height())
        for p in self.points:
            x = (p[0] - self.min_time) * px
            y = size.height() - p[1] * py
            qp.drawEllipse(x-5, y-5, 10, 10)
        qp.end()

app = QtGui.QApplication(sys.argv)
m = Main()
sys.exit(app.exec_())

