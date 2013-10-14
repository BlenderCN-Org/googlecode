# -*- mode: python -*-
import sys
import subprocess
import zipfile
import os
import os.path

sys.path = sys.path + ['.']
import makehuman

def SvnInfo():
    import makehuman
    return makehuman.get_svn_revision_1()

def get_plugin_files():
    """
    Returns all python modules (.py) and python packages (subfolders containing 
    a file called __init__.py) in the plugins/ folder.
    """
    import glob
    # plugin modules
    pluginModules = glob.glob(os.path.join("plugins/",'[!_]*.py'))

    # plugin packages
    for fname in os.listdir("plugins/"):
        if fname[0] != "_":
            folder = os.path.join("plugins", fname)
            if os.path.isdir(folder) and ("__init__.py" in os.listdir(folder)):
                pluginModules.append(os.path.join(folder, "__init__.py"))

    return pluginModules

SVNREV = SvnInfo()
VERSION= makehuman.getVersionStr(verbose=False)
VERSION_FN= str(SVNREV)

### Write VERSION file
vfile = open("VERSION","w")
vfile.write(SVNREV)
vfile.close()

###COMPILE TARGETS
try:
    subprocess.check_call(["python","compile_targets.py"])
except subprocess.CalledProcessError:
    print "check that compile_targets.py is working correctly"
    sys.exit(1)

###COMPILE MODELS
try:
    subprocess.check_call(["python","compile_models.py"])
except subprocess.CalledProcessError:
    print "check that compile_models.py is working correctly"
    sys.exit(1)

a = Analysis(['makehuman.py'] + get_plugin_files(),
             pathex=['lib','core','shared','apps','apps/gui', 'plugins'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None
             )

##### include mydir in distribution #######
def extra_datas(mydir):
    def rec_glob(p, files):
        import os
        import glob
        for d in glob.glob(p):
            if os.path.isfile(d):
                files.append(d)
            rec_glob("%s/*" % d, files)
    files = []
    rec_glob("%s/*" % mydir, files)
    extra_datas = []
    for f in files:
        if mydir == 'data' and f.endswith(".target"):
            print "skipping %s" % f
        else:
            extra_datas.append((f, f, 'DATA'))

    return extra_datas
###########################################

# append all of our necessary subdirectories
EXTRA_DATA_PATHS = ['data', 'plugins', 'tools', 'utils', 'icons']
#EXTRA_DATA_PATHS += ['lib', 'core', 'shared', 'apps', 'qt_menu.nib']
for p in EXTRA_DATA_PATHS:
    a.datas += extra_datas(p)


### Build
pyz = PYZ(a.pure)
if sys.platform == 'darwin':
    # MAC OSX
    exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='makehuman',
          debug=False,
          strip=None,
          upx=False,
          console=False )
    coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=None,
        upx=True,
        name='makehuman')
    app = BUNDLE(coll,
        name='MakeHuman.app',
        icon='icons/makehuman.icns')
    if os.path.exists(os.path.join("dist","MakeHuman.dmg")):
        os.remove(os.path.join("dist","MakeHuman.dmg"))
    subprocess.check_call(["hdiutil","create","dist/MakeHuman.dmg","-srcfolder","dist/MakeHuman.app","-volname","'MakeHuman for Mac OS X'"])
        
elif sys.platform == 'win32':
    # WINDOWS
    exe = EXE(pyz,
        a.scripts,
        exclude_binaries=True,
        name='makehuman.exe',
        debug=False,
        strip=None,
        upx=True,
        console=False )
    coll = COLLECT(exe,
        a.binaries,
        a.zipfiles,
        a.datas,
        strip=None,
        upx=True,
        name='makehuman')
    target_dir = os.path.join('dist','makehuman')
    zip = zipfile.ZipFile('dist/makehumansvn-%s-win32.zip' % VERSION_FN, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zip.write(fn, fn[rootlen:])                           
        
os.remove(os.path.join("core","VERSION"))
