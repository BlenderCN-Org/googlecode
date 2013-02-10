#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import gui
from export import Exporter, Config


class FbxConfig(Config):

    def __init__(self, rigtype, exporter):
        Config.__init__(self, exporter)
        self.rigtype         = rigtype,
        self.expressions     = exporter.expressions.selected
        self.useCustomShapes = exporter.useCustomShapes.selected
        
        
    def __repr__(self):
        return("<FbxOptions %s s %s e %s h %s>" % (
            self.rigtype, self.separateFolder, self.expressions, self.helpers))


class ExporterFBX(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Filmbox (fbx)"
        self.filter = "Filmbox (*.fbx)"

    def build(self, options):
        Exporter.build(self, options)
        self.expressions     = options.addWidget(gui.CheckBox("Expressions", False))
        self.useCustomShapes = options.addWidget(gui.CheckBox("Custom shapes", False))
        self.rigtypes        = self.addRigs(options)

    def export(self, human, filename):
        import mh2fbx

        for (button, rigtype) in self.rigtypes:
            if button.selected:
                break
        mh2fbx.exportFbx(human, filename("fbx"), FbxConfig(rigtype, self))

def load(app):
    app.addExporter(ExporterFBX())

def unload(app):
    pass
