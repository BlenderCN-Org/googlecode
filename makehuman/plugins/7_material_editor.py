#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import os
import gui3d
import gui
import log
import shader
import numpy as np
import material
import mh
from humanobjchooser import HumanObjectSelector

class MaterialEditorTaskView(gui3d.TaskView):
    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Material Editor')

        self.human = gui3d.app.selectedHuman

        self.humanObjSelector = self.addLeftWidget(HumanObjectSelector(self.human))
        @self.humanObjSelector.mhEvent
        def onActivate(value):
            self.reloadMaterial()

        shaderBox = self.addLeftWidget(gui.GroupBox('Shader'))
        self.shaderList = shaderBox.addWidget(gui.ListView())
        self.shaderList.setSizePolicy(gui.SizePolicy.Ignored, gui.SizePolicy.Preferred)

        self.shaderConfBox = self.addLeftWidget(gui.GroupBox('Shader config'))
        shaderConfig = self.human.material.shaderConfig
        for name in shaderConfig:
            chkBox = gui.CheckBox(name, shaderConfig[name])
            self.shaderConfBox.addWidget(chkBox)
            @chkBox.mhEvent
            def onClicked(event):
                shaderConfig = dict()
                for child in self.shaderConfBox.children:
                    shaderConfig[str(child.text())] = child.isChecked()
                self.getSelectedObject().material.configureShading(**shaderConfig)

        self.paramBox = self.addRightWidget(gui.GroupBox('Shader parameters'))

        self.materialBox = self.addRightWidget(gui.GroupBox('Material settings'))

        if not shader.Shader.supported():
            log.notice('Shaders not supported')
            self.shaderList.setEnabled(False)
            self.shaderList.hide()
            self.paramBox.hide()

        @self.shaderList.mhEvent
        def onClicked(item):
            self.setShader(unicode(item.getUserData()))

        self.loadSaveBox = self.addRightWidget(gui.GroupBox("Material file"))
        self.loadMaterialBtn = self.loadSaveBox.addWidget(gui.BrowseButton(), 0, 0)
        self.loadMaterialBtn.setFilter("MakeHuman Material (*.mhmat)")
        self.loadMaterialBtn.setText('Load')
        @self.loadMaterialBtn.mhEvent
        def onClicked(path):
            if path:
                self.loadMaterial(path)
        self.saveMaterialBtn = self.loadSaveBox.addWidget(gui.BrowseButton('save'), 0, 1)
        self.saveMaterialBtn.setFilter("MakeHuman Material (*.mhmat)")
        self.saveMaterialBtn.setText('Save')

        @self.saveMaterialBtn.mhEvent
        def onClicked(path):
            if path:
                if not os.path.splitext(path)[1]:
                    path = path + ".mhmat"
                self.saveMaterial(path)

    def loadMaterial(self, path):
        self.getSelectedObject().material = material.fromFile(path)
        self.reloadMaterial()

    def saveMaterial(self, path):
        self.getSelectedObject().material.toFile(path)

    def listMaterialSettings(self, obj):
        for child in self.materialBox.children[:]:
            self.materialBox.removeWidget(child)

        mat = obj.material

        w1 = self.materialBox.addWidget(ColorValue("Diffuse", mat.diffuseColor))
        @w1.mhEvent
        def onActivate(event):
            mat.diffuseColor = w1.value

        w3 = self.materialBox.addWidget(ImageValue("Diffuse texture", mat.diffuseTexture, mh.getSysDataPath('textures')))
        @w3.mhEvent
        def onActivate(event):
            mat.diffuseTexture = w3.value
            self.updateShaderConfig()

        w4 = self.materialBox.addWidget(ColorValue("Ambient", mat.ambientColor))
        @w4.mhEvent
        def onActivate(event):
            mat.ambientColor = w4.value

        w5 = self.materialBox.addWidget(ColorValue("Specular", mat.specularColor))
        @w5.mhEvent
        def onActivate(event):
            mat.specularColor = w5.value

        w7 = self.materialBox.addWidget(ScalarValue("Specular shininess", mat.shininess))
        @w7.mhEvent
        def onActivate(event):
            mat.shininess = w7.value

        w8 = self.materialBox.addWidget(ColorValue("Emissive", mat.emissiveColor))
        @w8.mhEvent
        def onActivate(event):
            mat.emissiveColor = w8.value

        w9 = self.materialBox.addWidget(ScalarValue("Opacity", mat.opacity))
        @w9.mhEvent
        def onActivate(event):
            mat.opacity = w9.value

        w10 = self.materialBox.addWidget(ScalarValue("Translucency", mat.translucency))
        @w10.mhEvent
        def onActivate(event):
            mat.translucency = w10.value

        w10a = self.materialBox.addWidget(TruthValue("Shadeless", mat.shadeless))
        @w10a.mhEvent
        def onActivate(event):
            mat.shadeless = w10a.value

        w10b = self.materialBox.addWidget(TruthValue("Wireframe", mat.wireframe))
        @w10b.mhEvent
        def onActivate(event):
            mat.wireframe = w10b.value

        w10c = self.materialBox.addWidget(TruthValue("Transparent", mat.transparent))
        @w10c.mhEvent
        def onActivate(event):
            mat.transparent = w10c.value

        w10d = self.materialBox.addWidget(TruthValue("Backface culling", mat.backfaceCull))
        @w10d.mhEvent
        def onActivate(event):
            mat.backfaceCull = w10d.value

        w10e = self.materialBox.addWidget(TruthValue("Depthless", mat.depthless))
        @w10e.mhEvent
        def onActivate(event):
            mat.depthless = w10e.value

        w10f = self.materialBox.addWidget(TruthValue("Auto ethnic skin", mat.autoBlendSkin))
        @w10f.mhEvent
        def onActivate(event):
            mat.autoBlendSkin = w10f.value

        w11 = self.materialBox.addWidget(ImageValue("Transparency map texture", mat.transparencyMapTexture, mh.getSysDataPath('textures')))
        @w11.mhEvent
        def onActivate(event):
            mat.transparencyMapTexture = w11.value
            self.updateShaderConfig()

        w12 = self.materialBox.addWidget(ScalarValue("Transparency (map) intensity", mat.transparencyMapIntensity))
        @w12.mhEvent
        def onActivate(event):
            mat.transparencyMapIntensity = w12.value

        w13 = self.materialBox.addWidget(ImageValue("Bump map texture", mat.bumpMapTexture, mh.getSysDataPath('textures')))
        @w13.mhEvent
        def onActivate(event):
            mat.bumpMapTexture = w13.value
            self.updateShaderConfig()

        w14 = self.materialBox.addWidget(ScalarValue("Bump map intensity", mat.bumpMapIntensity))
        @w14.mhEvent
        def onActivate(event):
            mat.bumpMapIntensity = w14.value

        w15 = self.materialBox.addWidget(ImageValue("Normal map texture", mat.normalMapTexture, mh.getSysDataPath('textures')))
        @w15.mhEvent
        def onActivate(event):
            mat.normalMapTexture = w15.value
            self.updateShaderConfig()

        w16 = self.materialBox.addWidget(ScalarValue("Normal map intensity", mat.normalMapIntensity))
        @w16.mhEvent
        def onActivate(event):
            mat.normalMapIntensity = w16.value

        w17 = self.materialBox.addWidget(ImageValue("Displacement map texture", mat.displacementMapTexture, mh.getSysDataPath('textures')))
        @w17.mhEvent
        def onActivate(event):
            mat.displacementMapTexture = w17.value
            self.updateShaderConfig()

        w18 = self.materialBox.addWidget(ScalarValue("Displacement map intensity", mat.displacementMapIntensity))
        @w18.mhEvent
        def onActivate(event):
            mat.displacementMapIntensity = w18.value

        w19 = self.materialBox.addWidget(ImageValue("Specular map texture", mat.specularMapTexture, mh.getSysDataPath('textures')))
        @w19.mhEvent
        def onActivate(event):
            mat.specularMapTexture = w19.value
            self.updateShaderConfig()

        w20 = self.materialBox.addWidget(ScalarValue("Specular map intensity", mat.specularMapIntensity))
        @w20.mhEvent
        def onActivate(event):
            mat.specularMapIntensity = w20.value

        w21 = self.materialBox.addWidget(FileValue("UV map", mat.uvMap, mh.getSysDataPath('uvs')))
        w21.browseBtn.setFilter("UV Set (*.obj)")
        @w21.mhEvent
        def onActivate(event):
            if os.path.basename(w21.value) == "default.obj":
                w21.value = None
                obj.setUVMap(None)
            else:
                obj.setUVMap(w21.value)

        w22 = self.materialBox.addWidget(TextValue("Material name", mat.name))
        @w22.mhEvent
        def onActivate(event):
            mat.name = w22.value


    def listShaders(self, mat, dir = mh.getSysDataPath('shaders/glsl')):
        shaders = set()
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if not os.path.isfile(path):
                continue
            postfix = '_shader.txt'
            if not name.endswith(postfix):
                continue
            name, type = name[:-len(postfix)].rsplit('_',1)
            if type not in ['vertex', 'geometry', 'fragment']:
                continue
            shaders.add(name)

        self.shaderList.clear()
        firstItem = self.shaderList.addItem('[None]', data = '')
        if mat.shader:
            shaderName = os.path.basename(mat.shader)
        else:
            shaderName = None

        selectedShader = None
        for name in sorted(shaders):
            item = self.shaderList.addItem(name, data = os.path.join(dir, name))
            if shaderName and unicode(shaderName) == unicode(item.text):
                selectedShader = item
                path = unicode(item.getUserData())

        if mat.shader and not selectedShader:
            # Custom shader selected (not in shader path): add it
            item = self.shaderList.addItem(shaderName, data = mat.shader)
            item.setChecked(True)
        elif selectedShader:
            selectedShader.setChecked(True)
        else:
            firstItem.setChecked(True)

    def updateShaderConfig(self, mat = None):
        if not mat:
            mat = self.getSelectedObject().material

        shaderConfig = mat.shaderConfig

        for child in self.shaderConfBox.children:
            name = str(child.text())
            child.setChecked( shaderConfig[name] )
            if name == 'diffuse':
                child.setEnabled(mat.supportsDiffuse())
            if name == 'bump':
                # TODO disable bump if normal enabled
                child.setEnabled(mat.supportsBump())
            if name == 'normal':
                child.setEnabled(mat.supportsNormal())
            if name == 'displacement':
                child.setEnabled(mat.supportsDisplacement())
            if name == 'spec':
                child.setEnabled(mat.supportsSpecular())

    def setShader(self, path, mat = None):
        if not mat:
            mat = self.getSelectedObject().material
        mat.setShader(path)
        self.listUniforms(mat)

    def listUniforms(self, mat):
        for child in self.paramBox.children[:]:
            self.paramBox.removeWidget(child)

        path = mat.shader

        if not path:
            return

        try:
            sh = mat.shaderObj
        except:
            sh = None
        if not sh:
            return
        uniforms = sh.getUniforms()
        for index, uniform in enumerate(uniforms):
            if uniform.name in material._materialShaderParams:
                continue
            self.paramBox.addWidget(UniformValue(uniform, mat), index)

    def getSelectedObject(self):
        selected = self.humanObjSelector.selected
        if selected == 'skin':
            return self.human
        if selected == 'hair':
            return self.human.hairObj
        if selected == 'eyes':
            return self.human.eyesObj
        if selected == 'genitals':
            return self.human.genitalsObj

        return self.human.clothesObjs[selected]

    def reloadMaterial(self):
        obj = self.getSelectedObject()

        if shader.Shader.supported():
            self.listShaders(obj.material)
            self.listUniforms(obj.material)
        self.updateShaderConfig(obj.material)
        self.listMaterialSettings(obj)

        if obj.material.filepath:
            self.saveMaterialBtn._path = obj.material.filepath
            self.loadMaterialBtn._path = obj.material.filepath
        else:
            self.saveMaterialBtn._path = mh.getPath('data')
            self.loadMaterialBtn._path = mh.getSysDataPath()

    def onShow(self, arg):
        super(MaterialEditorTaskView, self).onShow(arg)
        if not shader.Shader.supported():
            gui3d.app.statusPersist('Shaders not supported by OpenGL')

        self.reloadMaterial()

    def onHide(self, arg):
        gui3d.app.statusPersist('')
        super(MaterialEditorTaskView, self).onHide(arg)

    def onHumanChanged(self, event):
        if event.change == 'reset':
            self.reloadMaterial()
        elif event.change == 'smooth':
            self.reloadMaterial()

