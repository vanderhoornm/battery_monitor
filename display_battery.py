#!/usr/bin/python

# Reads the battery status file and graphs the data points
# Copyright (C) 2013 Maurits van der Hoorn
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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
        size = self.size()
        px = size.width()/(self.max_time - self.min_time)
        py = size.height()/4800000.0
        for y in xrange(0, 4800000, 480000):
            qp.drawLine(0, y*py, size.width(), y*py)
        for x in xrange(int(self.max_time - self.min_time), 0, -3600):
            qp.drawLine(x*px, 0, x*px, self.height())
        last_y = 4800000
        for p in self.points:
            x = (p[0] - self.min_time) * px
            y = size.height() - p[1] * py
            if y-last_y >= 0:
                qp.setBrush(QtCore.Qt.red)
            else:
                qp.setBrush(QtCore.Qt.green)
            last_y = y
            qp.drawEllipse(x-5, y-5, 10, 10)
        qp.end()

app = QtGui.QApplication(sys.argv)
m = Main()
sys.exit(app.exec_())

