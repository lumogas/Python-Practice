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
import ntpath

##  VARIABLES  ##
def kkExtract(x,y):
    """
    Used to get chunks of any strings split by underscores. The first 
    argument is the string, the other is the index to return
    For example: kkExtract('One_Two',0) would return 'One'
    """
    result = x.split('_')[y]
    return result

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
    kkSceneName = ntpath.basename(kkCurrentScene)
    kkSceneNameClean = kkSceneName[:-3] # with the extension removed

    # first three elements of the scene name are the shot's id
    kkShotName = '_'.join(kkSceneNameClean.split('_')[:3]) 

    kkVersionNumber = kkExtract( kkSceneNameClean, 4)

    #anim or blocking?
    kkStageName = kkExtract( kkSceneNameClean, 3)
    kkStageNameCap = kkStageName.title() # capitalize for the path output

    kkArtistName = kkExtract( kkSceneNameClean, -1)

    # output Path
    splitPath     = kkCurrentScene.split("/")
    joinPath      = "/".join(splitPath[0:7])
    pathOutput = ('%s/Publish/%s/%s/Media/' 
                  % (joinPath, kkStageNameCap, kkVersionNumber))
    pathSceneOutput = ('%s/Publish/%s/%s/Scenes/' 
                  % (joinPath, kkStageNameCap, kkVersionNumber))

    # blast name
    kkBlastName = "%s_%s_%s" % (kkShotName, kkStageName, kkVersionNumber)
    # get time range max
    maxTime       = playbackOptions( q = True, maxTime   = True )

    # playblast variable
    pb100         =  "%s%s.mov" % (pathOutput ,kkBlastName)

    return (pb100, kCodec, whatSound, pathOutput, pathSceneOutput, 
            kkSceneName, kkBlastName, kkArtistName, kkStageName)

## FUNCTIONS ##

def kkCapitalize(x):
    """Switches the first character in the string to a capital"""
    x = x[0].upper() + x[1:]
    return x

def kkRunDict(x):
    """Iterates through a dict, sets the values for the key"""
    for key, value in x.iteritems():
        key = kkCapitalize(key)
        kkMelCommand = "set%s(%s)" % (key, value)
        mel.eval(kkMelCommand)

def kkCreateFolders():
    """
    This creates the necessary folders for the playblast and the spare copy
    of the scene, and makes the spare copy of the scene itself. 
    """
    pathOutput = kkGetVars()[3]
    pathSceneOutput = kkGetVars()[4]
    kkSceneName = kkGetVars()[5]
    kkCurrentScene = sceneName()
    print pathOutput
    print pathSceneOutput
    print kkSceneName
    # This creates a Scenes folder in Publish
    if not os.path.isdir(pathSceneOutput):
        sysFile( pathSceneOutput, makeDir=True )    

    # This creates a copy of the scene in 
    # Publish/'CurrentTask'/'version'/Scenes
    kkCopySceneTarget = '%s/%s' % (pathSceneOutput ,kkSceneName)
    sysFile( kkCurrentScene, copy = kkCopySceneTarget )

    # create Anim folder if it doesn't exist
    if not os.path.isdir(pathOutput):
        sysFile( pathOutput, makeDir=True )

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
    kkCreateFolders()
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

    kkHudElements = ['animationDetailsVisibility', 'cameraNamesVisibility', 
                     'currentContainerVisibility', 'currentFrameVisibility',
                     'focalLengthVisibility', 'frameRateVisibility', 
                     'hikDetailsVisibility', 'objectDetailsVisibility',
                     'particleCountVisibility', 'polyCountVisibility',
                     'sceneTimecodeVisibility', 'selectDetailsVisibility',
                     'viewAxisVisibility', 'viewportRendererVisibility']

    kkHudStartSettings = {}

    kkBlastHudSettings = {'currentFrameVisibility':1,
                          'focalLengthVisibility':1 }

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

    for item in kkHudElements:
        kkMelCommand = "optionVar -q %s" % (item)
        kkHudStartSettings[item] = mel.eval(kkMelCommand)
        item = kkCapitalize(item)
        kkMelCommand = "set%s(0)" % (item)
        mel.eval(kkMelCommand)

    # separate Mel command for the gpu caches, because you can't figure out 
    # the pymel for it...
    kkMelQuery = ('modelEditor -q -queryPluginObjects ' + 
                  'gpuCacheDisplayFilter %s' % (kkCurrentPanel));
    kkMelStatus = mel.eval(kkMelQuery)

    # We now have a list of everything that's visible. To blast,first we 
    # hide everything...
    modelEditor( kkCurrentPanel, edit = True, alo = False )

    #now show only meshes, turn off selection highlighting ( and show 
    #caches, if visible)
    modelEditor( kkCurrentPanel, edit = True, polymeshes = True, 
                 sel = False, twoSidedLighting = True )
    kkMelEdit = ('modelEditor -e -pluginObjects gpuCacheDisplayFilter %s %s' 
                 % (kkMelStatus, kkCurrentPanel));
    mel.eval(kkMelEdit)

    for kkItem, kkSetting in zip(kkCameraItems, kkBlastCameraStatus):
        kkCommand = ('camera(kkCurrentCam, edit = True, %s = %s)' % 
                     (kkItem, kkSetting))
        eval(kkCommand)

    kkRunDict(kkBlastHudSettings) # Show frame number and focal length
    kkGroupName = kkCreateText() # put in the name and artist

    kkCapture() # do the playblast

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

    kkRunDict(kkHudStartSettings)

    # And finally, delete the temp text node, and its shaders
    delete(kkGroupName)
    mel.eval('MLdeleteUnused')
    
