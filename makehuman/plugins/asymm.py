#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d
import os
import random
import algos3d


class AsymmTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Asymm', category.app.getThemeResource('images', 'button_asymm.png'), category.app.getThemeResource('images', 'button_asymm_on.png'))
        self.asymmFaceSlider = gui3d.Slider(self,  position=[20, 150, 9.3], value=0.5, label="Face asymmetry")

        @self.asymmFaceSlider.event
        def onChange(value):
            self.faceAsymm(value)
            self.applyAsymm()

        self.faceAsymmDetails = {}
        self.facePath = "data/targets/asym/face/"

    def faceAsymmReset(self):
        for k,v in self.faceAsymmDetails.items():
            algos3d.loadTranslationTarget(self.app.scene3d.selectedHuman.meshData, k, -v, update=1, calcNorm=0)
            self.app.scene3d.selectedHuman.targetsDetailStack[k] = 0
            self.faceAsymmDetails[k] = 0
        
    def faceAsymm(self, value):
        
        self.faceAsymmReset()
        asymmZones = set()
        targetsList = os.listdir(self.facePath)
        for t in targetsList:
            if os.path.isfile(os.path.join(self.facePath, t)):
                nameData = t.split("-")
                asymmZones.add(nameData[1]+"-"+ nameData[2])
        
        for t in asymmZones:
            asymmType = random.randint(1,2) #1 = left, 2 = right
            asymmValue = random.random()* value
            a = self.facePath+"asym-"+t+"-"+str(asymmType)+".target"
            self.faceAsymmDetails[a] = asymmValue

    def applyAsymm(self):
        
        for k,v in self.faceAsymmDetails.items():
            algos3d.loadTranslationTarget(self.app.scene3d.selectedHuman.meshData, k, v, update=1, calcNorm=0)
            self.app.scene3d.selectedHuman.targetsDetailStack[k] = v
        self.app.scene3d.selectedHuman.meshData.update()

def load(app):
    category = app.getCategory('Advanced','button_advance.png','button_advance_on.png')
    taskview = AsymmTaskView(category)
    print 'Asymm loaded'