class ColorValue(gui.GroupBox):
    def __init__(self, name, value):
        super(ColorValue, self).__init__(name)
        self.name = name

        self.widgets = []
        for col in xrange(3):
            child = FloatValue(self, 0)
            self.addWidget(child, 0, col)
            self.widgets.append(child)
        self.pickBtn = self.addWidget(gui.ColorPickButton(value))
        @self.pickBtn.mhEvent
        def onClicked(color):
            self.value = color
            self.callEvent('onActivate', self.getValue())

        self.value = value

    def getValue(self):
        return material.Color().copyFrom([widget.value for widget in self.widgets])

    def setValue(self, value):
        if isinstance(value, material.Color):
            value = value.asTuple()
        else:
            value = tuple(value)

        for idx, widget in enumerate(self.widgets):
            widget.setText(str(value[idx]))

    value = property(getValue, setValue)


class TextValue(gui.GroupBox):
    def __init__(self, name, value):
        super(TextValue, self).__init__(name)
        self.name = name

        self.widget = StringValue(self, value)
        self.addWidget(self.widget, 0, 0)
        self.value = value

    def getValue(self):
        return self.widget.value

    def setValue(self, value):
        self.widget.setText(str(value))

    value = property(getValue, setValue)


class ScalarValue(gui.GroupBox):
    def __init__(self, name, value):
        super(ScalarValue, self).__init__(name)
        self.name = name

        self.widget = FloatValue(self, 0)
        self.addWidget(self.widget, 0, 0)
        self.value = value

    def getValue(self):
        return self.widget.value

    def setValue(self, value):
        self.widget.setText(str(value))

    value = property(getValue, setValue)


