#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

MakeHuman Material format with parser and serializer.
"""

import log
import os

_autoSkinBlender = None

class Color(object):
    def __init__(self, r=0.00, g=0.00, b=0.00):
        if hasattr(r, '__iter__'):
            # Copy constructor
            self.copyFrom(r)
        else:
            self.setValues(r,g,b)

    def setValues(self, r, g, b):
        self.setR(r)
        self.setG(g)
        self.setB(b)

    def getValues(self):
        return [self.r, self.g, self.b]

    values = property(getValues, setValues)

    def setR(self, r):
        self._r = max(0.0, min(1.0, float(r)))

    def setG(self, g):
        self._g = max(0.0, min(1.0, float(g)))

    def setB(self, b):
        self._b = max(0.0, min(1.0, float(b)))

    def getR(self):
        return self._r

    def getG(self):
        return self._g

    def getB(self):
        return self._b

    r = property(getR, setR)
    g = property(getG, setG)
    b = property(getB, setB)

    def __repr__(self):
        return "Color(%s %s %s)" % (self.r,self.g,self.b)

    # List interface
    def __getitem__(self, key):
        return self.asTuple()[key]

    def __iter__(self):
        return self.asTuple().__iter__()

    def copyFrom(self, color):
        r = color[0]
        g = color[1]
        b = color[2]
        self.setValues(r, g, b)

        return self

    def asTuple(self):
        return (self.r, self.g, self.b)

    def asStr(self):
        return "%r %r %r" % self.asTuple()

    # Comparison operators
    def __lt__(self, other):
        return self.asTuple().__lt__(other.asTuple())

    def __le__(self, other):
        return self.asTuple().__le__(other.asTuple())

    def __eq__(self, other):
        return self.asTuple().__eq__(other.asTuple())

    def __ne__(self, other):
        return self.asTuple().__ne__(other.asTuple())

    def __gt__(self, other):
        return self.asTuple().__gt__(other.asTuple())

    def __ge__(self, other):
        return self.asTuple().__ge__(other.asTuple())


# Protected shaderDefine parameters that are set exclusively by means of shaderConfig options (configureShading())
_shaderConfigDefines = ['DIFFUSE', 'BUMPMAP', 'NORMALMAP', 'DISPLACEMENT', 'SPECULARMAP', 'VERTEX_COLOR']

# Protected shader parameters that are set exclusively by means of material properties (configureShading())
_materialShaderParams = ['diffuse', 'ambient', 'specular', 'emissive', 'diffuseTexture', 'bumpmapTexture', 'bumpmapIntensity', 'normalmapTexture', 'normalmapIntensity', 'displacementmapTexture', 'displacementmapTexture', 'specularmapTexture', 'specularmapIntensity']

class Material(object):
    """
    Material definition.
    Defines the visual appearance of an object when it is rendered (when it is
    set to solid).

    NOTE: Use one material per object! You can use copyFrom() to duplicate
    materials.
    """

    def __init__(self, name="UnnamedMaterial", performConfig=True):
        self.name = name

        self.filename = None
        self.filepath = None

        self._ambientColor = Color(1.0, 1.0, 1.0)
        self._diffuseColor = Color(1.0, 1.0, 1.0)
        self._specularColor = Color(1.0, 1.0, 1.0)
        self._shininess = 0.2
        self._emissiveColor = Color()

        self._opacity = 1.0
        self._translucency = 0.0

        self._shadeless = False   # Set to True to disable shading. Configured shader will have no effect
        self._wireframe = False   # Set to True to do wireframe render
        self._transparent = False # Set to True to enable transparency rendering (usually needed when opacity is < 1)
        self._backfaceCull = True # Set to False to disable backface culling (render back of polygons)
        self._depthless = False   # Set to True for depthless rendering (object is not occluded and does not occlude other objects)

        self._autoBlendSkin = False # Set to True to adapt diffuse color and litsphere texture to skin tone

        self._diffuseTexture = None
        self._bumpMapTexture = None
        self._bumpMapIntensity = 1.0
        self._normalMapTexture = None
        self._normalMapIntensity = 1.0
        self._displacementMapTexture = None
        self._displacementMapIntensity = 1.0
        self._specularMapTexture = None
        self._specularMapIntensity = 1.0
        self._transparencyMapTexture = None
        self._transparencyMapIntensity = 1.0

        # Sub-surface scattering parameters
        self._sssEnabled = False
        self._sssRScale = 0.0
        self._sssGScale = 0.0
        self._sssBScale = 0.0

        self._shader = None
        self._shaderConfig = {
            'diffuse'      : True,
            'bump'         : True,
            'normal'       : True,
            'displacement' : True,
            'spec'         : True,
            'vertexColors' : True
        }
        self._shaderParameters = {}
        self._shaderDefines = []
        self.shaderChanged = True   # Determines whether shader should be recompiled

        if performConfig:
            self._updateShaderConfig()

        self._uvMap = None

    def copyFrom(self, material):
        self.name = material.name

        self.filename = material.filename
        self.filepath = material.filepath

        self._ambientColor.copyFrom(material.ambientColor)
        self._diffuseColor.copyFrom(material._diffuseColor)
        self._specularColor.copyFrom(material.specularColor)
        self._shininess = material.shininess
        self._emissiveColor.copyFrom(material.emissiveColor)

        self._opacity = material.opacity
        self._translucency = material.translucency

        self._shadeless = material.shadeless
        self._wireframe = material.wireframe
        self._transparent = material.transparent
        self._backfaceCull = material.backfaceCull
        self._depthless = material.depthless

        self._autoBlendSkin = material.autoBlendSkin

        self._diffuseTexture = material.diffuseTexture
        self._bumpMapTexture = material.bumpMapTexture
        self._bumpMapIntensity = material.bumpMapIntensity
        self._normalMapTexture = material.normalMapTexture
        self._normalMapIntensity = material.normalMapIntensity
        self._displacementMapTexture = material.displacementMapTexture
        self._displacementMapIntensity = material.displacementMapIntensity
        self._specularMapTexture = material.specularMapTexture
        self._specularMapIntensity = material.specularMapIntensity
        self._transparencyMapTexture = material.transparencyMapTexture
        self._transparencyMapIntensity = material.transparencyMapIntensity

        self._sssEnabled = material.sssEnabled
        self._sssRScale = material.sssRScale
        self._sssGScale = material.sssGScale
        self._sssBScale = material.sssBScale

        self._shader = material.shader
        self._shaderConfig = dict(material._shaderConfig)
        self._shaderParameters = dict(material._shaderParameters)
        self._shaderDefines = list(material.shaderDefines)
        self.shaderChanged = True

        self._uvMap = material.uvMap

        return self

    def fromFile(self, filename):
        """
        Parse .mhmat file and set as the properties of this material.
        """
        log.debug("Loading material from file %s", filename)
        try:
            f = open(filename, "rU")
        except:
            f = None
        if f == None:
            log.error("Failed to load material from file %s.", filename)
            return

        self.filename = os.path.normpath(filename)
        self.filepath = os.path.dirname(self.filename)

        shaderConfig_diffuse = None
        shaderConfig_bump = None
        shaderConfig_normal = None
        shaderConfig_displacement = None
        shaderConfig_spec = None
        shaderConfig_vertexColors = None

        for line in f:
            words = line.split()
            if len(words) == 0:
                continue
            if words[0] in ["#", "//"]:
                continue

            if words[0] == "name":
                self.name = words[1]
            elif words[0] == "ambientColor":
                self._ambientColor.copyFrom([float(w) for w in words[1:4]])
            elif words[0] == "diffuseColor":
                self._diffuseColor.copyFrom([float(w) for w in words[1:4]])
            elif words[0] == "diffuseIntensity":
                log.warning('Deprecated parameter "diffuseIntensity" specified in material %s', self.name)
            elif words[0] == "specularColor":
                self._specularColor.copyFrom([float(w) for w in words[1:4]])
            elif words[0] == "specularIntensity":
                log.warning('Deprecated parameter "specularIntensity" specified in material %s', self.name)
            elif words[0] == "shininess":
                self._shininess = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "emissiveColor":
                self._emissiveColor.copyFrom([float(w) for w in words[1:4]])
            elif words[0] == "opacity":
                self._opacity = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "translucency":
                self._translucency = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "shadeless":
                self._shadeless = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "wireframe":
                self._wireframe = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "transparent":
                self._transparent = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "backfaceCull":
                self._backfaceCull = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "depthless":
                self._depthless = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "autoBlendSkin":
                self._autoBlendSkin = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "diffuseTexture":
                self._diffuseTexture = getFilePath(words[1], self.filepath)
            elif words[0] == "bumpmapTexture":
                self._bumpMapTexture = getFilePath(words[1], self.filepath)
            elif words[0] == "bumpmapIntensity":
                self._bumpMapIntensity = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "normalmapTexture":
                self._normalMapTexture = getFilePath(words[1], self.filepath)
            elif words[0] == "normalmapIntensity":
                self._normalMapIntensity = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "displacementmapTexture":
                self._displacementMapTexture = getFilePath(words[1], self.filepath)
            elif words[0] == "displacementmapIntensity":
                self._displacementMapIntensity = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "specularmapTexture":
                self._specularMapTexture = getFilePath(words[1], self.filepath)
            elif words[0] == "specularmapIntensity":
                self._specularMapIntensity = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "transparencymapTexture":
                self._transparencyMapTexture = getFilePath(words[1], self.filepath)
            elif words[0] == "transparencymapIntensity":
                self._transparencyMapIntensity = max(0.0, min(1.0, float(words[1])))
            elif words[0] == "sssEnabled":
                self._sssEnabled = words[1].lower() in ["yes", "enabled", "true"]
            elif words[0] == "sssRScale":
                self._sssRScale = max(0.0, float(words[1]))
            elif words[0] == "sssGScale":
                self._sssGScale = max(0.0, float(words[1]))
            elif words[0] == "sssBScale":
                self._sssBScale = max(0.0, float(words[1]))
            elif words[0] == "shader":
                self._shader = getShaderPath(words[1], self.filepath)
            elif words[0] == "uvMap":
                self._uvMap = getFilePath(words[1], self.filepath)
                from getpath import getSysDataPath, canonicalPath
                if self._uvMap and \
                   canonicalPath(self._uvMap) == canonicalPath(getSysDataPath('uvs/default.obj')):
                    # uvs/default.obj is a meta-file that refers to the default uv set
                    self._uvMap = None
            elif words[0] == "shaderParam":
                if len(words) > 3:
                    self.setShaderParameter(words[1], words[2:])
                else:
                    self.setShaderParameter(words[1], words[2])
            elif words[0] == "shaderDefine":
                self.addShaderDefine(words[1])
            elif words[0] == "shaderConfig":
                if words[1] == "diffuse":
                    shaderConfig_diffuse = words[2].lower() in ["yes", "enabled", "true"]
                elif words[1] == "bump":
                    shaderConfig_bump = words[2].lower() in ["yes", "enabled", "true"]
                elif words[1] == "normal":
                    shaderConfig_normal = words[2].lower() in ["yes", "enabled", "true"]
                elif words[1] == "displacement":
                    shaderConfig_displacement = words[2].lower() in ["yes", "enabled", "true"]
                elif words[1] == "spec":
                    shaderConfig_spec = words[2].lower() in ["yes", "enabled", "true"]
                elif words[1] == "vertexColors":
                    shaderConfig_vertexColors = words[2].lower() in ["yes", "enabled", "true"]

        f.close()
        self.configureShading(diffuse=shaderConfig_diffuse, bump=shaderConfig_bump, normal=shaderConfig_normal, displacement=shaderConfig_displacement, spec=shaderConfig_spec, vertexColors=shaderConfig_vertexColors)

    def _texPath(self, filename, materialPath = None):
        """
        Produce a portable path for writing to file.
        """
        if materialPath:
            return os.path.relpath(filename, materialPath).replace('\\', '/')
        elif self.filepath:
            return os.path.relpath(filename, self.filepath).replace('\\', '/')
        else:
            return os.path.normpath(filename).replace('\\', '/')

    def toFile(self, filename, comments = []):
        import codecs

        try:
            f = codecs.open(filename, 'w', encoding='utf-8')
        except:
            f = None
        if f == None:
            log.error("Failed to open material file %s for writing.", filename)
            return

        f.write('# Material definition for %s\n' % self.name)
        for comment in comments:
            if not (comment.strip().startswith('//') or comment.strip().startswith('#')):
                comment = "# " + comment
            f.write(comment+"\n")
        f.write("\n")

        f.write("name %s\n" % self.name)
        f.write("ambientColor %s\n" % self.ambientColor.asStr())
        f.write("diffuseColor %s\n" % self.diffuseColor.asStr())
        f.write("specularColor %s\n" % self.specularColor.asStr())
        f.write("shininess %s\n" % self.shininess)
        f.write("emissiveColor %s\n" % self.emissiveColor.asStr())
        f.write("opacity %s\n" % self.opacity)
        f.write("translucency %s\n\n" % self.translucency)

        f.write("shadeless %s\n" % self.shadeless)
        f.write("wireframe %s\n" % self.wireframe)
        f.write("transparent %s\n" % self.transparent)
        f.write("backfaceCull %s\n" % self.backfaceCull)
        f.write("depthless %s\n\n" % self.depthless)

        hasTexture = False
        filedir = os.path.dirname(filename)
        if self.diffuseTexture:
            f.write("diffuseTexture %s\n" % self._texPath(self.diffuseTexture, filedir) )
            hasTexture = True
        if self.bumpMapTexture:
            f.write("bumpmapTexture %s\n" % self._texPath(self.bumpMapTexture, filedir) )
            f.write("bumpmapIntensity %s\n" % self.bumpMapIntensity)
            hasTexture = True
        if self.normalMapTexture:
            f.write("normalmapTexture %s\n" % self._texPath(self.normalMapTexture, filedir) )
            f.write("normalmapIntensity %s\n" % self.normalMapIntensity)
            hasTexture = True
        if self.displacementMapTexture:
            f.write("displacementmapTexture %s\n" % self._texPath(self.displacementMapTexture, filedir) )
            f.write("displacementmapIntensity %s\n" % self.displacementMapIntensity)
            hasTexture = True
        if self.specularMapTexture:
            f.write("specularmapTexture %s\n" % self._texPath(self.specularMapTexture, filedir) )
            f.write("specularmapIntensity %s\n" % self.specularMapIntensity)
            hasTexture = True
        if self.transparencyMapTexture:
            f.write("transparencymapTexture %s\n" % self._texPath(self.transparencyMapTexture, filedir) )
            f.write("transparencymapIntensity %s\n" % self.transparencyMapIntensity)
            hasTexture = True
        if hasTexture: f.write('\n')

        if self.sssEnabled:
            f.write("# Sub-surface scattering parameters\n" )
            f.write("sssEnabled %s\n" % self.sssEnabled )
            f.write("sssRScale %s\n" % self.sssRScale )
            f.write("sssGScale %s\n" % self.sssGScale )
            f.write("sssBScale %s\n\n" % self.sssBScale )

        if self.uvMap:
            f.write("uvMap %s\n\n" % self._texPath(self.uvMap, filedir) )

        if self.shader:
            f.write("shader %s\n\n" % self.shader.replace('\\', '/'))

        hasShaderParam = False
        global _materialShaderParams
        for name, param in self.shaderParameters.items():
            if name not in _materialShaderParams:
                hasShaderParam = True
                import image
                if isinstance(param, list):
                    f.write("shaderParam %s %s\n" % (name, " ".join([str(p) for p in param])) )
                elif isinstance(param, image.Image):
                    if hasattr(param, "sourcePath"):
                        f.write("shaderParam %s %s\n" % (name, self._texPath(param.sourcePath, filedir)) )
                elif isinstance(param, basestring) and not isNumeric(param):
                    # Assume param is a path
                    f.write("shaderParam %s %s\n" % (name, self._texPath(param, filedir)) )
                else:
                    f.write("shaderParam %s %s\n" % (name, param) )
        if hasShaderParam: f.write('\n')

        hasShaderDefine = False
        global _shaderConfigDefines
        for define in self.shaderDefines:
            if define not in _shaderConfigDefines:
                hasShaderDefine = True
                f.write("shaderDefine %s\n" % define)
        if hasShaderDefine: f.write('\n')

        for name, value in self.shaderConfig.items():
            f.write("shaderConfig %s %s\n" % (name, value) )

        f.close()

    def getUVMap(self):
        return self._uvMap

    def setUVMap(self, uvMap):
        self._uvMap = getFilePath(uvMap, self.filepath)
        from getpath import getSysDataPath, canonicalPath
        if self._uvMap and \
           canonicalPath(self._uvMap) == canonicalPath(getSysDataPath('uvs/default.obj')):
            # uvs/default.obj is a meta-file that refers to the default uv set
            self._uvMap = None

    uvMap = property(getUVMap, setUVMap)

    def getAmbientColor(self):
        return self._ambientColor

    def setAmbientColor(self, color):
        self._ambientColor.copyFrom(color)

    ambientColor = property(getAmbientColor, setAmbientColor)


    def getDiffuseColor(self):
        if self.autoBlendSkin:
            self._diffuseColor = Color(getSkinBlender().getDiffuseColor())
        return self._diffuseColor

    def setDiffuseColor(self, color):
        self._diffuseColor.copyFrom(color)

    diffuseColor = property(getDiffuseColor, setDiffuseColor)


    def getDiffuseIntensity(self):
        """
        Read-only property that represents the greyscale intensity of the
        diffuse color.
        """
        return getIntensity(self.diffuseColor)

    @property
    def diffuseIntensity(self):
        return self.getDiffuseIntensity()


    def getSpecularColor(self):
        return self._specularColor

    def setSpecularColor(self, color):
        self._specularColor.copyFrom(color)

    specularColor = property(getSpecularColor, setSpecularColor)


    def getShininess(self):
        """
        The specular shininess (the inverse of roughness or specular hardness).
        """
        return self._shininess

    def setShininess(self, hardness):
        """
        Sets the specular hardness or shinyness. Between 0 and 1.
        """
        self._shininess = min(1.0, max(0.0, hardness))

    shininess = property(getShininess, setShininess)


    def getSpecularIntensity(self):
        """
        Read-only property that represents the greyscale intensity of the
        specular color.
        """
        return getIntensity(self.specularColor)

    @property
    def specularIntensity(self):
        return self.getSpecularIntensity()


    def getEmissiveColor(self):
        #return self._emissiveColor.values
        return self._emissiveColor

    def setEmissiveColor(self, color):
        self._emissiveColor.copyFrom(color)

    emissiveColor = property(getEmissiveColor, setEmissiveColor)


    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = min(1.0, max(0.0, opacity))

    opacity = property(getOpacity, setOpacity)


    def getTranslucency(self):
        return self._translucency

    def setTranslucency(self, translucency):
        self._translucency = min(1.0, max(0.0, translucency))

    translucency = property(getTranslucency, setTranslucency)


    def getShadeless(self):
        return self._shadeless

    def setShadeless(self, shadeless):
        self._shadeless = shadeless

    shadeless = property(getShadeless, setShadeless)

    def getWireframe(self):
        return self._wireframe

    def setWireframe(self, wireframe):
        self._wireframe = wireframe

    wireframe = property(getWireframe, setWireframe)

    def getTransparent(self):
        return self._transparent

    def setTransparent(self, transparent):
        self._transparent = transparent

    transparent = property(getTransparent, setTransparent)

    def getBackfaceCull(self):
        return self._backfaceCull

    def setBackfaceCull(self, backfaceCull):
        self._backfaceCull = backfaceCull

    backfaceCull = property(getBackfaceCull, setBackfaceCull)

    def getDepthless(self):
        return self._depthless

    def setDepthless(self, depthless):
        self._depthless = depthless

    depthless = property(getDepthless, setDepthless)

    def getAutoBlendSkin(self):
        return self._autoBlendSkin

    def setAutoBlendSkin(self, autoblend):
        self._autoBlendSkin = autoblend

    autoBlendSkin = property(getAutoBlendSkin, setAutoBlendSkin)

    def getSSSEnabled(self):
        return self._sssEnabled

    def setSSSEnabled(self, sssEnabled):
        self._sssEnabled = sssEnabled

    sssEnabled = property(getSSSEnabled, setSSSEnabled)

    def getSSSRScale(self):
        return self._sssRScale

    def setSSSRScale(self, sssRScale):
        self._sssRScale = sssRScale

    sssRScale = property(getSSSRScale, setSSSRScale)

    def getSSSGScale(self):
        return self._sssGScale

    def setSSSGScale(self, sssGScale):
        self._sssGScale = sssGScale

    sssGScale = property(getSSSGScale, setSSSGScale)

    def getSSSBScale(self):
        return self._sssBScale

    def setSSSBScale(self, sssBScale):
        self._sssBScale = sssBScale

    sssBScale = property(getSSSBScale, setSSSBScale)


    def supportsDiffuse(self):
        return self.diffuseTexture != None

    def supportsBump(self):
        return self.bumpMapTexture != None

    def supportsDisplacement(self):
        return self.displacementMapTexture != None

    def supportsNormal(self):
        return self.normalMapTexture != None

    def supportsSpecular(self):
        return self.specularMapTexture != None

    def supportsTransparency(self):
        return self.transparencyMapTexture != None

    def configureShading(self, diffuse=None, bump = None, normal=None, displacement=None, spec = None, vertexColors = None):
        """
        Configure shading options and set the necessary properties based on
        the material configuration of this object. This configuration applies
        for shaders only (depending on whether the selected shader supports the
        chosen options), so only has effect when a shader is set.
        This method can be invoked even when no shader is set, the chosen
        options will remain effective when another shader is set.
        A value of None leaves configuration options unchanged.
        """
        if diffuse != None: self._shaderConfig['diffuse'] = diffuse
        if bump != None: self._shaderConfig['bump'] = bump
        if normal != None: self._shaderConfig['normal'] = normal
        if displacement != None: self._shaderConfig['displacement'] = displacement
        if spec != None: self._shaderConfig['spec'] = spec
        if vertexColors != None: self._shaderConfig['vertexColors'] = vertexColors

        self._updateShaderConfig()

    @property
    def shaderConfig(self):
        """
        The shader parameters as set by configureShading().
        """
        return dict(self._shaderConfig)

    def _updateShaderConfig(self):
        global _shaderConfigDefines
        global _materialShaderParams

        if not self.shader:
            return

        # Remove (non-custom) shader config defines (those set by shader config)
        for shaderDefine in _shaderConfigDefines:
            try:
                self._shaderDefines.remove(shaderDefine)
            except:
                pass

        # Reset (non-custom) shader parameters controlled by material properties
        for shaderParam in _materialShaderParams:
            try:
                del self._shaderParameters[shaderParam]
            except:
                pass

        if self._shaderConfig['vertexColors']:
            #log.debug("Enabling vertex colors.")
            self._shaderDefines.append('VERTEX_COLOR')
        if self._shaderConfig['diffuse'] and self.supportsDiffuse():
            #log.debug("Enabling diffuse texturing.")
            self._shaderDefines.append('DIFFUSE')
            self._shaderParameters['diffuseTexture'] = self.diffuseTexture
        bump = self._shaderConfig['bump'] and self.supportsBump()
        normal = self._shaderConfig['normal'] and self.supportsNormal()
        if bump and not normal:
            #log.debug("Enabling bump mapping.")
            self._shaderDefines.append('BUMPMAP')
            self._shaderParameters['bumpmapTexture'] = self.bumpMapTexture
            self._shaderParameters['bumpmapIntensity'] = self.bumpMapIntensity
        if normal:
            #log.debug("Enabling normal mapping.")
            self._shaderDefines.append('NORMALMAP')
            self._shaderParameters['normalmapTexture'] = self.normalMapTexture
            self._shaderParameters['normalmapIntensity'] = self.normalMapIntensity
        if self._shaderConfig['displacement'] and self.supportsDisplacement():
            #log.debug("Enabling displacement mapping.")
            self._shaderDefines.append('DISPLACEMENT')
            self._shaderParameters['displacementmapTexture'] = self.displacementMapTexture
            self._shaderParameters['displacementmapIntensity'] = self.displacementMapIntensity
        if self._shaderConfig['spec'] and self.supportsSpecular():
            #log.debug("Enabling specular mapping.")
            self._shaderDefines.append('SPECULARMAP')
            self._shaderParameters['specularmapTexture'] = self.specularMapTexture
            self._shaderParameters['specularmapIntensity'] = self._specularMapIntensity

        self._shaderDefines.sort()   # This is important for shader caching
        self.shaderChanged = True

    def setShader(self, shader):
        self._shader = getShaderPath(shader, self.filepath)
        self._updateShaderConfig()
        self.shaderChanged = True

    def getShader(self):
        return self._shader

    shader = property(getShader, setShader)

    def getShaderObj(self):
        import shader
        return shader.getShader(self.getShader(), self.shaderDefines)

    @property
    def shaderObj(self):
        return self.getShaderObj()


    @property
    def shaderParameters(self):
        """
        All shader parameters. Both those set by material properties as well as
        custom shader parameters set by setShaderParameter().
        """
        import numpy as np

        result = dict(self._shaderParameters)
        result['ambient']  = self.ambientColor.values
        result['diffuse'] = self.diffuseColor.values + [self.opacity]
        result['specular'] = self.specularColor.values + [self.shininess]
        result['emissive'] = self.emissiveColor

        if self.autoBlendSkin:
            result["litsphereTexture"] = getSkinBlender().getLitsphereTexture()
        return result

    def setShaderParameter(self, name, value):
        """
        Set a custom shader parameter. Shader parameters are uniform parameters
        passed to the shader programme, their type should match that declared in
        the shader code.
        """
        global _materialShaderParams

        if name in _materialShaderParams:
            raise RuntimeError('The shader parameter "%s" is protected and should be set by means of material properties.' % name)

        if isinstance(value, list):
            value = [float(v) for v in value]
        elif isinstance(value, basestring):
            if isNumeric(value):
                value = float(value)
            else:
                # Assume value is a path
                value = getFilePath(value, self.filepath)

        self._shaderParameters[name] = value

    def removeShaderParameter(self, name):
        global _materialShaderParams

        if name in _materialShaderParams:
            raise RuntimeError('The shader parameter "%s" is protected and should be set by means of material properties.' % name)
        try:
            del self._shaderParameters[name]
        except:
            pass

    def clearShaderParameters(self):
        """
        Remove all custom set shader parameters.
        """
        global _materialShaderParams

        for shaderParam in self.shaderParameters:
            if shaderParam not in _materialShaderParams:
                self.removeShaderParameter(shaderParam)


    @property
    def shaderDefines(self):
        """
        All shader defines. Both those set by configureShading() as well as
        custom shader defines set by addShaderDefine().
        """
        return list(self._shaderDefines)

    def addShaderDefine(self, defineStr):
        global _shaderConfigDefines

        if defineStr in _shaderConfigDefines:
            raise RuntimeError('The shader define "%s" is protected and should be set by means of configureShading().' % defineStr)
        if defineStr in self.shaderDefines:
            return
        self._shaderDefines.append(defineStr)
        self._shaderDefines.sort()   # This is important for shader caching

        self.shaderChanged = True

    def removeShaderDefine(self, defineStr):
        global _shaderConfigDefines

        if defineStr in _shaderConfigDefines:
            raise RuntimeError('The shader define %s is protected and should be set by means of configureShading().' % defineStr)
        try:
            self._shaderDefines.remove(defineStr)
        except:
            pass

        self.shaderChanged = True

    def clearShaderDefines(self):
        """
        Remove all custom set shader defines.
        """
        global _shaderConfigDefines

        for shaderDefine in self._shaderDefines:
            if shaderDefine not in _shaderConfigDefines:
                self.removeShaderDefine(shaderDefine)
        self.shaderChanged = True


    def _getTexture(self, texture):
        if isinstance(texture, basestring):
            return getFilePath(texture, self.filepath)
        else:
            return texture


    def getDiffuseTexture(self):
        return self._diffuseTexture

    def setDiffuseTexture(self, texture):
        self._diffuseTexture = self._getTexture(texture)
        self._updateShaderConfig()

    diffuseTexture = property(getDiffuseTexture, setDiffuseTexture)


    def getBumpMapTexture(self):
        return self._bumpMapTexture

    def setBumpMapTexture(self, texture):
        self._bumpMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    bumpMapTexture = property(getBumpMapTexture, setBumpMapTexture)


    def getBumpMapIntensity(self):
        return self._bumpMapIntensity

    def setBumpMapIntensity(self, intensity):
        self._bumpMapIntensity = intensity
        self._updateShaderConfig()

    bumpMapIntensity = property(getBumpMapIntensity, setBumpMapIntensity)


    def getNormalMapTexture(self):
        return self._normalMapTexture

    def setNormalMapTexture(self, texture):
        self._normalMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    normalMapTexture = property(getNormalMapTexture, setNormalMapTexture)


    def getNormalMapIntensity(self):
        return self._normalMapIntensity

    def setNormalMapIntensity(self, intensity):
        self._normalMapIntensity = intensity
        self._updateShaderConfig()

    normalMapIntensity = property(getNormalMapIntensity, setNormalMapIntensity)


    def getDisplacementMapTexture(self):
        return self._displacementMapTexture

    def setDisplacementMapTexture(self, texture):
        self._displacementMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    displacementMapTexture = property(getDisplacementMapTexture, setDisplacementMapTexture)


    def getDisplacementMapIntensity(self):
        return self._displacementMapIntensity

    def setDisplacementMapIntensity(self, intensity):
        self._displacementMapIntensity = intensity
        self._updateShaderConfig()

    displacementMapIntensity = property(getDisplacementMapIntensity, setDisplacementMapIntensity)


    def getSpecularMapTexture(self):
        """
        The specular or reflectivity map texture.
        """
        return self._specularMapTexture

    def setSpecularMapTexture(self, texture):
        """
        Set the specular or reflectivity map texture.
        """
        self._specularMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    specularMapTexture = property(getSpecularMapTexture, setSpecularMapTexture)


    def getSpecularMapIntensity(self):
        return self._specularMapIntensity

    def setSpecularMapIntensity(self, intensity):
        self._specularMapIntensity = intensity
        self._updateShaderConfig()

    specularMapIntensity = property(getSpecularMapIntensity, setSpecularMapIntensity)


    def getTransparencyMapTexture(self):
        """
        The transparency or reflectivity map texture.
        """
        return self._transparencyMapTexture

    def setTransparencyMapTexture(self, texture):
        """
        Set the transparency or reflectivity map texture.
        """
        self._transparencyMapTexture = self._getTexture(texture)
        self._updateShaderConfig()

    transparencyMapTexture = property(getTransparencyMapTexture, setTransparencyMapTexture)


    def getTransparencyMapIntensity(self):
        return self._transparencyMapIntensity

    def setTransparencyMapIntensity(self, intensity):
        self._transparencyMapIntensity = intensity
        self._updateShaderConfig()

    transparencyMapIntensity = property(getTransparencyMapIntensity, setTransparencyMapIntensity)


def fromFile(filename):
    """
    Create a material from a .mhmat file.
    """
    mat = Material(performConfig=False)
    mat.fromFile(filename)
    return mat

def getSkinBlender():
    global _autoSkinBlender
    if not _autoSkinBlender:
        import autoskinblender
        from core import G
        human = G.app.selectedHuman
        _autoSkinBlender = autoskinblender.EthnicSkinBlender(human)
    return _autoSkinBlender

def getFilePath(filename, folder = None):
    if not filename:
        return filename

    # Ensure unix style path
    filename.replace('\\', '/')

    # Search within current folder
    if folder:
        path = os.path.join(folder, filename)
        if os.path.isfile(path):
            return os.path.abspath(path)
    # Treat as absolute path or search relative to application path
    if os.path.isfile(filename):
        return os.path.abspath(filename)
    # Search in user data folder
    from getpath import getPath, getSysDataPath, getSysPath
    userPath = getPath(filename)
    if os.path.isfile(userPath):
        return os.path.abspath(userPath)
    # Search in system path
    sysPath = getSysPath(filename)
    if os.path.isfile(sysPath):
        return os.path.abspath(sysPath)
    # Search in system data path
    sysPath = getSysDataPath(filename)
    if os.path.isfile(sysPath):
        return os.path.abspath(sysPath)

    # Nothing found
    return os.path.normpath(filename)

def getShaderPath(shader, folder = None):
    shaderSuffixes = ['_vertex_shader.txt', '_fragment_shader.txt', '_geometry_shader.txt']
    paths = [shader+s for s in shaderSuffixes]
    paths = [p for p in paths if os.path.isfile(getFilePath(p, folder))]
    if len(paths) > 0:
        path = getFilePath(paths[0], folder)
        for s in shaderSuffixes:
            if path.endswith(s):
                path = path[:-len(s)]
    else:
        path = shader
    return path

def isNumeric(string):
    try:
        return unicode(string).isnumeric()
    except:
        # On decoding errors
        return False

def getIntensity(color):
    return 0.2126 * color[0] + \
           0.7152 * color[1] + \
           0.0722 * color[2]

class UVMap:
    def __init__(self, name):
        self.name = name
        self.type = "UvSet"
        self.filepath = None
        self.materialName = "Default"
        self.uvs = None
        self.fuvs = None


    def read(self, mesh, filepath):
        import numpy as np

        filename,ext = os.path.splitext(filepath)
        if ext == ".mhuv":
            raise NameError("ERROR: .mhuv files are obsolete. Change to .obj: %s" % filepath)

        uvs,fuvs = loadUvObjFile(filepath)
        self.filepath = filepath
        self.uvs = np.array(uvs)
        self.fuvs = np.array(fuvs)


def loadUvObjFile(filepath):
    fp = open(filepath, "rU")
    uvs = []
    fuvs = []
    for line in fp:
        words = line.split()
        if len(words) == 0:
            continue
        elif words[0] == "vt":
            uvs.append((float(words[1]), float(words[2])))
        elif words[0] == "f":
            fuvs.append( [(int(word.split("/")[1]) - 1) for word in words[1:]] )
    fp.close()
    return uvs,fuvs
