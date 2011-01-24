"""
The main MakeHuman Python Application file.

B{Project Name:}      MakeHuman

B{Product Home Page:} U{http://www.makehuman.org/}

B{Code Home Page:}    U{http://code.google.com/p/makehuman/}

B{Authors:}           Manuel Bastioni, Marc Flerackers

B{Copyright(c):}      MakeHuman Team 2001-2010

B{Licensing:}         GPL3 (see also U{http://sites.google.com/site/makehumandocs/licensing})

B{Coding Standards:}  See U{http://sites.google.com/site/makehumandocs/developers-guide}

Abstract
========

This is the main MakeHuman Python Application file which participates in the
application startup process. It contains functions that respond to events
affecting the main GUI toolbar along the top of the screen in all modes to
support switching between modes.

When the MakeHuman application is launched the *main* function from the C
application file *main.c* runs. This creates an integration layer by
dynamically generating a Python module (called 'mh'). That *main* function
then either imports this Python *main* module or executes this Python
script *main.py* (depending on platform).

This script displays a splash screen and a progress bar as it loads the
initial 3D humanoid model (the neutral base object) and adds the various
GUI sections into the scene. It creates the main toolbar that enables the
user to switch between different GUI modes and defines functions to
perform that switch for all active buttons. Active buttons are connected
to these functions by being registered to receive events.

At the end of the initiation process the splash screen is hidden and
Modelling mode is activated. The 'startEventLoop' method on the main Scene3D
object is invoked to call the OpenGL/SDL C functions that manage the
low-level event loop.

This Python module responds to high-level GUI toolbar events to switch
between different GUI modes, but otherwise events are handled by GUI mode
specific Python modules.
"""

import sys
#print sys.builtin_module_names
#if 'nt' in sys.builtin_module_names:
sys.path.append("./pythonmodules")
import os

def recursiveDirNames(root):
  pathlist=[]
  #root=os.path.dirname(root)
  for filename in os.listdir(root):
    path=os.path.join(root,filename)
    if not (os.path.isfile(path) or filename=="." or filename==".." or filename==".svn"):
      pathlist.append(path)
      pathlist = pathlist + recursiveDirNames(path) 
  return(pathlist)

sys.path.append("./")
sys.path.append("./apps")
sys.path.append("./shared")
sys.path.append("./shared/mhx/templates")
sys.path.append("./shared/mhx")
sys.path=sys.path + recursiveDirNames("./apps")
sys.path.append("./core")
sys.path=sys.path + recursiveDirNames("./core")

import subprocess
import webbrowser
import glob, imp
from os.path import join, basename, splitext

import mh
import gui3d, events3d, font3d
import mh2obj, mh2bvh, mh2mhx
import human, hair_chooser, background, human_texture
import guimodelling, guifiles#, guirender
from aljabr import centroid
import algos3d
#import font3d

