#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers, Thomas Larsson, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui3d
import gui
from export import Exporter
from exportutils.config import Config

class MD5Config(Config):

    def __init__(self, exporter):
        Config.__init__(self)
        self.selectedOptions(exporter)
        self.useRelPaths = True
        self.useTexFolder = exporter.useTexFolder

    def selectedOptions(self, exporter):
        self.useTexFolder       = exporter.useTexFolder.selected
        self.useHelpers            = exporter.useHelpers.selected
        #self.scale,self.unit    = exporter.taskview.getScale()
        self.smooth = self.subdivide = gui3d.app.selectedHuman.isSubdivided()

        return self


class ExporterMD5(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "MD5"
        self.filter = "MD5 (*.md5)"
        self.fileExtension = "md5"

    def build(self, options, taskview):
        self.taskview       = taskview
        self.useTexFolder   = options.addWidget(gui.CheckBox("Separate texture folder", True))
        self.useHelpers        = options.addWidget(gui.CheckBox("Helper geometry", False))

    def export(self, human, filename):
        from . import mh2md5
        cfg = MD5Config(self)
        cfg.selectedOptions(self)
        mh2md5.exportMd5(human, filename("md5mesh"), cfg)

    def onShow(self, exportTaskView):
        exportTaskView.scaleBox.hide()

    def onHide(self, exportTaskView):
        exportTaskView.scaleBox.show()

def load(app):
    app.addExporter(ExporterMD5())

def unload(app):
    pass