class TruthValue(gui.GroupBox):
    def __init__(self, name, value):
        super(TruthValue, self).__init__(name)
        self.name = name

        self.widget = BooleanValue(self, False)
        self.addWidget(self.widget, 0, 0)
        self.value = value

    def getValue(self):
        return self.widget.value

    def setValue(self, value):
        self.widget.setSelected(value)

    value = property(getValue, setValue)


class ImageValue(gui.GroupBox):
    def __init__(self, name, value, defaultPath = None):
        super(ImageValue, self).__init__(name)
        self.name = name

        self.widget = TextureValue(self, value, defaultPath)
        self.addWidget(self.widget, 0, 0)
        self.value = value

    def getValue(self):
        return self.widget.value

    def setValue(self, value):
        self.widget.value = value

    value = property(getValue, setValue)


class FileValue(gui.GroupBox):
    def __init__(self, name, value, defaultPath = None):
        super(FileValue, self).__init__(name)
        self.name = name

        self.fileText = self.addWidget(gui.TextView(''), 0, 0)
        self.browseBtn = self.addWidget(gui.BrowseButton(), 1, 0)

        if value:
            self.browseBtn._path = value
        elif defaultPath:
            self.browseBtn._path = defaultPath

        @self.browseBtn.mhEvent
        def onClicked(path):
            if not path:
                return
            self.setValue(path)
            self.callEvent('onActivate', self.getValue())

        self.setValue(value)

    def getValue(self):
        return self._value

    def setValue(self, value):
        if value:
            self._value = value
            self.fileText.setText(os.path.basename(value))
        else:
            self.fileText.setText('Default')

    value = property(getValue, setValue)

