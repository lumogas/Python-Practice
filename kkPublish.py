# From a script by Julien Segreto
# This script saves a playblast to the proper directory on the Temple project
# You need to have an active viewer window, and your scene needs to meet the 
# right naming conventions, otherwise it won't work.
# !/usr/bin/python
from pymel.core import *
import maya.mel as mel
import os
import sys
import platform

##  VARIABLES  ##

def kkGetVars():
    """
    Gets all the necessary variables to make the other functions work
    """
    # What operating system is this? If it's a Mac, or Windows, set up h264. 
    # Otherwise use jpeg
    if (platform.system() == 'Linux'):
        kCodec = 'jpeg'
    else:
        kCodec = 'H.264'

    # what's the current audio?
    mel.eval("global string $gPlayBackSlider")
    whatSound = mel.eval("timeControl -q -s $gPlayBackSlider")

    # working dir
    kkCurrentScene   = sceneName()

    # output Path
    splitPath     = kkCurrentScene.split("/")
    joinPath      = "/".join(splitPath[0:7])
    whatVersion = splitPath[-1]
    whatVersion = whatVersion.split("_")
    whatVersion = ''.join(whatVersion[-2:-1])
    whatShot = 'v' + splitPath[6][-3:]

    #anim or blocking?
    whatType = splitPath[8:9]
    whatType = whatType[0]
    print whatType

    pathOutput = ('%s/Publish/%s/%s/Media/' 
                  % (joinPath, whatType, whatVersion))
    print pathOutput
    # create Render Anim OR anim folder if not exists
    # check if anim exists - > No then check if Anim exists -> no -> create Anim
    #	########################################################yes -> set pathOutput to Anim
    #######################-> yes -> set pathOutput to anim


    if not os.path.isdir(pathOutput):
        sysFile( pathOutput, makeDir=True )

    # camera name
    cameraName    = getCurrentCamera()

    # scene name
    kkSceneName     = kkCurrentScene.split('/')
    kkSceneName     = kkSceneName[-1] # take out scene name from path
    kkSceneName     = kkSceneName[:-3] # get rid of extension
    kkSceneName = "_".join(kkSceneName.split('_')[:5]) # get rid of the shit

    # get time range max
    maxTime       = playbackOptions( q = True, maxTime   = True )

    # playblast variable
    pb100         = pathOutput + kkSceneName + ".mov"

    #print pathToMedia
    print joinPath
    print kkSceneName
    print pathOutput

    return pb100, kCodec, whatSound

## FUNCTIONS ##

def getCurrentCamera():
    '''
    gets the current maya viewport camera
    '''
    pan = getPanel(wf=True)
    cam = modelPanel(pan, q=True, camera=True)
    return cam

def kkCapture():
    ## CALL FUNCTIONS ##
    x = kkGetVars()
    # save playblast (100% and 50%)
    pb100 = x[0]
    kCodec = x[1]
    whatSound = x[2]
    playblast( format="qt", filename= pb100, percent=100, viewer= True, 
               showOrnaments=True, forceOverwrite=True, compression= kCodec,
               quality= 100, widthHeight= (1920, 1080), sound=whatSound)

def kkBlast():
    """
    This makes sure all the useless elements are hidden from view 
    during a playblast. It then makes visible everything that was active 
    before.
    """
    # Mel command to query gpu caches... 
    # modelEditor -q -queryPluginObjects gpuCacheDisplayFilter modelPanel4;

    # Mel command to hide gpu caches...
    # modelEditor -e -pluginObjects gpuCacheDisplayFilter false modelPanel4;

    # Python command that turns on the caches (here just in case I ever 
    # figure it out...
    # modelEditor( modelPanel='modelPanel4', 
    # pluginObjects= ['gpuCacheDisplayFilter', True] )
    # First, the variables
    # menu items - what can be shown?
    kkPanelItems =  ["nurbsCurves", "nurbsSurfaces", "polymeshes" , 
                     "subdivSurfaces", "planes", "lights", "cameras", 
                     "joints", "ikHandles", "deformers","dynamics", 
                     "fluids", "hairSystems", "follicles", "nCloths", 
                     "nRigids","dynamicConstraints", "locators", 
                     "dimensions", "pivots", "handles","textures", 
                     "strokes", "manipulators", "cv", "hulls", "grid", 
                     "hud", "sel"]

    kkCameraItems = ['displayFieldChart','displayFilmGate','displayGateMask',
                     'displayResolution','displaySafeAction',
                     'displaySafeTitle', 'overscan']

    kkPanelStatus = []
    kkCamStatus = []
    kkBlastCameraStatus = [False, False, False, False, False, False, '1.0']

    kkCurrentPanel = getPanel(wf=True)
    kkCurrentCam = getCurrentCamera()

    #record all the display status for each item in the list
    for kkItem in kkPanelItems:
        kkCommand = ('modelEditor( kkCurrentPanel, query = True, %s = True)' 
                     % (kkItem))
        kkPanelStatus.append(eval(kkCommand))
        print kkCommand

    for item in kkCameraItems:
        kkCommand = 'camera(kkCurrentCam, query = True, %s = True)' % (item)
        kkCamStatus.append(eval(kkCommand))

    # separate Mel command for the gpu caches, because you can't figure out 
    # the pymel for it...
    kkMelQuery = ('modelEditor -q -queryPluginObjects ' + 
                  'gpuCacheDisplayFilter %s' % (kkCurrentPanel));
    kkMelStatus = mel.eval(kkMelQuery)

    # We now have a list of everything that's visible. To blast,first we 
    # hide everything...
    modelEditor( kkCurrentPanel, edit = True, alo = False )

    #now show only meshes ( and caches, if visible)
    modelEditor( kkCurrentPanel, edit = True, polymeshes = True )
    kkMelEdit = ('modelEditor -e -pluginObjects gpuCacheDisplayFilter %s %s' 
                 % (kkMelStatus, kkCurrentPanel));
    mel.eval(kkMelEdit)

    for kkItem, kkSetting in zip(kkCameraItems, kkBlastCameraStatus):
        kkCommand = ('camera(kkCurrentCam, edit = True, %s = %s)' % 
                     (kkItem, kkSetting))
        eval(kkCommand)

    kkCapture()

    # Now restore visibility to all hidden items, so everything goes back to 
    # what it was before the playblast.

    for kkPanelItem, kkStatus in zip(kkPanelItems,kkPanelStatus):
        kkCommand = ('modelEditor( kkCurrentPanel, edit = True, %s = %s)' % 
                     (kkPanelItem, str(kkStatus)))
        eval(kkCommand)

    for kkItem, kkSetting in zip(kkCameraItems, kkCamStatus):
        kkCommand = ('camera(kkCurrentCam, edit = True, %s = %s)' % 
                     (kkItem, kkSetting))
        eval(kkCommand)
