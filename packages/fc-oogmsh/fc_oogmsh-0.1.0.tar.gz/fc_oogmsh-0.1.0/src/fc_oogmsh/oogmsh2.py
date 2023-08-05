import numpy as np

from . import gmsh
from .gmsh import elm_type_list,get_elm_desc_by_type,repr_object,set_bbox
from . import msh
from .msh import read_MeshFormat

def isooGmsh2(Gh):
  return isinstance(Gh,ooGmsh2)

class ooGmsh2:
  def __init__(self,gmsh_file=None):
    self.q = []
    self.dim = 3
    self.d=0
    self.nq = 0
    self.meshfile=gmsh_file
    self.M = []
    self.sElts=[]
    self.toGlobal=[]
    self.partitionnedfile=False
    self.orders = []
    self.types =[]
    self.MeshFormat=None
    self.bbox=None
    if gmsh_file==None:
      return
    try:
       fid = open(gmsh_file, "r")
    except IOError:
       raise NameError("File '%s' not found." % (gmsh_file))
    line = fid.readline().strip()
    if line=='$MeshFormat':
      self.MeshFormat=read_MeshFormat(fid)
    line = 'start'
    lineno=2
    while line:
      line = fid.readline()
      lineno+=1
      if line.find('$Nodes') == 0:
        line = fid.readline()
        lineno+=1
        self.nq = int(line.split()[0])
        self.q = np.zeros((self.nq, 3), dtype=float)
        self.toGlobal=np.zeros((self.nq, ), dtype=int)
        datas=np.reshape(np.fromfile(fid,dtype=np.float64,count=4*self.nq,sep=" "),(self.nq,4)).T # tag x y z on each line
        self.toGlobal=np.int32(datas[0])-1
        self.q = datas[1:4]
        line = fid.readline()
        if line.find('$EndNodes') != 0:
          raise ValueError('expecting EndNodes')
        if np.sum(np.abs(self.q[2]))==0:
          self.q=self.q[0:2]
          self.dim=2
      if line.find('$Elements') == 0:
        self.splitByType(fid)
    self.setOrders()
    self.setTypes()
    self.set_d()
    self.bbox=set_bbox(self.q)
      
  def splitByType(self,fid):
    elm_types=elm_type_list();
    Mt=getElements(fid)
    index=dict(num=0,elm_type=1,nb_tags=2,phys_lab=3,geo_lab=4,nb_parts=5)
    Ltype=np.unique(Mt[:,index['elm_type']])
    for i in range(len(Ltype)):
      eType=elm_types[Ltype[i]-1]
      M=Mt[Mt[:,index['elm_type']]==Ltype[i]]
      self.sElts.append(Elt())
      self.sElts[i].type=eType['elm_type']
      self.sElts[i].geo=eType['geo']
      self.sElts[i].order=eType['order']
      self.sElts[i].d=eType['d']
      self.sElts[i].nme=M.shape[0]
      self.sElts[i].values=M[:,index['geo_lab']:]
      nTags=M[:,index['nb_tags']]-3 # Tags number other that 'phys_lab' and 'geo_lab', if num<=0 => no tags
      self.sElts[i].phys_lab=M[:,index['phys_lab']]
      self.sElts[i].geo_lab=M[:,index['geo_lab']]
      self.sElts[i].nb_parts=np.zeros(self.sElts[i].nme, dtype=int)
      self.sElts[i].part_lab=[None] * self.sElts[i].nme
      
      ndfe=int(eType['nb_nodes'])
      self.sElts[i].me=np.zeros((self.sElts[i].nme,ndfe), dtype=int)
      
      K=(nTags>=0).nonzero()[0] # index of elmts with partition ids
      if len(K)>0:
        Kc=np.setdiff1d(np.arange(self.sElts[i].nme),K) #index of elmts without partition ids
        self.sElts[i].nb_parts[K]=M[K,index['nb_parts']]   
        self.sElts[i].part_lab=np.zeros((self.sElts[i].nme,max(nTags)))
      else:
        Kc=np.arange(self.sElts[i].nme )
      
      if len(Kc)>0: #read elmts without partition ids
        self.sElts[i].me[Kc]=M[Kc,:][:,index['geo_lab']+1+np.arange(ndfe)]#.transpose()
      
      #read elmts with partition ids  
      LnTags=np.unique(nTags[K])
      for nt in LnTags:
        ik=(nTags[K]==nt).nonzero()[0]
        k=K[ik]
        self.sElts[i].part_lab[np.ix_(k,np.arange(nt))]=M[k,:][:,index['nb_parts']+1+np.arange(nt)]
        self.sElts[i].me[k]=M[k,:][:,index['nb_parts']+nt+1+np.arange(ndfe)]
      #self.sElts[i].me-=1
      self.sElts[i].me=self.sElts[i].me.T-1
      
  def setOrders(self):
      Orders=np.zeros(len(self.sElts),dtype=int)
      for i in range(len(self.sElts)):
        Orders[i]=self.sElts[i].order
      self.orders=np.unique(Orders)
    
  def setTypes(self):
      Types=np.zeros(len(self.sElts),dtype=int)
      for i in range(len(self.sElts)):
        Types[i]=self.sElts[i].type
      self.types=Types
      
  def set_d(self):
    for i in range(len(self.sElts)):
      EltDesc=get_elm_desc_by_type(self.sElts[i].type)
      self.d=max(self.d,EltDesc['d'])
      
      
      
  def __repr__(self):
    strret = '%s object \n'%(self.__class__.__name__ )
    strret += '    dim : %d\n'%self.dim 
    strret += '      d : %d\n'%self.d 
    strret += '  types : %s\n'%str(self.types)
    strret += ' orders : %s\n'%str(self.orders)
    strret += '     nq : %d\n'%self.nq
    strret += repr_object('      q :',self.q)+'\n'
    strret += repr_object('toGlobal:',self.toGlobal)+'\n'
    strret += repr_object('  sElts :',self.sElts)
    #strret += '      q : %s object[%s], size %s\n'%(self.q.__class__.__name__,str(self.q.dtype),str(self.q.shape))
    #strret += 'toGlobal: %s object, size %s\n'%(self.toGlobal.__class__.__name__,str(self.toGlobal.shape))
