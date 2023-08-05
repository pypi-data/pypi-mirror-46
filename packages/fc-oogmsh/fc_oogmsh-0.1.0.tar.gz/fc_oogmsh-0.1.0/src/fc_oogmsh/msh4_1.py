""" Contains various functions compatible with MshFormat version 4.1
   
"""
import numpy as np
    
class Point_Entity:
  def __init__(self):
    self.tag=None
    self.Point=None
    self.numPhysicalTags=None
    self.PhysicalTags=None
    
  def read(self,fid):
    R = fid.readline().split()
    self.tag=np.int32(R[0])
    self.Point=np.float64(R[1:4])
    self.numPhysicalTags=np.int32(R[4])
    e=5+self.numPhysicalTags
    self.PhysicalTags=np.int32(R[5:e])
    
# $Nodes
def read_Nodes(self,fid,verbose=False):
  from fc_oogmsh.msh import NodesEntityBlock
  R = fid.readline().split()
  self.numEntityBlocks=np.int32(R[0])
  self.numNodes=np.int32(R[1])
  self.EntityBlocks=[NodesEntityBlock() for x in range(self.numEntityBlocks)]
  self.minNodeTag=np.int32(R[2])
  self.maxNodeTag=np.int32(R[3])
  for i in range(self.numEntityBlocks):
    self.EntityBlocks[i].read(fid,MeshFormat='4.1')
  R = fid.readline().strip()
  assert R=='$EndNodes'
  if verbose:
    print('Reading $Nodes section seem OK')
    
def read_NodesEntityBlock(self,fid):
  R=np.fromfile(fid,dtype=np.int32,count=4,sep=" ")
  self.entityTag=R[1]
  self.entityDim=R[0]
  self.parametric=R[2]
  self.numNodes=R[3]
  self.nodeTags=np.fromfile(fid,dtype=np.int32,count=self.numNodes,sep=" ") # One tag by line
  self.Nodes=np.reshape(np.fromfile(fid,dtype=np.float64,count=3*self.numNodes,sep=" "),(self.numNodes,3)).T # x y z on each line
# $EndNodes
    
class Point_PartitionedEntity:
  def __init__(self):
    self.tag=0
    self.parentDim=0
    self.parentTag=0
    self.numPartitions=0
    self.partitionTags=[]
    self.point=[]
    self.numPhysicalTags=[]
    self.PhysicalTags=[]
    
  def read(self,fid,Bounding=True):
    R=np.fromfile(fid,dtype=np.int32,count=4,sep=" ")
    self.tag=R[0]
    self.parentDim=R[1]
    self.parentTag=R[2]
    self.numPartitions=R[3]
    if R[3]>0:
      self.partitionTags=np.fromfile(fid,dtype=np.int32,count=R[3],sep=" ")
    self.point=np.fromfile(fid,dtype=np.float64,count=3,sep=" ")
    self.numPhysicalTags=np.fromfile(fid,dtype=np.int32,count=1,sep=" ")[0]
    if self.numPhysicalTags>0:
      self.PhysicalTags=np.fromfile(fid,dtype=np.int32,count=self.numPhysicalTags,sep=" ")
    if Bounding: # Curves, Surfaces and Volumes
      self.numBounding=np.fromfile(fid,dtype=np.int32,count=1,sep=" ")[0]
      if self.numBounding>0:
        self.BoundingTags=np.fromfile(fid,dtype=np.int32,count=self.numBounding,sep=" ")
        
    

