#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Internal OpenGL Renderer Functions.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

"""

import os
import projection
import mh
import log
import gui3d
from core import G
import gui
import image
from progress import Progress
import numpy as np

def Render(settings):
    progress = Progress.begin()
    
    if not mh.hasRenderToRenderbuffer():
        settings['dimensions'] = (G.windowWidth, G.windowHeight)

    if settings['lightmapSSS']:
        progress(0, 0.05, "Storing data")
        import image_operations as imgop
        import material
        human = G.app.selectedHuman
        materialBackup = material.Material(human.material)

        progress(0.05, 0.1, "Projecting lightmaps")
        diffuse = imgop.Image(data = human.material.diffuseTexture)
        lmap = projection.mapSceneLighting(settings['scene'], doFixSeams = False)
        # Do advanced seam fixing, to accomodate for blurring.
        seamfix = projection.SeamFix(lmap)
        lmapB = seamfix.apply()
        progress(0.1, 0.4, "Applying medium scattering")
        seamfix.expand(human.material.sssGScale - 1)
        lmapG = imgop.blurred(seamfix.apply(), human.material.sssGScale, 13)
        progress(0.4, 0.7, "Applying high scattering")
        seamfix.expand(human.material.sssRScale - human.material.sssGScale)
        lmapR = imgop.blurred(seamfix.apply(), human.material.sssRScale, 13)
        lmap = imgop.compose([lmapR, lmapG, lmapB])
        if not diffuse.isEmpty:
            progress(0.7, 0.8, "Combining textures")
            lmap = imgop.resized(lmap, diffuse.width, diffuse.height)
            progress(0.8, 0.9)
            lmap = imgop.multiply(lmap, diffuse)
        lmap.sourcePath = "Internal_Renderer_Lightmap_SSS_Texture"

        progress(0.9, 0.95, "Setting up renderer")
        human.material.diffuseTexture = lmap
        human.mesh.configureShading(diffuse = True)
        human.mesh.shadeless = True
        progress(0.95, 0.98, None)
    else:
        progress(0, 0.99, None)
        
    if not mh.hasRenderToRenderbuffer():
        # Limited fallback mode, read from screen buffer
        img = mh.grabScreen(0, 0, G.windowWidth, G.windowHeight)
        # TODO disable resolution GUI setting in fallback mode
    else:
        # Render to framebuffer object
        renderprog = Progress()
        renderprog(0, 0.99 - 0.59 * settings['AA'], "Rendering")
        width, height = settings['dimensions']
        if settings['AA']:
            width = width * 2
            height = height * 2
        img = mh.renderToBuffer(width, height)

        if settings['AA']:
            renderprog(0.4, 0.99, "AntiAliasing")
            # Resize to 50% using Qt image class
            qtImg = img.toQImage()
            del img
            # Bilinear filtered resize for anti-aliasing
            scaledImg = qtImg.scaled(width/2, height/2, transformMode = gui.QtCore.Qt.SmoothTransformation)
            del qtImg
            img = scaledImg
            #img = image.Image(scaledImg)    # Convert back to MH image
            #del scaledImg
        renderprog.finish()

    if settings['lightmapSSS']:
        progress(0.98, 0.99, "Restoring data")
        human.material = materialBackup

    # TODO restore scene object visibility

    progress(1, None, 'Rendering complete')

    gui3d.app.getCategory('Rendering').getTaskByName('Viewer').setImage(img)
    mh.changeTask('Rendering', 'Viewer')
    gui3d.app.statusPersist('Rendering complete.')