def kkMakeText(x,y):
    """
    Does the actual creation of the text geometry. Needs the text content to 
    be created, and the name of the group it will be parented under. 
    """
    kkTextName = x
    kkGroupName = y
    kkTextNameShape = x + 'Shape'
    group (em = True, n = kkGroupName)
    textCurves( n= x, f='DejaVu-Sans', t= kkTextName )

    for kkItem in (listRelatives(kkTextNameShape)):
        kkMelCommand = ('planarSrf -name %s -ch 1 -tol 0.01 -o on -po 1 %s' %
                        (kkItem, kkItem))
        kkPolyLetter = mel.eval(kkMelCommand)
        parent (kkPolyLetter, kkGroupName)
    delete(kkTextNameShape) #We don't need the curves, so we delete them
    scale(kkGroupName, [0.5,0.5,0.5]) #size them down, so they fit


def kkCreateText():
    """
    Creates a poly text version of the scene name, and another for the 
    artist's name.
    """
    x = kkGetVars()
    x = x[6],x[7]
    y = ['kkBottom','kkTop']
    z = [-6.925, 6.624] #the vertical distances, to put them at the edges.
    kkGroupName = 'kkTextBlock_GRP'

    group( em=True, n = kkGroupName)

    for kkName, kkGroup in zip(x,y):
        kkMakeText(kkName, kkGroup)    

    #center it, move it down    
    for kkItem, kkPositionY in zip(y,z):
        kkSize = exactWorldBoundingBox( kkItem)
        kkPosnX = ((kkSize[3] - kkSize[0]) / 2) * -1 
        move( kkItem, [ kkPosnX, kkPositionY, 0]) 
        parent(kkItem, kkGroupName)

    # create and assign a white surface shader to the geo to make it visible
    kkShaderName = "%s_shader" % (kkGroupName)
    kkShader = shadingNode('surfaceShader', n = kkShaderName, asShader=True)
    kkShader.outColor.set(1,1,1)
    kkSg = sets(renderable=1,noSurfaceShader=1,empty=1,
                name= kkShader + '_SG')
    connectAttr( kkShaderName + ".outColor",kkSg + ".surfaceShader",force=1)
    sets( kkSg, edit=1, forceElement= kkGroupName )

    return kkPutOnCamera(kkGroupName)


def kkPutOnCamera(x):
    """ 
    Grabs the text that has been created, groups it under a parent called
    kkTextBlockOffset_GRP, then places it on the camera, moving it 0.05 
    units further than the camera's near clipping plane, and scaling it 
    accordingly with an expression, so it stays the right size.
    """
    kkGroupName = '%sOffset_GRP' % (kkExtract(x,0))
    kkWhatCamera = getCurrentCamera()
    kkCamShape = [y for y  in listRelatives(kkWhatCamera) if 
                  (nodeType(y) == 'camera')]
    print kkCamShape
    kkBuffer = "%s.nearClipPlane" % (kkCamShape[0])
    kkOffset = -0.05
    kkNearClip = (getAttr(kkBuffer) * -1) + kkOffset

    group( em=True, n = kkGroupName)
    parent(x, kkGroupName)
    parentConstraint (kkWhatCamera, kkGroupName)
    kkExpString = (("float $d = %s.horizontalFilmAperture;\n" + 
                   "float $f = %s.focalLength;\n" +
                   "float $ratio = $d / (2 * $f);\n" +
                   "float $a = 2 * atan($ratio); // angle in radians\n" +
                   "$a = rad_to_deg($a); // angle in degrees\n" +
                   "$a = $a/2;\n" +
                   "float $z = abs(kkTextBlock_GRP.translateZ);\n" +
                   "float $kkTan = tand($a);\n" +
                   "$kkScale = $kkTan * $z;\n" +
                   "$kkScale = $kkScale * 2;\n" +
                   "kkTextBlock_GRP.scaleX = $kkScale;\n" +
                   "kkTextBlock_GRP.scaleY = $kkScale;\n") %
                   (kkWhatCamera, kkWhatCamera))

    expression( n = 'kkText_exp', s= kkExpString )
    move ('kkTextBlock_GRP', [0,0,kkNearClip], ls = True)
    return kkGroupName

