#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import gui3d
import mh
import files3d
import mh2proxy
import filechooser as fc
import log

class EyesAction(gui3d.Action):
    def __init__(self, name, human, library, before, after):
        super(EyesAction, self).__init__(name)
        self.human = human
        self.library = library
        self.before = before
        self.after = after

    def do(self):
        self.library.setEyes(self.human, self.after)
        return True

    def undo(self):
        self.library.setEyes(self.human, self.before)
        return True


class EyesTaskView(gui3d.TaskView):

    def __init__(self, category):

        gui3d.TaskView.__init__(self, category, 'Eyes')
        eyesDir = os.path.join(mh.getPath(''), 'data', 'eyes')
        if not os.path.exists(eyesDir):
            os.makedirs(eyesDir)
        self.paths = [eyesDir , mh.getSysDataPath('eyes')]
        #self.filechooser = self.addTopWidget(fc.FileChooser(self.paths, 'mhclo', 'thumb', mh.getSysDataPath('eyes/notfound.thumb')))
        self.filechooser = self.addRightWidget(fc.IconListFileChooser(self.paths, 'mhclo', 'thumb', mh.getSysDataPath('clothes/notfound.thumb'), 'Eyes'))
        self.filechooser.setIconSize(50,50)
        self.filechooser.enableAutoRefresh(False)
        self.addLeftWidget(self.filechooser.createSortBox())

        self.oHeadCentroid = [0.0, 7.436, 0.03 + 0.577]
        self.oHeadBBox = [[-0.84,6.409,-0.9862],[0.84,8.463,1.046]]

        self.human = gui3d.app.selectedHuman

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            if self.human.eyesProxy:
                oldFile = self.human.eyesProxy.file
            else:
                oldFile = 'clear.mhclo'
            gui3d.app.do(EyesAction("Change eyes",
                self.human,
                self,
                oldFile,
                filename))

    def setEyes(self, human, mhclo):
        self.filechooser.selectItem(mhclo)

        if human.eyesObj:
            gui3d.app.removeObject(human.eyesObj)
            human.eyesObj = None
            human.eyesProxy = None

        if os.path.basename(mhclo) == "clear.mhclo":
            return

        human.eyesProxy = mh2proxy.readProxyFile(human.meshData, mhclo, type="Eyes", layer=3)
        if not human.eyesProxy:
            log.error("Failed to load %s", mhclo)
            return

        obj = human.eyesProxy.obj_file
        #obj = os.path.join(obj[0], obj[1])
        mesh = files3d.loadMesh(obj)
        if not mesh:
            log.error("Failed to load %s", obj)
            return

        mesh.material = human.eyesProxy.material

        human.eyesObj = gui3d.app.addObject(gui3d.Object(human.getPosition(), mesh))
        human.eyesObj.setRotation(human.getRotation())
        human.eyesObj.mesh.setCameraProjection(0)
        human.eyesObj.mesh.setSolid(human.mesh.solid)
        if human.eyesProxy.cull:
            human.eyesObj.mesh.setCull(1)
        else:
            human.eyesObj.mesh.setCull(None)
        # Enabling this causes render-que order issues so that eyes render over hair
        # Disabling it renders hi-poly eyes wrong
        if human.eyesProxy.transparent:
            human.eyesObj.mesh.setTransparentPrimitives(len(human.eyesObj.mesh.fvert))
        else:
            human.eyesObj.mesh.setTransparentPrimitives(0)
        human.eyesObj.mesh.priority = 5

        #eyesName = human.eyesObj.mesh.name.split('.')[0]

        self.adaptEyesToHuman(human)
        human.eyesObj.setSubdivided(human.isSubdivided())

    def adaptEyesToHuman(self, human):

        if human.eyesObj and human.eyesProxy:

            mesh = human.eyesObj.getSeedMesh()
            human.eyesProxy.update(mesh)
            mesh.update()
            if human.eyesObj.isSubdivided():
                human.eyesObj.getSubdivisionMesh()

    def onShow(self, event):
        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        self.filechooser.refresh()
        if self.human.eyesProxy and self.human.eyesProxy.file:
            self.filechooser.setHighlightedItem(self.human.eyesProxy.file)
        self.filechooser.setFocus()
        if gui3d.app.settings.get('cameraAutoZoom', True):
            gui3d.app.setFaceCamera()

    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)

    def onHumanChanging(self, event):

        human = event.human
        if event.change == 'reset':
            log.message("resetting eyes")
            if human.eyesObj:
                gui3d.app.removeObject(human.eyesObj)
                human.eyesObj = None
                human.eyesProxy = None
            self.setEyes(human, mh.getSysDataPath("eyes/high-poly/high-poly.mhclo"))
            self.filechooser.deselectAll()
        else:
            if gui3d.app.settings.get('realtimeUpdates', False):
                self.adaptEyesToHuman(human)

    def onHumanChanged(self, event):

        human = event.human
        self.adaptEyesToHuman(human)

    def loadHandler(self, human, values):

        mhclo = values[1]
        if not os.path.exists(os.path.realpath(mhclo)):
            log.notice('EyesTaskView.loadHandler: %s does not exist. Skipping.', mhclo)
            return
        self.setEyes(human, mhclo)

    def saveHandler(self, human, file):

        if human.eyesProxy:
            file.write('eyes %s\n' % human.eyesProxy.file)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Geometries')
    taskview = EyesTaskView(category)
    taskview.sortOrder = 1
    category.addTask(taskview)

    app.addLoadHandler('eyes', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

    # Load initial eyes
    taskview.setEyes(gui3d.app.selectedHuman, mh.getSysDataPath("eyes/low-poly/low-poly.mhclo"))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass

