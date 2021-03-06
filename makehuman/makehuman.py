#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MakeHuman python entry-point.

**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Glynn Clements, Joel Palmius, Jonas Hauquier

**Copyright(c):**      MakeHuman Team 2001-2014

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

This file starts the MakeHuman python application.
"""

from __future__ import absolute_import  # Fix 'from . import x' statements on python 2.6
import sys
import os
import re
import subprocess

## Version information #########################################################
version = [1, 0]                        # Major and minor version number
release = False                         # False for nightly
versionSub = "Alpha 8 RC"               # Short version description
meshVersion = "hm08"                    # Version identifier of the basemesh

_versionStr = ".".join( [str(v) for v in version] ) + " " + versionSub
################################################################################

def isRelease():
    """
    True when release version, False for nightly (dev) build
    """
    return release

def isBuild():
    """
    Determine whether the app is frozen using pyinstaller/py2app.
    Returns True when this is a release or nightly build (eg. it is build as a
    distributable package), returns False if it is a source checkout.
    """
    return getattr(sys, 'frozen', False)

def getVersion():
    """
    Comparable version as list of ints
    """
    return version

def getVersionStr(verbose=True):
    """
    Verbose version as string, for displaying and information
    """
    if isRelease():
        return _versionStr
    else:
        if 'SVNREVISION' not in os.environ:
            get_svn_revision()
        result = _versionStr + " (r" + os.environ['SVNREVISION'] + ")"
        if verbose:
            result += (" [%s]" % os.environ['SVNREVISION_SOURCE'])
        return result

def getShortVersion():
    """
    Useful for tagging assets
    """
    return versionSub.replace(' ', '_').lower()

def getBasemeshVersion():
    """
    Version of the human basemesh
    """
    return meshVersion

def get_revision_svn_info():
    # Try getting svn revision by calling svn info (will only work in linux
    #  and windows where sliksvn is installed)
    output = subprocess.Popen(["svn","info","."], stdout=subprocess.PIPE, stderr=sys.stderr).communicate()[0]
    for line in output.splitlines():
        key, value = line.split(':', 1)
        if key.strip().lower() == 'revision':
            return value.strip()
    raise RuntimeError("revision not found in 'svn info .' output")

def get_revision_entries(folder=None):
    # First fallback: try to parse the entries file manually
    if folder:
        scriptdir = os.path.abspath(folder)
    else:
        scriptdir = os.path.dirname(os.path.abspath(__file__))
    svndir = os.path.join(scriptdir,'.svn')
    entriesfile = os.path.join(svndir,'entries')
    entries = open(entriesfile, 'r').read()
    result = re.search(r'dir\n(\d+)\n',entries)
    output = result.group(1)
    if not output:
        if not folder:
            # Try going up one folder
            return get_revision_entries(os.path.join(scriptdir, '..'))
        raise RuntimeError("revision not found in 'entries' file")
    return output

def get_revision_pysvn():
    # The following only works if pysvn is installed. We'd prefer not to use this since it's very slow.
    # It was taken from this stackoverflow post:
    # http://stackoverflow.com/questions/242295/how-does-one-add-a-svn-repository-build-number-to-python-code
    import pysvn
    repo = "."
    rev = pysvn.Revision( pysvn.opt_revision_kind.working )
    client = pysvn.Client()
    info = client.info2(repo,revision=rev,recurse=False)
    output = format(str(info[0][1].rev.number))
    return output

def get_revision_file():
    # Default fallback to use if we can't figure out SVN revision in any other
    # way: Use this file's svn revision.
    pattern = re.compile(r'[^0-9]')
    return pattern.sub("", "$Revision$")

def get_svn_revision_1():
    svnrev = None

    try:
        svnrev = get_revision_svn_info()
        os.environ['SVNREVISION_SOURCE'] = "svn info command"
        return svnrev
    except Exception as e:
        print >> sys.stderr,  "NOTICE: Failed to get svn version number from command line: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    try:
        svnrev = get_revision_entries()
        os.environ['SVNREVISION_SOURCE'] = "entries file"
        return svnrev
    except Exception as e:
        print >> sys.stderr,  "NOTICE: Failed to get svn version from file: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    try:
        svnrev = get_revision_pysvn()
        os.environ['SVNREVISION_SOURCE'] = "pysvn"
        return svnrev
    except Exception as e:
        print >> sys.stderr,  "NOTICE: Failed to get svn version number using pysvn: " + format(str(e)) + " (This is just a head's up, not a critical error)"

    print >> sys.stderr,  "NOTICE: Using SVN rev from file stamp. This is likely outdated, so the number in the title bar might be off by a few commits."
    svnrev = get_revision_file()
    os.environ['SVNREVISION_SOURCE'] = "approximated from file stamp"
    return svnrev

def get_svn_revision():
    #[BAL 07/13/2013] use the VERSION file if it exists. This is created and managed using pyinstaller.
    import getpath
    versionFile = getpath.getSysDataPath("VERSION")
    if os.path.exists(versionFile):
        version_ = open(versionFile).read().strip()
        print >> sys.stderr,  "data/VERSION file detected using value from version file: %s" % version_
        os.environ['SVNREVISION'] = version_
        os.environ['SVNREVISION_SOURCE'] = "data/VERSION static revision data"
    else:
        print >> sys.stderr,  "NO VERSION file detected retrieving revision info from SVN"
        # Set SVN rev in environment so it can be used elsewhere
        svnrev = get_svn_revision_1()
        print >> sys.stderr,  "Detected SVN revision: " + svnrev
        os.environ['SVNREVISION'] = svnrev
    
def recursiveDirNames(root):
    pathlist=[]
    #root=os.path.dirname(root)
    for filename in os.listdir(root):
        path=os.path.join(root,filename)
        if not (os.path.isfile(path) or filename=="." or filename==".." or filename==".svn"):
            pathlist.append(path)
            pathlist = pathlist + recursiveDirNames(path) 
    return(pathlist)

def set_sys_path():
    """
    Append local module folders to python search path.
    """
    #[BAL 07/11/2013] make sure we're in the right directory
    if sys.platform != 'darwin':
        os.chdir(sys.path[0])
    syspath = ["./", "./lib", "./apps", "./shared", "./apps/gui","./core"]
    syspath.extend(sys.path)
    sys.path = syspath

stdout_filename = None
stderr_filename = None

def get_platform_paths():
    global stdout_filename, stderr_filename
    import getpath

    home = getpath.getPath()

    if sys.platform == 'win32':
        stdout_filename = os.path.join(home, "python_out.txt")
        stderr_filename = os.path.join(home, "python_err.txt")

    elif sys.platform.startswith("darwin"):
        stdout_filename = os.path.join(home, "makehuman-output.txt")
        stderr_filename = os.path.join(home, "makehuman-error.txt")

def redirect_standard_streams():
    if stdout_filename:
        sys.stdout = open(stdout_filename, "w")
    if stderr_filename:
        sys.stderr = open(stderr_filename, "w")

def close_standard_streams():
    sys.stdout.close()
    sys.stderr.close()

def make_user_dir():
    """
    Make sure MakeHuman folder storing per-user files exists.
    """
    import getpath
    userDir = getpath.getPath()
    if not os.path.isdir(userDir):
        os.makedirs(userDir)
    userDataDir = getpath.getPath('data')
    if not os.path.isdir(userDataDir):
        os.makedirs(userDataDir)

def init_logging():
    import log
    log.init()
    log.message('Initialized logging')
    
def debug_dump():
    try:
        import debugdump
        debugdump.dump.reset()
    except debugdump.DependencyError as e:
        print >> sys.stderr,  "Dependency error: " + format(str(e))
        import log
        log.error("Dependency error: %s", e)
        sys.exit(-1)
    except Exception as _:
        import log
        log.error("Could not create debug dump", exc_info=True)

def parse_arguments():
    if len(sys.argv) < 2:
        return dict()

    import argparse    # requires python >= 2.7
    parser = argparse.ArgumentParser()

    # optional arguments
    parser.add_argument('-v', '--version', action='version', version=getVersionStr())
    parser.add_argument("--noshaders", action="store_true", help="disable shaders")
    parser.add_argument("--nomultisampling", action="store_true", help="disable multisampling (used for anti-aliasing and alpha-to-coverage transparency rendering)")
    parser.add_argument("--debugopengl", action="store_true", help="enable OpenGL error checking and logging (slow)")
    parser.add_argument("--fullloggingopengl", action="store_true", help="log all OpenGL calls (very slow)")
    parser.add_argument("--debugnumpy", action="store_true", help="enable numpy runtime error messages")
    if not isRelease():
        parser.add_argument("-t", "--runtests", action="store_true", help="run test suite (for developers)")

    # optional positional arguments
    parser.add_argument("mhmFile", default=None, nargs='?', help=".mhm file to load (optional)")

    argOptions = vars(parser.parse_args())
    return argOptions

def main():
    try:
        set_sys_path()
        make_user_dir()
        get_platform_paths()
        redirect_standard_streams()
        if not isRelease():
            get_svn_revision()
        os.environ['MH_VERSION'] = getVersionStr()
        args = parse_arguments()
        init_logging()
    except Exception as e:
        print >> sys.stderr,  "error: " + format(str(e))
        import traceback
        bt = traceback.format_exc()
        print >> sys.stderr, bt
        return

    # Pass release info to debug dump using environment variables
    os.environ['MH_FROZEN'] = "Yes" if isBuild() else "No"
    os.environ['MH_RELEASE'] = "Yes" if isRelease() else "No"

    debug_dump()
    from core import G
    G.args = args

    # Set numpy properties
    if not args.get('debugnumpy', False):
        import numpy
        # Suppress runtime errors
        numpy.seterr(all = 'ignore')

    # Here pyQt and PyOpenGL will be imported
    from mhmain import MHApplication
    application = MHApplication()
    application.run()

    #import cProfile
    #cProfile.run('application.run()')

    close_standard_streams()

if __name__ == '__main__':
    main()
