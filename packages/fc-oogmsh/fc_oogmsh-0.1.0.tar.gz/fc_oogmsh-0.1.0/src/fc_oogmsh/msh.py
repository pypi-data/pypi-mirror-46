""" Contains various functions/class compatibles with all MshFormat version >= 4.0

"""
import numpy as np
ListMeshFormat=['4.0','4.1']

def read_MeshFormat(fid):
  #assert line.strip()=='$MeshFormat', '[fc_oogmsh] Not MeshFormat section: %s'%line
  line = fid.readline()
  if not line:
    raise NameError('[fc_oogmsh] Unable to read MeshFormat section')
  data = line.split()
  MeshFormat={'version':data[0],'file_type':int(data[1]),'data_size':int(data[2])}
  line = fid.readline().strip()
  assert line=='$EndMeshFormat'
  if MeshFormat['version']=='4':
    MeshFormat['version']='4.0'
  return MeshFormat

    
def goto_endsection(fid,sectionname):
  assert sectionname[0]=='$', '[fc_oogmsh] Unvalid section name: %s'%sectionname.strip()
  endsectionname=sectionname.replace('$','$End').strip()
  line='start'
  while line:
    line = fid.readline()
    if line.strip()==endsectionname:
      return True
  assert False, '[fc_oogmsh] Unable to find end of the section name: %s'%endsectionname
    
def read_section(obj,fid,Sectionname,verbose=False):#,**kwargs):
  #MeshFormat=kwargs.pop('MeshFormat','4.1')
  if obj.MeshFormat is not None:
    assert obj.MeshFormat['version'] in ListMeshFormat
  from fc_oogmsh.msh import Entities, Nodes, Elements, PartitionedEntities
  assert Sectionname[0]=='$', '[fc_oogmsh] Unvalid section name: %s'%Sectionname
  sectionname=Sectionname[1:].strip()
  if sectionname=='MeshFormat':
    obj.MeshFormat=read_MeshFormat(fid)
    return
  if sectionname=='PhysicalNames':
    obj.PhysicalNames=read_PhysicalNames(fid)
    return
  if sectionname=='Entities':
    obj.Entities=Entities()
    obj.Entities.read(fid,MeshFormat=obj.MeshFormat['version'])
    return
  if sectionname=='Nodes':
    obj.Nodes=Nodes()
    obj.Nodes.read(fid,MeshFormat=obj.MeshFormat['version'])
    return
  if sectionname=='Elements':
    obj.Elements=Elements()
    obj.Elements.read(fid,MeshFormat=obj.MeshFormat['version'])
    return  
  if sectionname=='PartitionedEntities':
    obj.PartitionedEntities=PartitionedEntities()
    obj.PartitionedEntities.read(fid,MeshFormat=obj.MeshFormat['version'])
    obj.partitionnedfile=True
    return
  if verbose:
    print('[fc_oogmsh] Skipping section %s'%Sectionname)
  goto_endsection(fid,Sectionname)
    
    
# $PhysicalNames
def read_PhysicalNames(fid,verbose=False,**kwargs):
  MeshFormat=kwargs.pop('MeshFormat','4.1')
  assert MeshFormat in ListMeshFormat
  from fc_oogmsh.msh import PhysicalName
    
  R = fid.readline().strip()
  numPhysicalNames=np.int32(R)
  PhysicalNames=[PhysicalName() for x in range(numPhysicalNames)]
  for i in range(numPhysicalNames):
    PhysicalNames[i].read(fid) 
  line = fid.readline().strip()
  assert line=='$EndPhysicalNames'
  if verbose:
    print('Reading $PhysicalNames section seem OK')
  return PhysicalNames

class PhysicalName:
  def __init__(self):
    self.dimension=0
    self.physicalTag=[]
    self.name=''
    
  def read(self,fid):
    R = fid.readline().split()
    self.dimension=np.int32(R[0])
    self.physicalTag=np.int32(R[1])
    self.name=' '.join(R[2:])
        
# $EndPhysicalNames


# $Entities 
class Entities:
  def __init__(self):
    self.numPoints=0
    self.Points=[]
    self.numCurves=0
    self.Curves=[]
    self.numSurfaces=0
    self.Surfaces=[]
    self.numVolumes=0
    self.Volumes=[]
    
  def read(self,fid,verbose=False,MeshFormat='4.1'):
    if MeshFormat=='4.1':
      from fc_oogmsh.msh4_1 import Point_Entity
    else:
      from fc_oogmsh.msh4_0 import Point_Entity
    R=np.fromfile(fid,np.int32,count=4,sep=' ')
    self.numPoints=R[0]
    self.Points=[Point_Entity() for x in range(R[0])]
    for i in range(R[0]):
      self.Points[i].read(fid)
    self.numCurves=R[1]
    self.Curves=[Curve_Entity() for x in range(R[1])]
    for i in range(R[1]):
      self.Curves[i].read(fid)
    self.numSurfaces=R[2]
    self.Surfaces=[Surface_Entity() for x in range(R[2])]
    for i in range(R[2]):
      self.Surfaces[i].read(fid)
    self.numVolumes=R[3]
    self.Volumes=[Volume_Entity() for x in range(R[3])]
    for i in range(R[3]):
      self.Volumes[i].read(fid)
    R = fid.readline().strip()
    assert R=='$EndEntities'
    if verbose:
      print('Reading $Entities section seem OK')

