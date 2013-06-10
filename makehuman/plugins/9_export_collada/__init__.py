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
from export import Exporter
from exportutils.config import Config


class DaeConfig(Config):
    def __init__(self, exporter):
        from armature.options import ArmatureOptions

        Config.__init__(self)
        self.selectedOptions(exporter)

        self.useRelPaths = True
        self.useNormals = exporter.useNormals.selected
        self.rotate90X = exporter.rotate90X.selected
        self.rotate90Z = exporter.rotate90Z.selected
        self.feetOnGround = False
        self.expressions     = exporter.expressions.selected
        self.useCustomTargets = exporter.useCustomTargets.selected

        self.rigOptions = exporter.getRigOptions()
        if not self.rigOptions:
            self.rigOptions = ArmatureOptions()
        self.rigOptions.setExportOptions(
            useExpressions = self.expressions,
            feetOnGround = self.feetOnGround,
        )



class ExporterCollada(Exporter):
    def __init__(self):
        Exporter.__init__(self)
        self.name = "Collada (dae)"
        self.filter = "Collada (*.dae)"


    def build(self, options, taskview):
        Exporter.build(self, options, taskview)
        self.useNormals = options.addWidget(gui.CheckBox("Normals", False))
        self.rotate90X = options.addWidget(gui.CheckBox("Z up (Rotate 90 X)", False))
        self.rotate90Z = options.addWidget(gui.CheckBox("Face X (Rotate 90 Z)", False))
        self.expressions     = options.addWidget(gui.CheckBox("Expressions", False))
        self.useCustomTargets = options.addWidget(gui.CheckBox("Custom targets", False))


    def export(self, human, filename):
        from .mh2collada import exportCollada

        exportCollada(human, filename("dae"), DaeConfig(self))


def load(app):
    app.addExporter(ExporterCollada())

def unload(app):
    pass
