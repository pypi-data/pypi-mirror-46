#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ExportMarkerCountToXLS.py

# Copyright (c) 2015-2016, Richard Gerum, Sebastian Richter
#
# This file is part of ClickPoints.
#
# ClickPoints is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ClickPoints is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ClickPoints. If not, see <http://www.gnu.org/licenses/>

from __future__ import division, print_function
import clickpoints
from clickpoints.includes.QtShortCuts import AddQComboBox, AddQSaveFileChoose
from qtpy import QtCore, QtGui, QtWidgets
import numpy as np
from clickpoints.includes.matplotlibwidget import MatplotlibWidget

class Addon(clickpoints.Addon):
    def __init__(self, *args, **kwargs):
        clickpoints.Addon.__init__(self, *args, **kwargs)
        # set the title and layout
        self.setWindowTitle("Test - ClickPoints")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.last_list = None

    def imageLoadedEvent(self, filename, framenumber):
        return
        # only proceed if the frame is valid
        if framenumber is None:
            return#

        print("Items:", len(self.cp.window.view.items()))
        return

    def run(self, i):
        print("run")
        import threading
        print("->", isinstance(threading.current_thread(), threading._MainThread))
        self.cp.jumpToFrameWait(np.random.randint(10))

    def buttonPressedEvent(self):
        print("Button press", self.cp.getCurrentFrame())
        self.cp.jumpToFrameWait(np.random.randint(10))
        print("Button press", self.cp.getCurrentFrame())