##    strret += '      M : dimension %s\n'%str(self.M.shape)
    #strret += '  sElts : list of (%d) %s objects'%(len(self.sElts),self.sElts[0].__class__.__name__)
    return strret
  
  def phy2geo(self):
    import numpy
    ne=len(self.sElts)
    p2gdict=lambda Type,phylab,Geos,geolab,phys: dict(type=Type,phys_labs=phylab,toGeo=Geos,geo_labs=geolab,toPhys=phys)
    p2g=[]
    for sE in self.sElts:
      phylab=np.unique(sE.phys_lab)
      Geos=[];Phys=[]
      for pl in phylab:
        idx=np.where( (sE.phys_lab==pl) )[0]
        G=np.unique(sE.geo_lab[idx])
        Geos.append( G )
        Phys.append(pl*np.ones(G.shape))
      p2g.append( p2gdict(sE.type,phylab,Geos,np.concatenate(Geos),np.concatenate(Phys)) )
    return p2g
  
  def info(self):
    L=elm_type_list()
    for type in self.types:
      print('type %2d : %s'%(type,L[type-1]['desc']))
      
  def extractElement(self,Type,**kwargs):
    import numpy
    # return (q,me) with q a nq-by-dim array and me a (d+1)-by-nme array
    it=np.where(self.types==Type)[0]
    assert len(it)==1
    sE=self.sElts[it[0]]
    geo_labs=kwargs.get('geo_labs',None)
    phys_labs=kwargs.get('phys_labs',None)
    qtrans=kwargs.get('qtrans',False)
    if geo_labs is not None and phys_lab is not None:
      raise ValueError('Unallowed used of options')
    if geo_labs is None and phys_labs is None:
      idx,me=np.unique(sE.me,return_inverse=True)
      return self.q[idx],me.reshape(sE.me.shape)
    if geo_labs is not None:
      labs=sE.geo_lab
      olabs=geo_labs
    else:
      labs=sE.phys_lab
      olabs=phys_labs
    ME=sE.me[:,np.isin(labs,olabs)]
    idx,me=np.unique(ME,return_inverse=True)
    if qtrans:
      return self.q[idx].T,me.reshape(ME.shape)
    else:
      return self.q[idx],me.reshape(ME.shape)
    
  def get_q(self):
    return self.q,self.toGlobal
  
  def get_PhysicalTags(self,Type):
    if Type not in self.types: return None
    idx=np.where(self.types==Type)[0]
    assert len(idx)==1,'idx=%s'%str(idx)
    return np.unique(self.sElts[idx[0]].phys_lab)
  
  def get_ElementaryTags(self,Type):
    if Type not in self.types: return None
    idx=np.where(self.types==Type)[0]
    assert len(idx)==1,'idx=%s'%str(idx)
    return np.unique(self.sElts[idx[0]].geo_lab)
  
  def get_me_PhysicalTag(self,Type,phtag):
    if Type not in self.types: return None
    idx=np.where(self.types==Type)[0]
    assert len(idx)==1,'idx=%s'%str(idx)
    i=idx[0]
    k=np.where(self.sElts[i].phys_lab==phtag)[0]
    return self.sElts[i].me[:,k]
  
  def get_me_ElementaryTag(self,Type,eltag):
    if Type not in self.types: return None
    idx=np.where(self.types==Type)[0]
    assert len(idx)==1,'idx=%s'%str(idx)
    i=idx[0]
    k=np.where(self.sElts[i].geo_lab==eltag)[0]
    return self.sElts[i].me[:,k]
  
  def get_localmesh_PhysicalTag(self,EltType,PhysTag):
    from fc_oogmsh.msh import FromGlobalToLocal
    me=self.get_me_PhysicalTag(EltType,PhysTag)
    return FromGlobalToLocal(self.q,me,self.toGlobal)  
    
  def get_localmesh_ElementaryTag(self,EltType,eltag):
    from fc_oogmsh.msh import FromGlobalToLocal
    me=self.get_me_ElementaryTag(EltType,eltag)
    return FromGlobalToLocal(self.q,me,self.toGlobal)    
    