class MHApplication(gui3d.Application):
  
    def __init__(self):
        gui3d.Application.__init__(self)

        self.modelCamera = mh.Camera()

        mh.cameras.append(self.modelCamera)

        self.guiCamera = mh.Camera()
        self.guiCamera.fovAngle = 45
        self.guiCamera.eyeZ = 10
        self.guiCamera.projection = 0
        mh.cameras.append(self.guiCamera)

        self.setTheme("default")
        #self.setTheme("3d")
        
        self.fonts = {}
        
        self.settings = {}
        self.shortcuts = {
            # Actions
            (events3d.KMOD_CTRL, events3d.SDLK_z): self.undo,
            (events3d.KMOD_CTRL, events3d.SDLK_y): self.redo,
            (events3d.KMOD_CTRL, events3d.SDLK_m): self.goToModelling,
            (events3d.KMOD_CTRL, events3d.SDLK_s): self.goToSave,
            (events3d.KMOD_CTRL, events3d.SDLK_l): self.goToLoad,
            (events3d.KMOD_CTRL, events3d.SDLK_e): self.goToExport,
            (events3d.KMOD_CTRL, events3d.SDLK_r): self.goToRendering,
            (events3d.KMOD_CTRL, events3d.SDLK_h): self.goToHelp,
            (events3d.KMOD_CTRL, events3d.SDLK_q): self.stop,
            (events3d.KMOD_CTRL, events3d.SDLK_w): self.toggleStereo,
            (events3d.KMOD_CTRL, events3d.SDLK_f): self.toggleSolid,
            (events3d.KMOD_ALT, events3d.SDLK_t): self.saveTarget,
            (events3d.KMOD_ALT, events3d.SDLK_e): self.quickExport,
            (events3d.KMOD_ALT, events3d.SDLK_s): self.subdivide,
            (events3d.KMOD_ALT, events3d.SDLK_g): self.grabScreen,
            # Camera navigation
            (0, events3d.SDLK_2): self.rotateDown,
            (0, events3d.SDLK_4): self.rotateLeft,
            (0, events3d.SDLK_6): self.rotateRight,
            (0, events3d.SDLK_8): self.rotateUp,
            (0, events3d.SDLK_UP): self.panUp,
            (0, events3d.SDLK_DOWN): self.panDown,
            (0, events3d.SDLK_RIGHT): self.panRight,
            (0, events3d.SDLK_LEFT): self.panLeft,
            (0, events3d.SDLK_PLUS): self.zoomIn,
            (0, events3d.SDLK_MINUS): self.zoomOut,
            (0, events3d.SDLK_7): self.sideView,
            (0, events3d.SDLK_1): self.frontView,
            (0, events3d.SDLK_3): self.topView,
            (0, events3d.SDLK_PERIOD): self.resetView
        }

        # Display the initial splash screen and the progress bar during startup
        self.splash = gui3d.Object(self, "data/3dobjs/splash.obj", self.getThemeResource("images", "splash.png"), position = [0, 0, 0])
        self.progressBar = gui3d.ProgressBar(self)
        self.scene3d.update()
        self.scene3d.redraw(0)

        self.progressBar.setProgress(0.2)

        gui3d.Object(self, "data/3dobjs/upperbar.obj", self.getThemeResource("images", "upperbar.png"), [0, 0, 9])
        gui3d.Object(self, "data/3dobjs/backgroundbox.obj", position = [0, 0, -89.99])
        gui3d.Object(self, "data/3dobjs/lowerbar.obj", self.getThemeResource("images", "lowerbar.png"), [0, 32, 9])
        gui3d.Object(self, "data/3dobjs/lowerbar2.obj", self.getThemeResource("images", "lowerbar.png"), [0, 580, 9])

        self.progressBar.setProgress(0.3)
        #hairObj = hair.loadHairsFile(self.scene3d, path="./data/hairs/default", update = False)
        #self.scene3d.clear(hairObj) 
        self.scene3d.selectedHuman = human.Human(self.scene3d, "data/3dobjs/base.obj")
        self.scene3d.selectedHuman.setTexture("data/textures/texture.tif")
        self.progressBar.setProgress(0.6)

        self.tool = None
        self.selectedGroup = None

        self.undoStack = []
        self.redoStack = []

        @self.scene3d.selectedHuman.event
        def onMouseDown(event):
          if self.tool:
            self.selectedGroup = self.app.scene3d.getSelectedFacesGroup()
            self.tool.callEvent("onMouseDown", event)
          else:
            self.currentTask.callEvent("onMouseDown", event)

        @self.scene3d.selectedHuman.event
        def onMouseMoved(event):
          if self.tool:
            self.tool.callEvent("onMouseMoved", event)
          else:
            self.currentTask.callEvent("onMouseMoved", event)

        @self.scene3d.selectedHuman.event
        def onMouseDragged(event):
          if self.tool:
            self.tool.callEvent("onMouseDragged", event)
          else:
            self.currentTask.callEvent("onMouseDragged", event)

        @self.scene3d.selectedHuman.event
        def onMouseUp(event):
          if self.tool:
            self.tool.callEvent("onMouseUp", event)
          else:
            self.currentTask.callEvent("onMouseUp", event)

        @self.scene3d.selectedHuman.event
        def onMouseEntered(event):
          if self.tool:
            self.tool.callEvent("onMouseEntered", event)
          else:
            self.currentTask.callEvent("onMouseEntered", event)

        @self.scene3d.selectedHuman.event
        def onMouseExited(event):
          if self.tool:
            self.tool.callEvent("onMouseExited", event)
          else:
            self.currentTask.callEvent("onMouseExited", event)

        # Set up categories and tasks
        
        guimodelling.ModellingCategory(self)
        self.progressBar.setProgress(0.7)
        guifiles.FilesCategory(self)
        self.progressBar.setProgress(0.8)
        #guirender.RenderingCategory(self)
      
        library = gui3d.Category(self, "Library")
        hair_chooser.HairTaskView(library)
        background.BackgroundTaskView(library)
        human_texture.HumanTextureTaskView(library)

        # Load plugins not starting with _    
        self.modules = {}
        for path in glob.glob(join("plugins/",'[!_]*.py')):
            try:
                name, ext = splitext(basename(path))
                module = imp.load_source(name, path)
                self.modules[name] = module
                module.load(self)
            except Exception, e:
                print('Could not load %s' % name)
                print e

        category = gui3d.Category(self, "Help", style=gui3d.CategoryButtonStyle)
        # Help button
        @category.button.event
        def onClicked(event):
          webbrowser.open(os.getcwd()+"/docs/MH_Users_Guide.pdf");
          
        # Exit button
        category = gui3d.Category(self, "Exit", style=gui3d.CategoryButtonStyle)
        @category.button.event
        def onClicked(event):
          self.stop()
          
        self.undoButton = gui3d.Button(self, [650, 508, 9.1], "Undo", style=gui3d.ButtonStyle._replace(width=40, height=16))
        self.redoButton = gui3d.Button(self, [694, 508, 9.1], "Redo", style=gui3d.ButtonStyle._replace(width=40, height=16))
        self.resetButton = gui3d.Button(self, [738, 508, 9.1], "Reset", style=gui3d.ButtonStyle._replace(width=40, height=16))
                                        
        @self.undoButton.event
        def onClicked(event):
            self.app.undo()

        @self.redoButton.event
        def onClicked(event):
            self.app.redo()

        @self.resetButton.event
        def onClicked(event):
            human = self.scene3d.selectedHuman
            human.resetMeshValues()
            human.applyAllTargets(self.progress)
            self.app.categories['Modelling'].tasksByName['Macro modelling'].syncSliders()
            self.app.categories['Modelling'].tasksByName['Macro modelling'].syncStatus()
            self.app.categories['Modelling'].tasksByName['Detail modelling'].syncSliders()
          
        self.globalButton = gui3d.Button(self, [650, 530, 9.2], "Global cam", style=gui3d.ButtonStyle._replace(width=128, height=20))
        self.faceButton = gui3d.Button(self, [650, 555, 9.2], "Face cam", style=gui3d.ButtonStyle._replace(width=128, height=20))
        
        @self.globalButton.event
        def onClicked(event):
          self.app.setGlobalCamera()
          
        @self.faceButton.event
        def onClicked(event):
          self.app.setFaceCamera()

        self.switchCategory("Modelling")

        self.progressBar.setProgress(1.0)
        self.progressBar.hide()
        
        #font = font3d.Font("data/fonts/arial.fnt")
        #font3d.createMesh(self.scene3d, font, "ABCDEFGHIJKLMNOPQRSTUVWXYZ", [60, 540, 9.6]);

    def onStart(self, event):
        self.splash.hide()
        self.scene3d.selectedHuman.applyAllTargets(self.app.progress)
        mh.updatePickingBuffer();

    def onKeyDown(self, event):
        
        # Normalize modifiers
        modifiers = 0
        if (event.modifiers & events3d.KMOD_CTRL) and (event.modifiers & events3d.KMOD_ALT):
            modifiers = events3d.KMOD_CTRL | events3d.KMOD_ALT
        elif event.modifiers & events3d.KMOD_CTRL:
            modifiers = events3d.KMOD_CTRL
        elif event.modifiers & events3d.KMOD_ALT:
            modifiers = events3d.KMOD_ALT
            
        # Normalize key
        key = event.key
        if key in xrange(events3d.SDLK_KP0, events3d.SDLK_KP9 + 1):
            key = events3d.SDLK_0 + key - events3d.SDLK_KP0
        elif key == events3d.SDLK_KP_PERIOD:
            key = events3d.SDLK_PERIOD
        elif key == events3d.SDLK_KP_MINUS:
            key = events3d.SDLK_MINUS
        elif key == events3d.SDLK_KP_PLUS:
            key = events3d.SDLK_PLUS
            
        if (modifiers, key) in self.shortcuts:
            self.shortcuts[(modifiers, key)]()

    # Undo-redo
    def do(self, action):
        if action.do():
            self.undoStack.append(action)
            del self.redoStack[:]
            print("do " + action.name)
            self.scene3d.redraw()

    def did(self, action):
        self.undoStack.append(action)
        del self.redoStack[:]
        print("did " + action.name)
        self.scene3d.redraw()

    def undo(self):
        if self.undoStack:
            action = self.undoStack.pop()
            print("undo " + action.name)
            action.undo()
            self.redoStack.append(action)
            self.scene3d.redraw()

    def redo(self):
        if self.redoStack:
            action = self.redoStack.pop()
            print("redo " + action.name)
            action.do()
            self.undoStack.append(action)
            self.scene3d.redraw()

    # Themes
    def setTheme(self, theme):
        f = open("data/themes/" + theme + ".mht", 'r')

        for data in f.readlines():
            lineData = data.split()

            if len(lineData) > 0:
                if lineData[0] == "version":
                    print("Version " + lineData[1])
                elif lineData[0] == "color":
                    if lineData[1] == "clear":
                        mh.setClearColor(float(lineData[2]), float(lineData[3]), float(lineData[4]), float(lineData[5]))

        self.theme = theme

    def getThemeResource(self, folder, id):
        if '/' in id:
            return id
        if os.path.exists("data/themes/" + self.theme + "/" + folder + "/"+ id):
            return "data/themes/" + self.theme + "/" + folder + "/"+ id
        else:
            return "data/themes/default/" + folder + "/"+ id
      
    # Font resources
    def getFont(self, fontFamily):
        if fontFamily not in self.fonts:
            self.fonts[fontFamily] = font3d.Font("data/fonts/%s.fnt" % fontFamily)
        return self.fonts[fontFamily]

    # Global progress bar
    def progress(self, value):
        self.progressBar.setProgress(value)
        if value <= 0:
            self.progressBar.show()
        elif value >= 1.0:
            self.progressBar.hide()
      
    # Camera's
    def setGlobalCamera(self):
        self.modelCamera.eyeX = 0
        self.modelCamera.eyeY = 0
        self.modelCamera.eyeZ = 60
        self.modelCamera.focusX = 0
        self.modelCamera.focusY = 0
        self.modelCamera.focusZ = 0
  
    def setFaceCamera(self):
        human = self.scene3d.selectedHuman
        headNames = [group.name for group in human.meshData.facesGroups if ("head" in group.name or "jaw" in group.name)]
        self.headVertices, self.headFaces = human.meshData.getVerticesAndFacesForGroups(headNames)
        center = centroid([v.co for v in self.headVertices])
        self.modelCamera.eyeX = center[0]
        self.modelCamera.eyeY = center[1]
        self.modelCamera.eyeZ = 10
        self.modelCamera.focusX = center[0]
        self.modelCamera.focusY = center[1]
        self.modelCamera.focusZ = 0
        human.setPosition([0.0, 0.0, 0.0])
        human.setRotation([0.0, 0.0, 0.0])
        
    # Shortcuts
    def setShortcut(self, modifier, key, method):
        
        shortcut = (modifier, key)
        
        if shortcut in self.shortcuts:
            print 'Shortcut is in use'
            return False
            
        # Remove old entry
        for s, m in self.shortcuts.iteritems():
            if m == method:
                del self.shortcuts[s]
                break
                
        self.shortcuts[shortcut] = method
        
        for shortcut, m in self.shortcuts.iteritems():
            print shortcut, m
        
        return True
        
    def getShortcut(self, method):
        
        for shortcut, m in self.shortcuts.iteritems():
            if m == method:
                return shortcut
    
    # Shortcut methods
    
    def goToModelling(self):
        self.switchCategory("Modelling")
        self.scene3d.redraw()
        
    def goToSave(self):
        self.switchCategory("Files")
        self.switchTask("Save")
        self.scene3d.redraw()
        
    def goToLoad(self):
        self.switchCategory("Files")
        self.switchTask("Load")
        
    def goToExport(self):
        self.switchCategory("Files")
        self.switchTask("Export")
        self.scene3d.redraw()
        
    def goToRendering(self):
        self.switchCategory("Rendering")
        self.scene3d.redraw()
        
    def goToHelp(self):
        webbrowser.open(os.getcwd()+"/docs/MH_Users_Guide.pdf");
          
    def toggleStereo(self):
        stereoMode = mh.cameras[0].stereoMode
        stereoMode += 1
        if stereoMode > 2:
            stereoMode = 0
        mh.cameras[0].stereoMode = stereoMode

        # We need a black background for stereo
        background = self.categories["Modelling"].background
        if stereoMode:
            color = [  0,   0,   0, 255]
            self.categories["Modelling"].anaglyphsButton.setSelected(True)
        else:
            color = [100, 100, 100, 255]
            self.categories["Modelling"].anaglyphsButton.setSelected(False)
        for g in background.mesh.facesGroups:
            g.setColor(color)

        self.scene3d.redraw()
        
    def toggleSolid(self):
        if self.scene3d.selectedHuman.mesh.solid:
            self.scene3d.selectedHuman.mesh.setSolid(0)
        else:
            self.scene3d.selectedHuman.mesh.setSolid(1)
        self.scene3d.redraw()
        
    def saveTarget(self):
        human = self.scene3d.selectedHuman
        algos3d.saveTranslationTarget(human.meshData, "full_target.target")
        print "Full target exported"
        
    def quickExport(self):
        exportPath = mh.getPath('exports')
        if not os.path.exists(exportPath):
            os.makedirs(exportPath)
        mh2obj.exportObj(self.scene3d.selectedHuman.meshData, exportPath + '/quick_export.obj', 'data/3dobjs/base.obj')
        mh2bvh.exportSkeleton(self.scene3d.selectedHuman.meshData, exportPath + '/quick_export.bvh')
        mh2mhx.exportMhx(self.scene3d.selectedHuman.meshData, exportPath + '/quick_export.mhx')
        
    def grabScreen(self):
        grabPath = mh.getPath('grab')
        if not os.path.exists(grabPath):
            os.makedirs(grabPath)
        # TODO: use bbox to choose grab region
        self.scene3d.grabScreen(180, 80, 440, 440, os.path.join(grabPath, 'grab.bmp'))
        
    def subdivide(self):
        print 'subdividing'
        self.scene3d.selectedHuman.subdivide()
        
    # Camera navigation
    def rotateDown(self):
        human = self.scene3d.selectedHuman
        rot = human.getRotation()
        rot[0] += 5.0
        human.setRotation(rot)
        self.scene3d.redraw()
        
    def rotateLeft(self):
        human = self.scene3d.selectedHuman
        rot = human.getRotation()
        rot[1] -= 5.0
        human.setRotation(rot)
        self.scene3d.redraw()
        
    def rotateRight(self):
        human = self.scene3d.selectedHuman
        rot = human.getRotation()
        rot[1] += 5.0
        human.setRotation(rot)
        self.scene3d.redraw()
        
    def rotateUp(self):
        human = self.scene3d.selectedHuman
        rot = human.getRotation()
        rot[0] -= 5.0
        human.setRotation(rot)
        self.scene3d.redraw()
        
    def panUp(self):
        human = self.scene3d.selectedHuman
        trans = human.getPosition()
        trans[1] += 0.05
        human.setPosition(trans)
        self.scene3d.redraw()
                    
    def panDown(self):
        human = self.scene3d.selectedHuman
        trans = human.getPosition()
        trans[1] -= 0.05
        human.setPosition(trans)
        self.scene3d.redraw()      
        
    def panRight(self):
        human = self.scene3d.selectedHuman
        trans = human.getPosition()
        trans[0] += 0.05
        human.setPosition(trans)
        self.scene3d.redraw()
        
    def panLeft(self):
        human = self.scene3d.selectedHuman
        trans = human.getPosition()
        trans[0] -= 0.05
        human.setPosition(trans)
        self.scene3d.redraw()
        
    def zoomOut(self):
        mh.cameras[0].eyeZ += 0.65
        self.scene3d.redraw()
        
    def zoomIn(self):
        mh.cameras[0].eyeZ -= 0.65
        self.scene3d.redraw()
        
    def topView(self):
        self.scene3d.selectedHuman.setRotation([90.0, 0.0, 0.0])
        self.scene3d.redraw()
        
    def frontView(self):
        self.scene3d.selectedHuman.setRotation([0.0, 0.0, 0.0])
        self.scene3d.redraw()
        
    def sideView(self):
        self.scene3d.selectedHuman.setRotation([0.0, 90.0, 0.0])
        self.scene3d.redraw()
        
    def resetView(self):
        self.scene3d.selectedHuman.setPosition([0.0, 0.0, 0.0])
        mh.cameras[0].eyeZ = 60.0
        self.scene3d.redraw()
    
application = MHApplication()
mainScene = application.scene3d # HACK: Don't remove this, it is needed to receive events from C
application.start()

#import cProfile
#cProfile.run('application.start()')
