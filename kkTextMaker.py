from pymel.core import *
import ntpath
import kkPublish

def kkExtract(x,y):
    """
    Used to get the names of the scene's component parts
    """
    result = x.split('_')[y]
    return result

def kkGetVars():
    """
    Gets the name of the scene, the version, the stage and the artist
    """
    kkCurrentScene   = sceneName()
    # trim the .ma extension
    kkSceneName = ntpath.basename(kkCurrentScene)[:-3]
    # first three elements of the scene name are the shot's id
    kkShotName = '_'.join(kkSceneName.split('_')[:3]) 
    kkStageName = kkExtract( kkSceneName, 3)
    kkArtistName = kkExtract( kkSceneName, -1)
    kkVersionNumber = kkExtract( kkSceneName, 4)
    kkBottomText = "%s_%s_%s" % (kkShotName, kkStageName, kkVersionNumber)

    return kkBottomText, kkArtistName

def kkMakeText(x,y):
    """
    Does the actual creation of the text geometry. Needs the text content to 
    be created, and the name of the group it will be put under. 
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
    delete(kkTextNameShape)
    scale(kkGroupName, [0.5,0.5,0.5])

#return kkCurrentScene

def kkCreateText():
    """
    Creates a poly text version of the scene name, and another for the 
    artist's name.
    """
    x = kkGetVars()
    y = ['kkBottom','kkTop']
    z = [-6.925, 6.624]
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
    kkPutOnCamera(kkGroupName)


def kkPutOnCamera(x):
    kkGroupName = 'kkTextBlockOffset_GRP'
    kkWhatCamera = kkPublish.getCurrentCamera()
    group( em=True, n = kkGroupName)
    parent(x, kkGroupName)
    parentConstraint (kkWhatCamera, kkGroupName)
    kkExpString = ("float $d = %s.horizontalFilmAperture;" + 
                   "float $f = %s.focalLength;" +
                   "float $ratio = $d / (2 * $f);" +
                   "float $a = 2 * atan($ratio); // angle in radians" +
                   "$a = rad_to_deg($a); // angle in degrees" +
                   "$a = $a/2;" +
                   "float $z = abs(kkTextBlock_GRP.translateZ);" +
                   "float $kkTan = tand($a);" +
                   "$kkScale = $kkTan * $z;" +
                   "$kkScale = $kkScale * 2;" +
                   "kkTextBlock_GRP.scaleX = $kkScale;" +
                   "kkTextBlock_GRP.scaleY = $kkScale;" %
                   (kkWhatCamera, kkWhatCamera))

    expression( n = 'kkText_exp', s= kkExpString )