class Entity:
  def __init__(self):
    self.tag=None
    self.min=None
    self.max=None
    self.numPhysicalTags=None
    self.PhysicalTags=None
    
  def read_Entity(self,fid):
    R = fid.readline().split()
    self.tag=np.int32(R[0])
    self.min=np.float64(R[1:4])
    self.max=np.float64(R[4:7])
    self.numPhysicalTags=np.int32(R[7])
    e=8+self.numPhysicalTags
    self.PhysicalTags=np.int32(R[8:e])
    return R[e:]
    
        
class Curve_Entity(Entity):
  def __init__(self):
    Entity.__init__(self)
    self.numBoundingPoints=None
    self.PointTags=None
    
  def read(self,fid):
    R=self.read_Entity(fid)
    self.numBoundingPoints=np.int32(R[0])
    self.PointTags=np.int32(R[1:])
    assert len(self.PointTags)==self.numBoundingPoints

class Surface_Entity(Entity):
  def __init__(self):
    Entity.__init__(self)
    self.numBoundingCurves=None
    self.CurveTags=None
    
  def read(self,fid):
    R=self.read_Entity(fid)
    self.numBoundingCurves=np.int32(R[0])
    self.CurveTags=np.int32(R[1:])
    assert len(self.CurveTags)==self.numBoundingCurves 
    
class Volume_Entity(Entity):
  def __init__(self):
    Entity.__init__(self)
    self.numBoundingSurfaces=None
    self.SurfaceTags=None
    
  def read(self,fid):
    R=self.read_Entity(fid)
    self.numBoundingSurfaces=np.int32(R[0])
    self.SurfaceTags=np.int32(R[1:])
    assert len(self.SurfaceTags)==self.numBoundingSurfaces  

# $EndEntities 

# $Nodes
class Nodes:
  def __init__(self):
    self.numNodes=0
    self.minNodeTag=None
    self.maxNodeTag=None
    self.numEntityBlocks=0
    self.numEntityBlocks=None
  
  def read(self,fid,verbose=False,MeshFormat='4.1'):
    if MeshFormat=='4.1':
      from fc_oogmsh.msh4_1 import read_Nodes 
      read_Nodes(self,fid,verbose=verbose)
    else:
      from fc_oogmsh.msh4_0 import read_Nodes 
      read_Nodes(self,fid,verbose=verbose)
    
class NodesEntityBlock:
  def __init__(self):
    self.entityTag=None
    self.entityDim=None
    self.parametric=None
    self.numNodes=None
    self.nodeTags=None
    self.Nodes=None
  
  def read(self,fid,MeshFormat='4.1'):
    if MeshFormat=='4.1':
      from fc_oogmsh.msh4_1 import read_NodesEntityBlock 
      read_NodesEntityBlock(self,fid)
    else:
      from fc_oogmsh.msh4_0 import read_NodesEntityBlock 
      read_NodesEntityBlock(self,fid)
# $EndNodes

# $Elements
class Elements:
  def __init__(self):
    self.numElements=0
    self.ElementTypes=[]
    self.numEntityBlocks=0
    self.EntityBlocks=None
    
  def read(self,fid,verbose=False,MeshFormat='4.1'):
    R = fid.readline().split()
    self.numEntityBlocks=np.int32(R[0])
    self.numElements=np.int32(R[1])
    self.EntityBlocks=[ElementsEntityBlock() for x in range(self.numEntityBlocks)]
    self.ElementTypes=np.zeros((self.numEntityBlocks,),dtype=np.int32)
    for i in range(self.numEntityBlocks):
      self.EntityBlocks[i].read(fid,MeshFormat)
      self.ElementTypes[i]=self.EntityBlocks[i].elementType
    R = fid.readline().strip()
    assert R=='$EndElements'
    if verbose:
      print('Reading $Elements section seem OK')
    
class ElementsEntityBlock:
  def __init__(self):
    self.entityTag=None
    self.entityDim=None
    self.elementDesc=None
    self.nodeTags=None # NodeTags is connectivity array
    self.elementTags=None
    self.numElementsBlock=0
    
  def read(self,fid,MeshFormat):
    from fc_oogmsh.gmsh import get_elm_desc_by_type
    R=fid.readline().split()
    if MeshFormat=='4.1':
      self.entityTag=np.int32(R[1])
      self.entityDim=np.int32(R[0])
    else:
      self.entityTag=np.int32(R[0])
      self.entityDim=np.int32(R[1])
    self.elementType=np.int32(R[2])
    self.elementDesc=get_elm_desc_by_type(self.elementType)
    nb_nodes_by_elt=self.elementDesc['nb_nodes']
    self.numElementsBlock=np.int32(R[3])
    
    
    R=np.fromfile(fid,dtype=np.int32,count=(nb_nodes_by_elt+1)*self.numElementsBlock,sep=" ")
    K=R.reshape((self.numElementsBlock,nb_nodes_by_elt+1)).T 
    self.elementTags=np.int32(K[0])
    self.nodeTags=K[1:]
