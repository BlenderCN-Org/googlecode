#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers, Glynn Clements

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

Utility module for finding the user home path.
"""

import sys
import os

if sys.platform == 'win32':
    import _winreg

def getPath(type):
    if isinstance(type, (str, unicode)):
        typeStr = str(type)
    elif type is None:
        typeStr = ""
    else:
        raise TypeError("String expected")

    if sys.platform == 'win32':
        keyname = r'Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders'
        name = 'Personal'
        k = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, keyname)
        value, type = _winreg.QueryValueEx(k, 'Personal')
        if type == _winreg.REG_EXPAND_SZ:
            path = _winreg.ExpandEnvironmentStrings(value)
        elif type == _winreg.REG_SZ:
            path = value
        else:
            raise RuntimeError("Couldn't determine user folder")

        if typeStr == "exports":
            path += u"\\makehuman\\exports\\"
        elif typeStr == "models":
            path += u"\\makehuman\\models\\"
        elif typeStr == "grab":
            path += u"\\makehuman\\grab\\"
        elif typeStr == "render":
            path += u"\\makehuman\\render\\"
        elif typeStr == "scenes":
            path += u"\\makehuman\\scenes\\"
        elif typeStr == "":
            path += u"\\makehuman\\"
        else:
            raise ValueError("Unknown value '%s' for getPath()!" % typeStr)
    else:
        path = os.path.expanduser('~')
        if sys.platform.startswith("darwin"): 
            path = os.path.join(path,"Documents")
            path = os.path.join(path,"MakeHuman")
        else:
            path = os.path.join(path,"makehuman")

        if typeStr == "exports":
            path += "/exports/"
        elif typeStr == "models":
            path += "/models/"
        elif typeStr == "grab":
            path += "/grab/"
        elif typeStr == "render":
            path += "/render/"
        elif typeStr == "scenes":
            path += "/scenes/"
        elif typeStr == "":
            path += "/"
        else:
            raise ValueError("Unknown property '%s' for getPath()!" % typeStr)

    return path

def getSysDataPath(subPath = ""):
    """
    Path to the data folder that is installed with MakeHuman system-wide.
    """
    if subPath:
        return os.path.join("data/", subPath)
    else:
        return "data/"

def getSysPath(subPath):
    """
    Path to the system folder where MakeHuman is installed (it is possible that 
    data is stored in another path).
    """
    if subPath:
        return os.path.join(subPath)
    else:
        return os.path.join(".")


def _allnamesequal(name):
    return all(n==name[0] for n in name[1:])

def commonprefix(paths, sep='/'):
    """
    Implementation of os.path.commonprefix that works as you would expect.
    
    Source: http://rosettacode.org/wiki/Find_Common_Directory_Path#Python
    """
    from itertools import takewhile
    
    bydirectorylevels = zip(*[p.split(sep) for p in paths])
    return sep.join(x[0] for x in takewhile(_allnamesequal, bydirectorylevels))

def isSubPath(subpath, path):
    """
    Verifies whether subpath is within path.
    """
    subpath = os.path.normpath(os.path.realpath(subpath))
    path = os.path.normpath(os.path.realpath(path))
    return commonprefix([subpath, path]) == path
