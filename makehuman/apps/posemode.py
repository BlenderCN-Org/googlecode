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

import os
import gui3d
from armature.pose import createPoseRig
from armature.utils import debugCoords
import humanmodifier
import warpmodifier
import algos3d
import log


class Storage:
    def __init__(self):
        self.coord = None
        self.targetBuffer = None
        self.filepath = None
        self.dirty = False


    def store(self, human):
        debugCoords("store")
        if self.coord is not None:
            raise NameError("Failed to set unposed coords")
        obj = human.meshData
        self.coord = obj.coord.copy()
        #warpmodifier.clearRefObject()
        human.warpsNeedReset = False
        if self.filepath and not self.dirty:
            return self.filepath

        self.dirty = False
        self.filepath = None
        self.targetBuffer = {}
        for trgpath, target in algos3d.targetBuffer.items():
            self.targetBuffer[trgpath] = target
        return None


    def restore(self, human, filepath):
        if self.coord is not None:
            obj = human.meshData
            obj.changeCoords(self.coord)
            obj.calcNormals()
            obj.update()
            self.coord = None
            debugCoords("restore1")
        #warpmodifier.removeAllWarpTargets(human)
        if self.targetBuffer is not None:
            algos3d.targetBuffer = self.targetBuffer
            self.targetBuffer = None
        self.filepath = filepath
        self.dirty = False
        debugCoords("restore2")


def compromiseStorage():
    _storage.dirty = True
    _storage.filepath = None
    log.debug("Storage compromised")

_storage = Storage()
_inPoseMode = False


def printVert(human):
    return
    for vn in [8202]:
        x = human.meshData.coord[vn]
        if human.unposedCoords is None:
            y = (0,0,0)
        else:
            y = human.unposedCoords[vn]
        log.debug("  %d: (%.3f %.3f %.3f) (%.3f %.3f %.3f)", vn,x[0],x[1],x[2],y[0],y[1],y[2])


def enterPoseMode():
    global _inPoseMode, _storage
    if _inPoseMode:
        return
    log.message("Enter pose mode")
    _inPoseMode = True
    filepath = _storage.store(gui3d.app.selectedHuman)
    log.message("Pose mode entered: %s" % filepath)
    return filepath


def exitPoseMode(filepath=None):
    global _inPoseMode, _storage
    if not _inPoseMode:
        return
    log.message("Exit pose mode: %s" % filepath)
    _storage.restore(gui3d.app.selectedHuman, filepath)
    _inPoseMode = False
    log.message("Pose mode exited")


def resetPoseMode():
    global _inPoseMode, _storage
    exitPoseMode()
    log.message("Reset pose mode")
    _storage.__init__()
    enterPoseMode()


def changePoseMode(event):
    human = event.human
    #log.debug("Change pose mode %s w=%s e=%s", _inPoseMode, human.warpsNeedReset, event.change)
    if human and human.warpsNeedReset:
        exitPoseMode()
    elif event.change not in ["targets", "warp"]:
        exitPoseMode()
    if event.change == "reset":
        resetPoseMode()


def loadMhpFile(filepath, pose=None):

    human = gui3d.app.selectedHuman
    folder = os.path.dirname(filepath)
    hasTargets = False
    for file in os.listdir(folder):
        if os.path.splitext(file)[1] == ".target":
            hasTargets = True
            break

    if hasTargets:
        (fname, ext) = os.path.splitext(os.path.basename(filepath))
        filenamePattern = "${gender}-${age}-${tone}-${weight}-%s.target" % fname
        modpath = os.path.join(folder, filenamePattern)
        log.debug('PoseLoadTaskView.loadMhpFile: %s %s', filepath, modpath)
        modifier = PoseModifier(modpath)
        modifier.updateValue(human, 1.0)
    else:
        modifier = None

    if not pose:
        pose = createPoseRig(human)
    pose.setModifier(modifier)
    pose.readMhpFile(filepath)

    return pose

#----------------------------------------------------------
#   class PoseModifierSlider
#----------------------------------------------------------

class PoseModifierSlider(humanmodifier.ModifierSlider):
    def __init__(self, label, modifier):
        humanmodifier.ModifierSlider.__init__(self, label=label, modifier=modifier, warpResetNeeded=False)

    def onChanging(self, value):
        enterPoseMode()
        humanmodifier.ModifierSlider.onChanging(self, value)

    def onChange(self, value):
        enterPoseMode()
        humanmodifier.ModifierSlider.onChange(self, value)