# $EndElements

# $PartitionedEntities
class PartitionedEntities:
  def __init__(self):
    self.numPartitions=0
    self.numGhostEntities=0
    self.GhostEntities=[]
    self.numPoints=0
    self.numCurves=0
    self.numSurfaces=0
    self.numVolumes=0
    self.Points=[]
    self.Curves=[]
    self.Surfaces=[]
    self.Volumes=[]
    
  def read(self,fid,verbose=False,MeshFormat='4.1'):
    if MeshFormat=='4.1':
      from fc_oogmsh.msh4_1 import Point_PartitionedEntity
    else:
      Point_PartitionedEntity=PartitionedEntity
    R=np.fromfile(fid,dtype=np.int32,count=2,sep=" ")
    self.numPartitions=R[0]
    self.numGhostEntities=R[1]
    if self.numGhostEntities>0:
      #print(self.numGhostEntities)
      R=np.fromfile(fid,dtype=np.int32,count=2*self.numGhostEntities,sep=" ")
      #print(R)
      R=R.reshape((self.numGhostEntities,2)).T
      self.GhostEntities={'tag':R[0],'partition':R[1]}
    R=np.fromfile(fid,dtype=np.int32,count=4,sep=" ")  
    self.numPoints=R[0]
    self.numCurves=R[1]
    self.numSurfaces=R[2]
    self.numVolumes=R[3]
    self.Points=[Point_PartitionedEntity() for x in range(self.numPoints)]
    for i in range(self.numPoints):
      self.Points[i].read(fid,Bounding=False)
    self.Curves=[PartitionedEntity() for x in range(self.numCurves)]
    for i in range(self.numCurves):
      self.Curves[i].read(fid)  
    self.Surfaces=[PartitionedEntity() for x in range(self.numSurfaces)]
    for i in range(self.numSurfaces):
      self.Surfaces[i].read(fid)  
    self.Volumes=[PartitionedEntity() for x in range(self.numVolumes)]
    for i in range(self.numVolumes):
      self.Volumes[i].read(fid)    
    R = fid.readline().strip()
    assert R=='$EndPartitionedEntities', 'Failed! current line is %s'%R
    if verbose:
      print('Reading $PartitionedEntities section seem OK')
      
class PartitionedEntity:
  def __init__(self):
    self.tag=0
    self.parentDim=0
    self.parentTag=0
    self.numPartitions=0
    self.partitionTags=[]
    self.min=[]
    self.max=[]
    self.numPhysicalTags=[]
    self.PhysicalTags=[]
    self.numBounding=0
    self.BoundingTags=[]
    
  def read(self,fid,Bounding=True):
    R=np.fromfile(fid,dtype=np.int32,count=4,sep=" ")
    self.tag=R[0]
    self.parentDim=R[1]
    self.parentTag=R[2]
    self.numPartitions=R[3]
    if R[3]>0:
      self.partitionTags=np.fromfile(fid,dtype=np.int32,count=R[3],sep=" ")
    self.min=np.fromfile(fid,dtype=np.float64,count=3,sep=" ")
    self.max=np.fromfile(fid,dtype=np.float64,count=3,sep=" ")
    self.numPhysicalTags=np.fromfile(fid,dtype=np.int32,count=1,sep=" ")[0]
    if self.numPhysicalTags>0:
      self.PhysicalTags=np.fromfile(fid,dtype=np.int32,count=self.numPhysicalTags,sep=" ")
    if Bounding: # Curves, Surfaces and Volumes
      self.numBounding=np.fromfile(fid,dtype=np.int32,count=1,sep=" ")[0]
      if self.numBounding>0:
        self.BoundingTags=np.fromfile(fid,dtype=np.int32,count=self.numBounding,sep=" ")
    
# $EndPartitionedEntities

def FromGlobalToLocal(q,me,qtags):
  if me is None:
    return None,None,None
  mtag=np.max(qtags) # Suppose qtags to be positive !
  CV=np.zeros((mtag+1,),dtype=np.int32)
  CV[qtags]=np.arange(len(qtags))
  ME=CV[me]
  idx=np.unique(ME)
  Q=q[:,idx] 
  midx=max(idx)
  CV=np.zeros((midx+1,),dtype=np.int32)
  CV[idx]=np.arange(len(idx))
  ME=CV[ME]
  toGlobal=qtags[idx]
  #Q=q[:,toGlobal]
  return Q,ME,qtags[idx]
    
