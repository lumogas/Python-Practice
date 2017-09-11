### This script makes sure all the useless elements are hidden from view 
### during a playblast. It then makes visible everything that was active 
### before.

from pymel.core import *
import maya.mel as mel

# Mel command to query gpu caches... 
# modelEditor -q -queryPluginObjects gpuCacheDisplayFilter modelPanel4;

#First, the variables
kkCount = 0

# menu items - what can be shown?
kkPanelItems =  ["nurbsCurves", "nurbsSurfaces", 
                 "polymeshes" , "subdivSurfaces", "planes", "lights", 
                 "cameras", "joints", "ikHandles", "deformers","dynamics", 
                 "fluids", "hairSystems",
                "follicles", "nCloths", "nRigids","dynamicConstraints", 
                "locators", "dimensions", "pivots", "handles","textures", 
                "strokes", "manipulators", "cv", "hulls", "grid", "hud", 
                "sel"]

#menu items - what should be shown?
kkValidItems = ["polymeshes"]

kkStatusList = []
                
kkCurrentPanel = getPanel(wf=True)

#record all the display status for each item in the list
for kkItem in kkPanelItems:
    # kkCommand = 'modelEditor( kkCurrentPanel' + ', query = True, ' + kkItem + '= True )'
    kkCommand = ('modelEditor( kkCurrentPanel, query = True, %s = True)' 
                 % (kkItem))
    kkStatusList.append(eval(kkCommand))
    print kkCommand

# We now have a list of everything that's visible. To blast,first we hide 
# everything...
modelEditor( kkCurrentPanel, edit = True, alo = False )

#now show only meshes ( and caches, if visible)
modelEditor( kkCurrentPanel, edit = True, polymeshes = True )

kkMelStatus = str(kkStatusList[0]).lower()
print kkMelStatus
kkMelCommand = 'modelEditor -e -pluginObjects gpuCacheDisplayFilter '+ kkMelStatus  + ' ' + kkCurrentPanel; # Separate command for the @!*$ gpu caches...
print kkMelCommand
mel.eval(kkMelCommand)

playblast()

# Now restore visibility to all hidden items, so everything goes back to 
# what it was before the playblast.

for kkStatus in kkStatusList:
    print kkItem
    kkWhat = str(kkPanelItems[kkCount])
    kkCommand = 'modelEditor( kkCurrentPanel' + ', edit = True, ' + kkWhat + '= ' + str(kkStatus)  + ' )'
    print kkCommand
    eval(kkCommand)
    kkCount += 1
