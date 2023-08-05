""" Contains various functions compatible with MshFormat version 4.0
   
"""
import numpy as np

# $Entities 
from fc_oogmsh.msh import Entity    
    
class Point_Entity(Entity):
  def __init__(self):
    Entity.__init__(self)    
    
  def read(self,fid):
    self.read_Entity(fid)
# $EndEntities 
        
# $Nodes
def read_Nodes(self,fid,verbose=False):
  from fc_oogmsh.msh import NodesEntityBlock
  R = fid.readline().split()
  self.numEntityBlocks=np.int32(R[0])
  self.numNodes=np.int32(R[1])
  self.EntityBlocks=[NodesEntityBlock() for x in range(self.numEntityBlocks)]
  self.minNodeTag=10**6;self.maxNodeTag=0; # Missing in 4.0 version but present in 4.1
  for i in range(self.numEntityBlocks):
    self.EntityBlocks[i].read(fid,MeshFormat='4.0')
    if len(self.EntityBlocks[i].nodeTags)>0:
      self.minNodeTag=min(self.minNodeTag,min(self.EntityBlocks[i].nodeTags))
      self.maxNodeTag=max(self.maxNodeTag,max(self.EntityBlocks[i].nodeTags))
  R = fid.readline().strip()
  assert R=='$EndNodes'
  if verbose:
    print('Reading $Nodes section seem OK')
    
def read_NodesEntityBlock(self,fid):
  R=fid.readline().split()
  self.entityTag=np.int32(R[0])
  self.entityDim=np.int32(R[1])
  self.parametric=np.int32(R[2])
  self.numNodes=np.int32(R[3])
  R=np.fromfile(fid,dtype=np.float64,count=self.numNodes*4,sep=" ")
  K=R.reshape((self.numNodes,4)).T 
  self.nodeTags=np.int32(K[0])
  self.Nodes=K[1:]
# $EndNodes


