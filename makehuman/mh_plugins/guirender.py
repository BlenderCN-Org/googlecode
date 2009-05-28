""" 
Class for handling Render mode in the GUI.

===========================  ===============================================================  
Project Name:                **MakeHuman**                                                  
Module File Location:        mh_plugins/guirender.py                                          
Product Home Page:           http://www.makehuman.org/                                      
SourceForge Home Page:       http://sourceforge.net/projects/makehuman/                     
Authors:                     Manuel Bastioni                                            
Copyright(c):                MakeHuman Team 2001-2008                                       
Licensing:                   GPL3 (see also http://makehuman.wiki.sourceforge.net/Licensing)
Coding Standards:            See http://makehuman.wiki.sourceforge.net/DG_Coding_Standards  
===========================  ===============================================================  

This module implements the 'guirender' class structures and methods to support GUI 
Render mode operations.
Render mode is invoked by selecting the Render mode icon from the main GUI control 
bar at the top of the screen. 
While in this mode, user actions (keyboard and mouse events) are passed into 
this class for processing. Having processed an event this class returns control to the 
main OpenGL/SDL/Application event handling loop.  

"""

__docformat__ = 'restructuredtext'

import files3d, gui3d, events3d
import mh2povray
import mh2renderman

class RenderingCategory(gui3d.Category):
  def __init__(self, parent):
    gui3d.Category.__init__(self, parent, "Rendering", "data/images/button_render.png")
    
    aqsis = gui3d.TaskView(self, "Aqsis",  "data/images/button_aqsis.png")
    @aqsis.event
    def onShow(event):
      pass
    @aqsis.event
    def onHide(event):
      pass
    @aqsis.button.event
    def onClicked(event):
      mh2renderman.saveScene(self.app.scene3d, "scena.rib", "renderman_output", "aqsis")
      
    pixie = gui3d.TaskView(self, "Pixie",  "data/images/button_pixie.png")
    @pixie.event
    def onShow(event):
      pass
    @pixie.event
    def onHide(event):
      pass
    @pixie.button.event
    def onClicked(event):
      mh2renderman.saveScene(self.app.scene3d, "scena.rib", "renderman_output", "pixie")
      
    povray = gui3d.TaskView(self, "Povray",  "data/images/button_povray.png")
    @povray.event
    def onShow(event):
      pass
    @povray.event
    def onHide(event):
      pass
    @povray.button.event
    def onClicked(event):
      reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
      for obj in self.app.scene3d.objects:
          # print "POV-Ray Export test: ", obj.name
          # Only process the humanoid figure
          if obj.name == "base.obj":
              cameraData = self.app.scene3d.getCameraSettings()
              mh2povray.povrayExport(obj, cameraData)
          
  def onShow(self, event):
    self.setFocus()
    gui3d.Category.onShow(self, event)