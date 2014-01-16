#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

Internal OpenGL Renderer Plugin.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thanasis Papoutsidakis

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

from . import mh2opengl

import os
from core import G
import gui
from guirender import RenderTaskView
import mh

class OpenGLTaskView(RenderTaskView):

    def __init__(self, category):
        RenderTaskView.__init__(self, category, 'Render')

        # Don't change shader for this RenderTaskView.
        self.taskViewShader = G.app.selectedHuman.material.shader

        settingsBox = self.addLeftWidget(gui.GroupBox('Settings'))
        settingsBox.addWidget(gui.TextView("Resolution"))
        self.resBox = settingsBox.addWidget(gui.TextEdit(
            "x".join([str(self.renderingWidth), str(self.renderingHeight)])))
        self.AAbox = settingsBox.addWidget(gui.CheckBox("Anti-aliasing"))
        self.AAbox.setSelected( G.app.settings.get('GL_RENDERER_AA', True) )
        self.lightmapSSS = settingsBox.addWidget(gui.CheckBox("Lightmap SSS"))
        self.lightmapSSS.setSelected( G.app.settings.get('GL_RENDERER_SSS', False) )
        self.renderButton = settingsBox.addWidget(gui.Button('Render'))

        if not mh.hasRenderToRenderbuffer():
            # Can only use screen grabbing as fallback, resolution option disabled
            self.resBox.setEnabled(False)

        @self.resBox.mhEvent
        def onChange(value):
            try:
                value = value.replace(" ", "")
                res = [int(x) for x in value.split("x")]
                self.renderingWidth = res[0]
                self.renderingHeight = res[1]
            except: # The user hasn't typed the value correctly yet.
                pass

        @self.AAbox.mhEvent
        def onClicked(value):
            G.app.settings['GL_RENDERER_AA'] = self.AAbox.selected

        @self.lightmapSSS.mhEvent
        def onClicked(value):
            G.app.settings['GL_RENDERER_SSS'] = self.lightmapSSS.selected

        @self.renderButton.mhEvent
        def onClicked(event):
            settings = dict()
            settings['scene'] = self.getScene()
            settings['AA'] = self.AAbox.selected
            settings['dimensions'] = (self.renderingWidth, self.renderingHeight)
            settings['lightmapSSS'] = self.lightmapSSS.selected
            
            reload(mh2opengl)
            mh2opengl.Render(settings)

    def onShow(self, event):
        RenderTaskView.onShow(self, event)
        self.renderButton.setFocus()

    def onHide(self, event):
        RenderTaskView.onHide(self, event)


def load(app):
    category = app.getCategory('Rendering')
    taskview = OpenGLTaskView(category)
    taskview.sortOrder = 1.3
    category.addTask(taskview)

def unload(app):
    pass

