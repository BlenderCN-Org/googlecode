#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Material library plugin.

"""

__docformat__ = 'restructuredtext'

import material 
import os
import gui3d
import mh
import download
import gui
import filechooser as fc
import log

class MaterialAction(gui3d.Action):
    def __init__(self, obj, after):
        super(MaterialAction, self).__init__("Change material of %s" % obj.mesh.name)
        self.obj = obj
        self.before = material.Material().copyFrom(obj.material)
        self.after = after

    def do(self):
        self.obj.material = self.after
        return True

    def undo(self):
        self.obj.material = self.before
        return True


class TextureTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Material', label='Skin/Material')
        self.skinBlender = EthnicSkinBlender(gui3d.app.selectedHuman)

        self.systemSkins = mh.getSysDataPath('skins')
        self.systemClothes = os.path.join(mh.getSysDataPath('clothes'), 'textures')
        self.systemHair = mh.getSysDataPath('hairstyles')
        self.systemEyes = mh.getSysDataPath('eyes')

        self.userSkins = os.path.join(mh.getPath(''), 'data', 'skins')
        self.userClothes = os.path.join(mh.getPath(''), 'data', 'clothes', 'textures')
        self.userHair = os.path.join(mh.getPath(''), 'data', 'hairstyles')
        self.userEyes = os.path.join(mh.getPath(''), 'data', 'eyes')

        for path in (self.userSkins, self.userClothes, self.userEyes):
            if not os.path.exists(path):
                os.makedirs(path)

        self.defaultClothes = [self.systemClothes, self.userClothes]
        self.defaultHair = [self.systemHair, self.userHair]
        self.defaultEyes = [self.systemEyes, self.userEyes]

        self.textures = self.defaultClothes
        self.activeClothing = None
        self.hairTexture = None
        self.eyeTexture = None

        self.filechooser = self.addRightWidget(fc.IconListFileChooser(self.userSkins, 'mhmat', ['thumb', 'png'], mh.getSysDataPath('skins/notfound.thumb'), 'Material'))
        self.filechooser.setIconSize(50,50)
        self.filechooser.enableAutoRefresh(False)
        self.addLeftWidget(self.filechooser.createSortBox())

        self.update = self.filechooser.sortBox.addWidget(gui.Button('Check for updates'))
        self.mediaSync = None
        self.mediaSync2 = None

        @self.filechooser.mhEvent
        def onFileSelected(filename):
            mat = material.fromFile(filename)
            human = gui3d.app.selectedHuman
            if self.skinRadio.selected:
                gui3d.app.do(MaterialAction(human,
                    mat))
            elif self.hairRadio.selected:
                gui3d.app.do(MaterialAction(human.hairObj,
                    mat))
            elif self.eyesRadio.selected:
                gui3d.app.do(MaterialAction(human.eyesObj,
                    mat))
            else: # Clothes
                if self.activeClothing:
                    uuid = self.activeClothing
                    gui3d.app.do(MaterialAction(human.clothesObjs[uuid],
                        mat))

        @self.update.mhEvent
        def onClicked(event):
            self.syncMedia()

        self.objectSelector = []
        self.humanBox = self.addLeftWidget(gui.GroupBox('Human'))
        self.skinRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Skin", selected=True))
        self.hairRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Hair", selected=False))
        self.eyesRadio = self.humanBox.addWidget(gui.RadioButton(self.objectSelector, "Eyes", selected=False))

        @self.skinRadio.mhEvent
        def onClicked(event):
            if self.skinRadio.selected:
                self.reloadTextureChooser()

        @self.hairRadio.mhEvent
        def onClicked(event):
            if self.hairRadio.selected:
                self.reloadTextureChooser()

        @self.eyesRadio.mhEvent
        def onClicked(event):
            if self.eyesRadio.selected:
                self.reloadTextureChooser()

        self.clothesBox = self.addLeftWidget(gui.GroupBox('Clothes'))
        self.clothesSelections = []


    def onShow(self, event):

        # When the task gets shown, set the focus to the file chooser
        gui3d.TaskView.onShow(self, event)
        human = gui3d.app.selectedHuman

        self.skinRadio.setChecked(True)
        self.reloadTextureChooser()

        if human.hairObj:
            self.hairRadio.setEnabled(True)
        else:
            self.hairRadio.setEnabled(False)

        if human.eyesObj:
            self.eyesRadio.setEnabled(True)
        else:
            self.eyesRadio.setEnabled(False)

        self.populateClothesSelector()

        # Offer to download skins if none are found
        self.numSkin = len([filename for filename in os.listdir(os.path.join(mh.getPath(''), 'data', 'skins')) if filename.lower().endswith('png')])
        if self.numSkin < 1:
            gui3d.app.prompt('No skins found', 'You don\'t seem to have any skins, download them from the makehuman media repository?\nNote: this can take some time depending on your connection speed.', 'Yes', 'No', self.syncMedia)


    def populateClothesSelector(self):
        """
        Builds a list of all available clothes.
        """
        human = gui3d.app.selectedHuman
        # Only keep first 3 radio btns (human body parts)
        for radioBtn in self.objectSelector[3:]:
            radioBtn.hide()
            radioBtn.destroy()
        del self.objectSelector[3:]

        self.clothesSelections = []
        theClothesList = human.clothesObjs.keys()
        self.activeClothing = None
        for i, uuid in enumerate(theClothesList):
            if i == 0:
                self.activeClothing = uuid
            radioBtn = self.clothesBox.addWidget(gui.RadioButton(self.objectSelector, human.clothesProxies[uuid].name, selected=False))
            self.clothesSelections.append( (radioBtn, uuid) )

            @radioBtn.mhEvent
            def onClicked(event):
                for radio, uuid in self.clothesSelections:
                    if radio.selected:
                        self.activeClothing = uuid
                        log.debug( 'Selected clothing "%s" (%s)' % (radio.text(), uuid) )
                        self.reloadTextureChooser()
                        return

    def applyClothesTexture(self, uuid, filename):
        human = gui3d.app.selectedHuman
        if uuid not in human.clothesObjs.keys():
            log.warning("Cannot set texture for clothes with UUID %s, no such item", uuid)
            return False
        clo = human.clothesObjs[uuid]
        clo.mesh.setTexture(filename)
        return True

    def getClothesTexture(self, uuid):
        """
        Get the currently set texture for clothing item with specified UUID.
        """
        human = gui3d.app.selectedHuman
        if uuid not in human.clothesObjs.keys():
            return None
        clo = human.clothesObjs[uuid]
        return clo.getTexture()

    def reloadTextureChooser(self):
        human = gui3d.app.selectedHuman
        selectedMat = None

        if self.skinRadio.selected:
            self.textures = [self.systemSkins, self.userSkins, mh.getSysDataPath('textures')]
            selectedMat = human.material.filename
        elif self.hairRadio.selected:
            proxy = human.hairProxy
            if proxy:
                self.textures = [os.path.dirname(proxy.file)] + self.defaultHair
            else:
                self.textures = self.defaultHair
            selectedMat = human.hairObj.material.filename
        elif self.eyesRadio.selected:
            proxy = human.eyesProxy
            if proxy:
                self.textures = [os.path.dirname(proxy.file)] + self.defaultEyes
            else:
                self.textures = self.defaultEyes
            selectedMat = human.eyesObj.material.filename
        else: # Clothes
            if self.activeClothing:
                uuid = self.activeClothing
                clo = human.clothesObjs[uuid]
                filepath = human.clothesProxies[uuid].file
                self.textures = [os.path.dirname(filepath)] + self.defaultClothes
                selectedMat = clo.material.filename
            else:
                # TODO maybe dont show anything?
                self.textures = self.defaultClothes

                filec = self.filechooser
                log.debug("fc %s %s %s added", filec, filec.children.count(), str(filec.files))

        # Reload filechooser
        self.filechooser.deselectAll()
        self.filechooser.setPaths(self.textures)
        self.filechooser.refresh()
        if selectedMat:
            self.filechooser.setHighlightedItem(selectedMat)
        self.filechooser.setFocus()
        if self.eyesRadio.selected:
            print self.filechooser.children.getItems()[1].file
            print self.filechooser.children.getItems()[2].file

    def onHide(self, event):
        gui3d.TaskView.onHide(self, event)

    def onHumanChanging(self, event):
        self.skinBlender.onSkinUpdateEvent(event)

    def onHumanChanged(self, event):
        self.skinBlender.onSkinUpdateEvent(event)

    def loadHandler(self, human, values):

        if values[0] == 'skinTexture':
            (fname, ext) = os.path.splitext(values[1])
            if fname != "texture":
                path = os.path.join(os.path.join(mh.getPath(''), 'data', 'skins', values[1]))
                if os.path.isfile(path):
                    human.setTexture(path)
                elif ext == ".tif":
                    path = path.replace(".tif", ".png")
                    human.setTexture(path)
        elif values[0] == 'textures':
            uuid = values[1]
            filepath = values[2]

            if human.hairProxy and human.hairProxy.getUuid() == uuid:
                if not os.path.dirname(filepath):
                    proxy = human.hairProxy
                    hairPath = os.path.dirname(proxy.file)
                    filepath = os.path.join(hairPath, filepath)
                human.hairObj.mesh.setTexture(filepath)
                return
            elif human.eyesProxy and human.eyesProxy.getUuid() == uuid:
                if not os.path.dirname(filepath):
                    proxy = human.eyesProxy
                    eyesPath = os.path.dirname(proxy.file)
                    filepath = os.path.join(eyesPath, filepath)
                human.eyesObj.mesh.setTexture(filepath)
                return
            elif not uuid in human.clothesProxies.keys():
                log.error("Could not load texture for object with uuid %s!" % uuid)
                return
            proxy = human.clothesProxies[uuid]
            if not os.path.dirname(filepath):
                proxy = human.clothesProxies[uuid]
                clothesPath = os.path.dirname(proxy.file)
                filepath = os.path.join(clothesPath, filepath)
            self.applyClothesTexture(uuid, filepath)
            return

    def saveHandler(self, human, file):

        file.write('skinTexture %s\n' % os.path.basename(human.getTexture()))
        for name, clo in human.clothesObjs.items():
            if clo:
                proxy = human.clothesProxies[name]
                if clo.mesh.texture !=  proxy.material.diffuseTexture:
                    clothesPath = os.path.dirname(proxy.file)
                    if os.path.dirname(clo.mesh.texture) == clothesPath:
                        texturePath = os.path.basename(clo.mesh.texture)
                    else:
                        texturePath = clo.mesh.texture
                    file.write('textures %s %s\n' % (proxy.getUuid(), texturePath))
        if human.hairObj and human.hairProxy:
            file.write('textures %s %s\n' % (human.hairProxy.getUuid(), human.hairObj.mesh.texture))
        if human.eyesObj and human.eyesProxy:
            file.write('textures %s %s\n' % (human.eyesProxy.getUuid(), human.eyesObj.mesh.texture))
        #if self.eyeTexture:
        #    file.write('eyeTexture %s\n' % self.eyeTexture)

    def syncMedia(self):

        if self.mediaSync:
            return
        if not os.path.isdir(self.userSkins):
            os.makedirs(self.userSkins)
        self.mediaSync = download.MediaSync(gui3d.app, self.userSkins, 'http://download.tuxfamily.org/makehuman/skins/', self.syncMediaFinished)
        self.mediaSync.start()
        self.mediaSync2 = None

    def syncMediaFinished(self):
        '''
        if not self.mediaSync2:
            if not os.path.isdir(self.userClothes):
                os.makedirs(self.userClothes)
            self.mediaSync2 = download.MediaSync(gui3d.app, self.userClothes, 'http://download.tuxfamily.org/makehuman/clothes/textures/', self.syncMediaFinished)
            self.mediaSync2.start()
            self.mediaSync = None
        else:
            self.mediaSync = None
            self.filechooser.refresh()
        '''

        self.mediaSync = None
        self.filechooser.refresh()

import image
import image_operations
class EthnicSkinBlender(object):
    # TODO move this someplace else (in Human maybe?) In the future we probably want a more generic mechanism for blending textures

    def __init__(self, human):
        self.human = human
        self.skinCache = { 'caucasian' : image.Image(mh.getSysDataPath('litspheres/skinmat_caucasian.png')),
                           'african'   : image.Image(mh.getSysDataPath('litspheres/skinmat_african.png')),
                           'asian'    : image.Image(mh.getSysDataPath('litspheres/skinmat_asian.png')) }

    def onSkinUpdateEvent(self, event):
        if "litsphereTexture" not in self.human.meshData.shaderParameters:
            return

        current = self.human.meshData.shaderParameters["litsphereTexture"]
        if current and (isinstance(current, image.Image) or \
           os.path.abspath(current) == os.path.abspath(mh.getSysDataPath("litspheres/adaptive_skin_tone.png"))):
            if event.change == "caucasian" or event.change == "african" or \
              event.change == "asian" or event.change == "material":
                self.updateAdaptiveSkin()

    def updateAdaptiveSkin(self):
        img = self.getEthnicityBlendMaterial()
        # Set parameter so the image can be referenced when material is written to file
        img.sourcePath = mh.getSysDataPath("litspheres/adaptive_skin_tone.png")
        self.human.setShaderParameter("litsphereTexture", img)

    def getEthnicityBlendMaterial(self):
        caucasianWeight = self.human.getCaucasian()
        africanWeight   = self.human.getAfrican()
        asianWeight     = self.human.getAsian()
        blends = []

        if caucasianWeight > 0:
            blends.append( ('caucasian', caucasianWeight) )
        if africanWeight > 0:
            blends.append( ('african', africanWeight) )
        if asianWeight > 0:
            blends.append( ('asian', asianWeight) )

        if len(blends) == 1:
            return self.skinCache[blends[0][0]]
        else:
            img = image_operations.mix(self.skinCache[blends[0][0]], self.skinCache[blends[1][0]], blends[0][1], blends[1][1])
            if len(blends) > 2:
                img = image_operations.mix(img, self.skinCache[blends[2][0]], 1.0, blends[2][1])
            return img



# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Materials')
    taskview = TextureTaskView(category)
    taskview.sortOrder = 0
    category.addTask(taskview)

    app.addLoadHandler('textures', taskview.loadHandler)
    app.addLoadHandler('skinTexture', taskview.loadHandler)
    app.addLoadHandler('eyeTexture', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)


# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
