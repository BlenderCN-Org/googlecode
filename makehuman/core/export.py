#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import gui
import log

class Config:

    def __init__(self, exporter=None):
        if exporter:
            self.separateFolder     = exporter.separateFolder.selected
            self.eyebrows           = exporter.eyebrows.selected
            self.lashes             = exporter.lashes.selected
            self.helpers            = exporter.helpers.selected
            self.hidden             = exporter.hidden.selected
            self.scale,self.unit    = exporter.getScale(exporter.scales)
            self.subdivide          = exporter.smooth.selected
        else:
            self.separateFolder     = False
            self.eyebrows           = True
            self.lashes             = True
            self.helpers            = False
            self.hidden             = True
            self.scale,self.unit    = 1.0, "decimeter"
            self.subdivide          = False

        self.exporting          = True
        self.feetOnGround       = False
        self.skirtRig		= None
        self.rigtype            = None
        self.cage               = False
        self.texFolder          = None
        self.proxyList          = []


class Exporter(object):
    def __init__(self):
        self.group = "mesh"

    def build(self, options):
        self.separateFolder = options.addWidget(gui.CheckBox("Separate folder", False))
        self.eyebrows       = options.addWidget(gui.CheckBox("Eyebrows", True))
        self.lashes         = options.addWidget(gui.CheckBox("Eyelashes", True))
        self.helpers        = options.addWidget(gui.CheckBox("Helper geometry", False))
        self.hidden         = options.addWidget(gui.CheckBox("Keep hidden faces", True))
        self.smooth         = options.addWidget(gui.CheckBox("Subdivide", False))
        self.scales         = self.addScales(options)

    def export(self, human, filename):
        raise NotImplementedError()

    _scales = {
        "decimeter": 1.0,
        "meter": 0.1,
        "inch": 1.0/0.254,
        "centimeter": 10.0
        }

    def addScales(self, options):
        check = True
        buttons = []
        scales = []
        for name in ["decimeter", "meter", "inch", "centimeter"]:
            button = options.addWidget(gui.RadioButton(scales, name, check))
            check = False
            buttons.append((button,name))
        return buttons

    def getScale(self, buttons):
        for (button, name) in buttons:
            if button.selected and name in self._scales:
                return (self._scales[name], name)
        return (1, "decimeter")
        
    def addRigs(self, options, rigs = None):
        path = "data/rigs"
        if not os.path.exists(path):
            log.message("Did not find directory %s", path)
            return []

        check = rigs is None
        buttons = []
        rigs = rigs if rigs is not None else []
        for fname in os.listdir(path):
            (name, ext) = os.path.splitext(fname)
            if ext == ".rig":
                button = options.addWidget(gui.RadioButton(rigs, "Use %s rig" % name, check))
                check = False
                buttons.append((button, name))
        return buttons
