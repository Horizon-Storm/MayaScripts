#Create Lightning Mesh

import maya.cmds as cmds
import random

''' 
Create and deform a number of meshes and uv's for use with a scrolling UV2 material 
'''

numMeshes = 10

divisions = 20
moveRepeats = 3  #more repeats results in a more jagged mesh
offsetfactor = 1

#Loop over numMeshes

for mesh in xrange(0, numMeshes):

    #Create Mesh and randomly move Edges
    
    lightningmesh = cmds.polyPlane( sx=divisions, sy=1, w=20, h=0.5)[0]
    
    for rep in xrange(0,moveRepeats):
        for x in xrange(3,(divisions*2),2):
            offset = (random.random()-0.5)*2 * offsetfactor
            cmds.select("{0}.e[{1}]".format(lightningmesh,x))
            cmds.move(offset, z=1, r=1)
            
            
    #Create Second UV Set
    
    cmds.select("{0}.map[:]".format(lightningmesh))
    cmds.polyEditUV(pivotV=0, scaleV=0.01)
    
    cmds.select("{0}.map[:]".format(lightningmesh))
    cmds.polyEditUV(r=1, v=mesh*(1.0/numMeshes))

    cmds.select('{0}'.format(lightningmesh))
    cmds.polyCopyUV(createNewMap=1)
        
    cmds.polyNormalizeUV(pa=0)

    #Add a Wave Deformer
    
    Amp = (random.random()-0.5) * 0.4
    Wavelength = random.random() + 0.5
       
    cmds.select('{0}'.format(lightningmesh))
    WaveDef = cmds.nonLinear(type="wave")[0] 
    
    cmds.setAttr('{0}.amplitude'.format(WaveDef), Amp)
    cmds.setAttr('{0}.wavelength'.format(WaveDef), Wavelength)
    cmds.setAttr('{0}.dropoff'.format(WaveDef), 1)
    
    #Add a Twist Deformer
    
    TwistAngle = (random.random()-0.5)*2 * 720
    
    cmds.select('{0}'.format(lightningmesh))
    TwistDef = cmds.nonLinear(type='twist')
    
    cmds.setAttr('{0}.rz'.format(TwistDef[1]), 90)
    cmds.setAttr('{0}.endAngle'.format(TwistDef[0]), TwistAngle)