class Elt: # ooMs
  def __init__(self):
    self.type = 0
    self.geo = '' # kind of geometry
    self.order = 0
    self.d = 0
    self.nme = [] # N -> nme
    self.values=[]
    self.nTags=[]
    self.phys_lab=[] # PhysicalLabel -> phys_lab
    self.geo_lab = [] # GeometricalLabel -> geo_lab
    self.nb_parts =[] # nMeshPart -> nb_parts
    self.part_lab =[] #  MeshPart -> part_lab
    self.me =[]    
    
  def __repr__(self):
    strret = '%s object \n'%self.__class__.__name__ 
    strret += '      d : %d, type : %d, order : %d\n'%(self.d,self.type,self.order)
    strret += '    geo : %s\n'%self.geo
    strret += '    nme : %d\n'%self.nme
    strret += repr_object('     me :',self.me)+'\n'
    strret += repr_object('phys_lab:',self.phys_lab)+'\n'
    strret += repr_object('geo_lab :',self.geo_lab)+'\n'
    strret += repr_object('part_lab:',self.part_lab)+'\n'
    strret += repr_object('nb_parts:',self.nb_parts)+'\n'
    strret += repr_object('  nTags :',self.nTags)
    return strret
  
  
def getElements(fid):
  import numpy
  line = fid.readline()
  nel = int(line.split()[0])
  M=np.zeros((nel,55), dtype=int)
  maxcol=0
  for i in range(0, nel):
    line = fid.readline()
    data = line.split()
    nd=len(data)
    maxcol=max(maxcol,nd)
    M[i,0:nd]=data
  M=M[:,0:maxcol]
  line = fid.readline()
  if line.find('$EndElements') != 0:
    raise ValueError('expecting EndElements') 
  return M
  