class UniformValue(gui.GroupBox):
    def __init__(self, uniform, mat):
        super(UniformValue, self).__init__(uniform.name)

        self.uniform = uniform
        self.material = mat
        self.widgets = None
        self.colorPicker = None
        self.create()

    def create(self):
        values = None
        if self.material:
            # Material params have precedence over declarations in shader code
            params = self.material.shaderParameters
            values = params.get(self.uniform.name)
        if values is None:
            values = np.atleast_2d(self.uniform.values)
        else:
            values = np.atleast_2d(values)
        rows, cols = values.shape
        self.widgets = []
        for row in xrange(rows):
            widgets = []
            for col in xrange(cols):
                child = self.createWidget(values[row,col], row)
                self.addWidget(child, row, col)
                widgets.append(child)
            self.widgets.append(widgets)
        if self.uniform.pytype == float and rows == 1 and cols in [3, 4]:
            self.colorPicker = gui.ColorPickButton(material.Color().copyFrom(values[0,:3]))
            @self.colorPicker.mhEvent
            def onClicked(color):
                for idx,widget in enumerate(self.widgets[0][:3]):
                    widget.setValue(color.asTuple()[idx])
                self.callEvent('onActivate', color)
            self.addWidget(self.colorPicker, 1, 0)

    def createWidget(self, value, row):
        type = self.uniform.pytype
        if type == int:
            return IntValue(self, value)
        if type == float:
            return FloatValue(self, value)
        if type == str:
            # TODO account for tex idx
            defaultPath = mh.getSysDataPath('litspheres') if self.uniform.name == 'litsphereTexture' else None
            return TextureValue(self, value, defaultPath)
        if type == bool:
            return BooleanValue(self, value)
        return gui.TextView('???')

    def onActivate(self, arg=None):
        values = [[widget.value
                   for widget in widgets]
                  for widgets in self.widgets]
        if self.colorPicker:
            self.colorPicker.setColor(material.Color().copyFrom(values[0][:3]))
        if len(self.uniform.dims) == 1:
            values = values[0]
            if self.uniform.dims == (1,) and self.uniform.pytype == str:
                values = values[0]
                if not os.path.isfile(values):
                    return
        self.material.setShaderParameter(self.uniform.name, values)

