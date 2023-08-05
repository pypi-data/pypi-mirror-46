import numpy as np
from . import gmsh
from .gmsh import elm_type_list,get_elm_desc_by_type,repr_object,set_bbox

def isooGmsh4(Gh):
  return isinstance(Gh,ooGmsh4)

class ooGmsh4:
  def __init__(self,gmsh_file=None,verbose=False):
    self.q=None
    self.nq=0
    self.dim=0
    self.d=0
    self.toGlobal=None
    self.types=[]
    self.meshfile=gmsh_file
    self.partitionnedfile=False
    self.MeshFormat=None
    self.PhysicalNames=[]
    self.Entities=None
    self.PartitionedEntities=None
    self.Nodes=None
    self.Elements=None
    #self.PeriodicLinks=[]
    
    if gmsh_file==None:
      return
    try:
       fid = open(gmsh_file, "r")
    except IOError:
       raise NameError("File '%s' not found." % (gmsh_file))
    import fc_oogmsh 
    line='start'
    while line:
      line = fid.readline()
      if line:
        self.read_section(fid,line,verbose=verbose)
    fid.close()
    self.q,self.toGlobal=self.get_q()
    if np.all(self.q[2]==0):
      self.q=self.q[:2]
    (self.dim,self.nq)=self.q.shape
    self.set_types()
    self.set_d()
    self.bbox=set_bbox(self.q)
      
  def set_types(self):
    self.types=np.unique(self.Elements.ElementTypes)
      
  def set_d(self):
    for Type in self.types:
      EltDesc=get_elm_desc_by_type(Type)
      self.d=max(self.d,EltDesc['d'])
      
  def __repr__(self):
    strret = '%s object \n'%(self.__class__.__name__ )
    strret += '    dim : %d\n'%self.dim 
    strret += '      d : %d\n'%self.d 
    strret += '  types : %s\n'%str(self.types)
    #strret += ' orders : %s\n'%str(self.orders)
    strret += '     nq : %d\n'%self.nq
    strret += repr_object('      q :',self.q)+'\n'
    strret += repr_object('toGlobal:',self.toGlobal)+'\n'
    strret += 'Entities:'+str(type(self.Entities))+'\n'
    strret += 'Nodes   :'+str(type(self.Nodes))+'\n'
    strret += 'Elements:'+str(type(self.Elements))+'\n'
    return strret
    
  # add read_section  as method     
  from fc_oogmsh.msh import read_section
  
  def get_q(self,**kwargs):
    nodeTags=np.hstack([self.Nodes.EntityBlocks[i].nodeTags for i in range(self.Nodes.numEntityBlocks)])-1
    Nodes=np.hstack([self.Nodes.EntityBlocks[i].Nodes for i in range(self.Nodes.numEntityBlocks)])
    return Nodes,nodeTags
  
  def get_me(self,i):
    assert i in np.arange(self.Elements.numEntityBlocks)
    return self.Elements.EntityBlocks[i].nodeTags
  
  def get_ElementaryTags(self,Type):
    idx=np.where(self.Elements.ElementTypes==Type)[0]
    if len(idx)==0:
      return None
    return np.hstack([self.Elements.EntityBlocks[i].entityTag for i in idx])
  
  def get_PhysicalTags_entityDim(self,entityDim):
    assert entityDim in np.arange(4)
    if entityDim==0:
      return np.unique(np.hstack([self.Entities.Points[i].PhysicalTags for i in range(self.Entities.numPoints)]))
    if entityDim==1:
      return np.unique(np.hstack([self.Entities.Curves[i].PhysicalTags for i in range(self.Entities.numCurves)]))
    if entityDim==2:
      return np.unique(np.hstack([self.Entities.Surfaces[i].PhysicalTags for i in range(self.Entities.numSurfaces)]))
    if entityDim==3:
      return np.unique(np.hstack([self.Entities.Volumes[i].PhysicalTags for i in range(self.Entities.numVolumes)]))
  
  def get_Elements_by_dim(self,entityDim):
    assert entityDim in np.arange(4)
    if entityDim==0:
      return self.Entities.Points
    if entityDim==1:
      return self.Entities.Curves
    if entityDim==2:
      return self.Entities.Surfaces
    if entityDim==3:
      return self.Entities.Volumes
    
  def get_subEntities(self,EltType):
    from fc_oogmsh.gmsh import get_elm_desc_by_type
    elt=get_elm_desc_by_type(EltType)
    if elt is None:
      return None
    idx=np.where(self.Elements.ElementTypes==EltType)[0]
    if len(idx)==0:
      return None
    EltsTags=np.hstack([self.Elements.EntityBlocks[i].entityTag for i in idx])
    
    sE=self.get_Elements_by_dim(elt['d'])
    sEtags=np.hstack([sE[i].tag for i in range(len(sE))])
    B=np.isin(sEtags,EltsTags)
    return [sE[i] for i in range(len(sE)) if B[i]]
    
  def get_PhysicalTags(self,EltType):
    sE=self.get_subEntities(EltType)
    if sE is None:
      return None
    return np.unique(np.concatenate([sE[i].PhysicalTags for i in range(len(sE))]))
  
  def get_me_ElementaryTag(self,EltType,tag):
    idx=np.where(self.Elements.ElementTypes==EltType)[0]
    if len(idx)==0:
      return None
    j=[i for i in idx if self.Elements.EntityBlocks[i].entityTag==tag]
    if len(j)!=1:
      return None
    #assert len(j)==1, 'j=%s'%str(j)
    return self.Elements.EntityBlocks[j[0]].nodeTags-1
  
  def get_localmesh_ElementaryTag(self,EltType,EltTag):
    """ returns q,me,toGlobal
    """
    from fc_oogmsh.msh import FromGlobalToLocal
    me=self.get_me_ElementaryTag(EltType,EltTag)
    return FromGlobalToLocal(self.q,me,self.toGlobal)
      
  def get_me_PhysicalTag(self,EltType,PhysTag):
    sE=self.get_subEntities(EltType)
    if sE is None:
      return None
    J=[ i for i in range(len(sE)) if PhysTag in sE[i].PhysicalTags]
    if len(J)==0:
      return None
    tags=[sE[i].tag for i in J]
    idx=np.where(self.Elements.ElementTypes==EltType)[0]
    if len(idx)==0:
      return None
    entityTags=[self.Elements.EntityBlocks[i].entityTag for i in idx]
    I=np.arange(len(entityTags))[np.isin(entityTags,tags)]
    if len(I)==0:
      return None
    return np.hstack([ self.Elements.EntityBlocks[idx[i]].nodeTags for i in I])-1

  def get_localmesh_PhysicalTag(self,EltType,PhysTag):
    from fc_oogmsh.msh import FromGlobalToLocal
    me=self.get_me_PhysicalTag(EltType,PhysTag)
    return FromGlobalToLocal(self.q,me,self.toGlobal)
