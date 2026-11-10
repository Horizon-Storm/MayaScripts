#Create Lightning Mesh

import maya.cmds as cmds
import random

''' 
Create and deform a number of meshes and uv's for use with a scrolling UV2 material 
'''

numMeshes = 10

# Number of subdivisions across each plane, and how many times to jag the edges.
divisions = 20
# Controls the distance of each random edge offset.
moveRepeats = 3  # More repeats result in a more jagged mesh.
offsetfactor = 1

#Loop over numMeshes

for mesh in xrange(0, numMeshes):

    #Create Mesh and randomly move Edges
    # Create a long, narrow plane to use as the base lightning mesh.
    
    lightningmesh = cmds.polyPlane( sx=divisions, sy=1, w=20, h=0.5)[0]
    
    # Move alternating edges by random amounts to create a jagged shape.
    for rep in xrange(0,moveRepeats):
        for x in xrange(3,(divisions*2),2):
            offset = (random.random()-0.5)*2 * offsetfactor
            cmds.select("{0}.e[{1}]".format(lightningmesh,x))
            cmds.move(offset, z=1, r=1)
            
            
    #Create Second UV Set
    # Adjust the current UVs and offset them for this mesh in the sequence.
    
    cmds.select("{0}.map[:]".format(lightningmesh))
    cmds.polyEditUV(pivotV=0, scaleV=0.01)
    
    cmds.select("{0}.map[:]".format(lightningmesh))
    cmds.polyEditUV(r=1, v=mesh*(1.0/numMeshes))

    # Copy the UVs into a new UV set, then normalize the UV layout.
    cmds.select('{0}'.format(lightningmesh))
    cmds.polyCopyUV(createNewMap=1)
        
    cmds.polyNormalizeUV(pa=0)

    #Add a Wave Deformer
    # Add a wave deformer with randomized amplitude and wavelength.
    
    Amp = (random.random()-0.5) * 0.4
    Wavelength = random.random() + 0.5
       
    cmds.select('{0}'.format(lightningmesh))
    WaveDef = cmds.nonLinear(type="wave")[0] 
    
    cmds.setAttr('{0}.amplitude'.format(WaveDef), Amp)
    cmds.setAttr('{0}.wavelength'.format(WaveDef), Wavelength)
    cmds.setAttr('{0}.dropoff'.format(WaveDef), 1)
    
    #Add a Twist Deformer
    # Add a twist deformer and randomize how far it twists the mesh.
    
    TwistAngle = (random.random()-0.5)*2 * 720
    
    cmds.select('{0}'.format(lightningmesh))
    TwistDef = cmds.nonLinear(type='twist')
    
    cmds.setAttr('{0}.rz'.format(TwistDef[1]), 90)
    cmds.setAttr('{0}.endAngle'.format(TwistDef[0]), TwistAngle)