class NumberValue(gui.TextEdit):
    def __init__(self, parent, value):
        super(NumberValue, self).__init__(str(value), self._validator)
        self.parent = parent

    def sizeHint(self):
        size = self.minimumSizeHint()
        size.width = size.width() * 3
        return size

    def onActivate(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

    def onChange(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

    def setValue(self, value):
        self.setText(str(value))

class StringValue(gui.TextEdit):
    def __init__(self, parent, value):
        super(StringValue, self).__init__(str(value))
        self.parent = parent

    @property
    def value(self):
        return unicode(self.text)

    def setValue(self, value):
        self.setText(value)

    def onActivate(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

    def onChange(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

class IntValue(NumberValue):
    _validator = gui.intValidator

    @property
    def value(self):
        return int(self.text)

class FloatValue(NumberValue):
    _validator = gui.floatValidator

    @property
    def value(self):
        return float(self.text)

class BooleanValue(gui.CheckBox):
    def __init__(self, parent, value):
        super(BooleanValue, self).__init__()
        self.parent = parent
        self.setSelected(value)

    def onClicked(self, arg=None):
        try:
            self.parent.callEvent('onActivate', self.value)
        except:
            pass

    @property
    def value(self):
        return self.selected

    def setValue(self, value):
        self.setChecked(value)

class TextureValue(gui.QtGui.QWidget, gui.Widget):
    def __init__(self, parent, value, defaultPath = None):
        super(TextureValue, self).__init__()
        self.parent = parent
        self._path = value

        self.layout = gui.QtGui.QGridLayout(self)
        self.imageView = gui.ImageView()
        self.browseBtn = gui.BrowseButton()
        self.browseBtn.setFilter("Image Files (*.png *.jpg *.bmp)")

        self.layout.addWidget(self.imageView)
        self.layout.addWidget(self.browseBtn)

        self.value = value

        if value and isinstance(value, basestring):
            self.browseBtn._path = value
        elif defaultPath:
            self.browseBtn._path = defaultPath

        @self.browseBtn.mhEvent
        def onClicked(path):
            if not path:
                return
            self._path = path
            self.imageView.setImage(self.value)
            self.parent.callEvent('onActivate', self.value)

    def getValue(self):
        return self._path

    def setValue(self, value):
        self._path = value
        if value:
            self.imageView.setImage(value)
            if isinstance(value, basestring):
                self.browseBtn._path = value
        else:
            self.imageView.setImage(mh.getSysDataPath('notfound.thumb'))

    value = property(getValue, setValue)


def load(app):
    category = app.getCategory('Utilities')
    taskview = category.addTask(MaterialEditorTaskView(category))

def unload(app):
    pass


