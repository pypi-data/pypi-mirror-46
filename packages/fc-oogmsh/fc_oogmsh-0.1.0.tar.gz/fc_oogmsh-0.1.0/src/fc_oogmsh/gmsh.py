import numpy as np
import os,errno
import os.path as op
from . import Sys

from fc_tools.others import mkdir_p

 
def repr_object(strname,value):
  if isinstance(value,np.ndarray):
    return strname + ' %s object[%s], size %s'%(value.__class__.__name__,str(value.dtype),str(value.shape))
  if isinstance(value,list):
    return strname + ' %s of %d elements'%(value.__class__.__name__,len(value))
  return strname + ' unknown'

def set_bbox(q):
  dim=q.shape[0]
  bbox=np.zeros((q.shape[0],2))
  for i in range(dim):
    bbox[i,0]=np.min(q[i])
    bbox[i,1]=np.max(q[i])
  return bbox.flatten()
    
def NumNodesByEltType():
  elm_type=np.zeros((32,),dtype=int)
  elm_type[0] = 2   # not used
  elm_type[1] = 2   # 2-node line
  elm_type[2] = 3   # 3-node triangle
  elm_type[3] = 4   # 4-node quadrangle
  elm_type[4] = 4   # 4-node tetrahedron
  elm_type[5] = 8   # 8-node hexahedron
  elm_type[6] = 6   # 6-node prism
  elm_type[7] = 5   # 5-node pyramid
  elm_type[8] = 3   # 3-node second order line
                     # (2 nodes at vertices and 1 with edge)
  elm_type[9] = 6   # 6-node second order triangle
                      # (3 nodes at vertices and 3 with edges)
  elm_type[10] = 9   # 9-node second order quadrangle
                      # (4 nodes at vertices,
                      #  4 with edges and 1 with face)
  elm_type[11] = 10   # 10-node second order tetrahedron
                      # (4 nodes at vertices and 6 with edges)
  elm_type[12] = 27   # 27-node second order hexahedron
                      # (8 nodes at vertices, 12 with edges,
                      #  6 with faces and 1 with volume)
  elm_type[13] = 18   # 18-node second order prism
                      # (6 nodes at vertices,
                      #  9 with edges and 3 with quadrangular faces)
  elm_type[14] = 14   # 14-node second order pyramid
                      # (5 nodes at vertices,
                      #  8 with edges and 1 with quadrangular face)
  elm_type[15] = 1  # 1-node point
  elm_type[16] = 8   # 8-node second order quadrangle
                      # (4 nodes at vertices and 4 with edges)
  elm_type[17] = 20   # 20-node second order hexahedron
                      # (8 nodes at vertices and 12 with edges)
  elm_type[18] = 15   # 15-node second order prism
                      # (6 nodes at vertices and 9 with edges)
  elm_type[19] = 13   # 13-node second order pyramid
                      # (5 nodes at vertices and 8 with edges)
  elm_type[20] = 9   # 9-node third order incomplete triangle
                      # (3 nodes at vertices, 6 with edges)
  elm_type[21] = 10   # 10-node third order triangle
                      # (3 nodes at vertices, 6 with edges, 1 with face)
  elm_type[22] = 12   # 12-node fourth order incomplete triangle
                      # (3 nodes at vertices, 9 with edges)
  elm_type[23] = 15   # 15-node fourth order triangle
                      # (3 nodes at vertices, 9 with edges, 3 with face)
  elm_type[24] = 15   # 15-node fifth order incomplete triangle
                      # (3 nodes at vertices, 12 with edges)
  elm_type[25] = 21   # 21-node fifth order complete triangle
                      # (3 nodes at vertices, 12 with edges, 6 with face)
  elm_type[26] = 4   # 4-node third order edge
                      # (2 nodes at vertices, 2 internal to edge)
  elm_type[27] = 5   # 5-node fourth order edge
                      # (2 nodes at vertices, 3 internal to edge)
  elm_type[28] = 6   # 6-node fifth order edge
                      # (2 nodes at vertices, 4 internal to edge)
  elm_type[29] = 20   # 20-node third order tetrahedron
                      # (4 nodes at vertices, 12 with edges,
                      #  4 with faces)
  elm_type[30] = 35   # 35-node fourth order tetrahedron
                      # (4 nodes at vertices, 18 with edges,
                      #  12 with faces, 1 in volume)
  elm_type[31] = 56   # 56-node fifth order tetrahedron
                      # (4 nodes at vertices, 24 with edges,
                      #  24 with faces, 4 in volume)
  return elm_type

def orderByEltType():
  order=np.zeros((32,),dtype=int)
  order[1] = 1   # 2-node line
  order[2] = 1   # 3-node triangle
  order[3] = 1   # 4-node quadrangle
  order[4] = 1   # 4-node tetrahedron
  order[5] = 1   # 8-node hexahedron
  order[6] = 1  # 6-node prism
  order[7] = 1   # 5-node pyramid
  order[8] = 2   # 3-node second order line
                     # (2 nodes at vertices and 1 with edge)
  order[9] = 2   # 6-node second order triangle
                      # (3 nodes at vertices and 3 with edges)
  order[10] = 2   # 9-node second order quadrangle
                      # (4 nodes at vertices,
                      #  4 with edges and 1 with face)
  order[11] = 2   # 10-node second order tetrahedron
                      # (4 nodes at vertices and 6 with edges)
  order[12] = 2   # 27-node second order hexahedron
                      # (8 nodes at vertices, 12 with edges,
                      #  6 with faces and 1 with volume)
  order[13] = 2   # 18-node second order prism
                      # (6 nodes at vertices,
                      #  9 with edges and 3 with quadrangular faces)
  order[14] = 2   # 14-node second order pyramid
                      # (5 nodes at vertices,
                      #  8 with edges and 1 with quadrangular face)
  order[15] = 1   # 1-node point
  order[16] = 2  # 8-node second order quadrangle
                      # (4 nodes at vertices and 4 with edges)
  order[17] = 2   # 20-node second order hexahedron
                      # (8 nodes at vertices and 12 with edges)
  order[18] = 2   # 15-node second order prism
                      # (6 nodes at vertices and 9 with edges)
  order[19] = 2   # 13-node second order pyramid
                      # (5 nodes at vertices and 8 with edges)
  order[20] = 3   # 9-node third order incomplete triangle
                      # (3 nodes at vertices, 6 with edges)
  order[21] = 3   # 10-node third order triangle
                      # (3 nodes at vertices, 6 with edges, 1 with face)
  order[22] = 4   # 12-node fourth order incomplete triangle
                      # (3 nodes at vertices, 9 with edges)
  order[23] = 4   # 15-node fourth order triangle
                      # (3 nodes at vertices, 9 with edges, 3 with face)
  order[24] = 5   # 15-node fifth order incomplete triangle
                      # (3 nodes at vertices, 12 with edges)
  order[25] = 5   # 21-node fifth order complete triangle
                      # (3 nodes at vertices, 12 with edges, 6 with face)
  order[26] = 3   # 4-node third order edge
                      # (2 nodes at vertices, 2 internal to edge)
  order[27] = 4  # 5-node fourth order edge
                      # (2 nodes at vertices, 3 internal to edge)
  order[28] = 5   # 6-node fifth order edge
                      # (2 nodes at vertices, 4 internal to edge)
  order[29] = 3   # 20-node third order tetrahedron
                      # (4 nodes at vertices, 12 with edges,
                      #  4 with faces)
  order[30] = 4   # 35-node fourth order tetrahedron
                      # (4 nodes at vertices, 18 with edges,
                      #  12 with faces, 1 in volume)
  order[31] = 5   # 56-node fifth order tetrahedron
                      # (4 nodes at vertices, 24 with edges,
                      #  24 with faces, 4 in volume)
  return order

def EltTypeSimplex(elmtype):
  if elmtype in [15]:
    return 0
  if elmtype in [1,8]:
    return 1
  if elmtype in [2,9,10,15,21]:
    return 2
  if elmtype in [4,11]:
    return 3  
  return None

ListMshFileVersion=['2.2','4.0','4.1']

def check_MshFileVersion(MshFileVersion):
  if MshFileVersion not in ListMshFileVersion:
    raise NameError('[fc_oogmsh] Incompatible mesh file format! %s not in %s'%(MshFileVersion,str(ListMshFileVersion)))

def gmsh_run(geofile,**kwargs):
  env=Sys.environment()
  dim=kwargs.get('dim', 2)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  meshfile=kwargs.get('meshfile','')
  options=kwargs.get('options','')
  strings=kwargs.get('strings',[''])
  force=kwargs.get('force',False)
  verbose=kwargs.get('verbose',1)
  MshFileVersion=kwargs.get('MshFileVersion',setformat())
  if MshFileVersion not in ListMshFileVersion:
    raise NameError('[fc_oogmsh] Incompatible MSH file format! %s not in %s'%(MshFileVersion,str(ListMshFileVersion)))
  if not isGoodMshFormatVersion(MshFileVersion):
    raise NameError('[fc_oogmsh] Need GMSH %s for MSH file format %s but GMSH %s is used!'%(getMinimalVersion(MshFileVersion),MshFileVersion,version()))
  gmsh_cmd=kwargs.get('gmsh_bin',env.gmsh_bin)
  if not os.path.isfile(gmsh_cmd):
    print('[fc_oogmsh] Unable to find GMSH binary application')
    print('[fc_oogmsh]   <%s> does not exists'%gmsh_cmd)
    raise NameError('GMSH binary not found ')
  try:
    fid = open(geofile, "r")
  except IOError:
    raise NameError("File '%s' not found." % (geofile))
  if verbose>0:
    print('[fc_oogmsh] Using input file: %s'%geofile)
  filewoext=op.splitext(op.basename(geofile))[0] # file without extension
  mkdir_p(meshdir)
  if len(meshfile)==0:
    meshfile=meshdir+op.sep+filewoext+".msh"
  if op.isfile(meshfile):
    if force:
      if verbose>0:
        print('[fc_oogmsh] Overwritting mesh file %s'%(meshfile))
    else:
      if verbose>0:
        print('[fc_oogmsh] Mesh file %s already exist.\n  -> Use "force" flag to rebuild if needed.'%(meshfile))
      return meshfile 
    
  strings.append('Mesh.MshFileVersion=%s;'%MshFileVersion)
  gmsh_str=u'%s -%d %s -string "%s" "%s" -o "%s"'%(gmsh_cmd,round(dim),options,' '.join(strings),geofile,meshfile)
  from fc_tools.others import system_run
  if verbose in [1,2]:
    print('[fc_oogmsh] Use option verbose=3 to see gmsh output')
  res=system_run(gmsh_str,name='[fc_oogmsh]',verbose=verbose-1,stop=False)
  if not res:
    raise NameError('[fc_oogmsh] gmsh execution failed')
  if not op.isfile(meshfile):
    raise NameError('[fc_oogmsh] file %s not found'%meshfile)
  return meshfile

def buildmesh(d,geofile,N,**kwargs):
  env=Sys.environment()
  options=kwargs.pop('options','')
  meshdir=kwargs.pop('meshdir',env.mesh_dir)
  options="-setnumber N %d %s"%(N,options)
  ngeofile=checkgeofile(d,geofile)
  filewoext=op.splitext(op.basename(ngeofile))[0] # file without extension
  meshfile_default=meshdir+op.sep+filewoext+"-"+str(N)+".msh"
  meshfile=kwargs.pop('savemesh',meshfile_default)
  mpath=op.dirname(meshfile)
  if len(mpath)>0:
    mkdir_p(mpath)
  else:
    mkdir_p(meshdir)
    meshfile=meshdir+op.sep+meshfile
  gmsh_run(ngeofile,dim=d,options=options,meshfile=meshfile,**kwargs)
  return meshfile

def checkgeofile(d,filename):
  geofile=filename
  if os.path.splitext(filename)[1] == '':
    geofile=filename+'.geo'
  if os.path.isfile(geofile):
    return geofile
  if os.path.dirname(filename) != '':
    raise NameError('Unable to find geofile :\n   %s\n'%geofile)
  env=Sys.environment()
  ngeofile=os.path.join(env.geo_dir,geofile)
  if os.path.isfile(ngeofile):
    return ngeofile
  if d==2.5:
    sd='3ds'
  else:
    sd='%dd'%d
  ngeofile=os.path.join(env.geo_dir,sd,geofile)
  if os.path.isfile(ngeofile):
    return ngeofile
  raise NameError('Unable to find geofile :\n   %s\n in directory %s'%(geofile,ngeofile))
  
def buildmesh2d(geofile,N,**kwargs):
  return buildmesh(2,geofile,N,**kwargs)

def buildmesh3d(geofile,N,**kwargs):
  return buildmesh(3,geofile,N,**kwargs)

def buildmesh3ds(geofile,N,**kwargs):
  return buildmesh(2.5,geofile,N,**kwargs)

def buildpartmesh(meshfile,np,**kwargs):
  options=kwargs.pop('options','')
  options='-saveall -part %d %s'%(np,options)
  filewoext=op.splitext(op.basename(meshfile))[0] # file without extension
  filedir=op.dirname(meshfile)
  savedir=kwargs.pop('savedir',filedir)
  meshpartfile_default=savedir+op.sep+filewoext+'-part%d.msh'%np
  
  meshpartfile=kwargs.pop('savemesh',meshpartfile_default)
  mpath=op.dirname(meshpartfile)
  if len(mpath)>0:
    mkdir_p(mpath)
  else:
    mkdir_p(filedir)
    meshpartfile=filedir+op.sep+meshpartfile
  
  gmsh_run(meshfile,options=options,meshfile=meshpartfile,**kwargs)
  return meshpartfile
  
def buildpartrectangle(Lx,Ly,Nx,Ny,N,**kwargs):
  options=kwargs.pop('options','')
  meshfile=kwargs.pop('meshfile',None)
  filename='rectanglepart';
  #geofile='geodir/2d/'+filename+'.geo'
  geofile=checkgeofile(2,filename)
  if meshfile is None:
    meshfile='%s-Lx%.3f-Ly%.3f-Nx%d-Ny%d-N%d.msh'%(filename,Lx,Ly,Nx,Ny,N)
  options=options+' -setnumber N %d'%N + ' -setnumber NX %d'%Nx + ' -setnumber NY %d'%Ny + ' -setnumber LX %d'%Lx + ' -setnumber LY %d'%Ly 
  gmsh_run(geofile,options=options,meshfile=meshfile,**kwargs)
  return meshfile    
      
def elm_type_list():
  """ FUNCTION gmsh.elm_type_list
    Returns a list of dictionay to obtain informations on 'elm_type' of gmsh.

    OUTPUT:
    elmt_list: cell array such that the i-th elm_type informations are given by
        elmt_list[i-1].elm_type: 
          number of the element -> i,
        elmt_list[i-1].desc: 
          description of the element as a string (coming from gmsh manual),
        elmt_list[i-1].nb_nodes: 
          number of nodes,
        elmt_list[i-1].order: 
          order of the element,
        elmt_list[i-1].incomplete: 
          True if incomplete element, False otherwise,
        elmt_list[i-1].d: 
          minimal space dimension or d-simplex (point, line, triangle, 
          tetrahedron)
        elmt_list[i-1].geo: 
          'point', 'line', 'triangle', 'quadrangle', 'tetrahedron', 'prism', 
          'pyramid' or 'edge'

    USAGE:
    elmt_list=elm_type_list()

    Copyright (C) 2017-2019 F. Cuvelier
  """
  settype=lambda n,s,nn,order,inc,d,geo: dict(elm_type=n,desc=s,nb_nodes=nn,order=order,incomplete=inc,d=d,geo=geo)
  elmt_list=[None]*93  # 93 is the biggest elm_type in gmsh manual
  elmt_list[1-1]=settype(1,'2-node line',2,1,False,1,'line')
  elmt_list[2-1]=settype(2,'3-node triangle',3,1,False,2,'triangle')
  elmt_list[3-1]=settype(3,'4-node quadrangle',4,1,False,2,'quadrangle')
  elmt_list[4-1]=settype(4,'4-node tetrahedron',4,1,False,3,'tetrahedron')
  elmt_list[5-1]=settype(5,'8-node hexahedron',8,1,False,3,'hexahedron')
  elmt_list[6-1]=settype(6,'6-node prism',6,1,False,3,'prism')
  elmt_list[7-1]=settype(7,'5-node pyramid',5,1,False,3,'pyramid')
  elmt_list[8-1]=settype(8,'3-node second order line (2 nodes associated with the vertices and 1 with the edge)',3,2,False,1,'line')
  elmt_list[9-1]=settype(8,'6-node second order triangle (3 nodes associated with the vertices and 3 with the edges)',6,2,False,2,'triangle') 
  elmt_list[10-1]=settype(10,'9-node second order quadrangle (4 nodes associated with the vertices, 4 with the edges and 1 with the face)',9,2,False,2,'quadrangle')
  elmt_list[11-1]=settype(11,'10-node second order tetrahedron (4 nodes associated with the vertices and 6 with the edges)',10,2,False,3,'tetrahedron')
  elmt_list[12-1]=settype(12,'27-node second order hexahedron (8 nodes associated with the vertices, 12 with the edges, 6 with the faces and 1 with the volume)',27,2,False,3,'hexahedron')
  elmt_list[13-1]=settype(13,'18-node second order prism (6 nodes associated with the vertices, 9 with the edges and 3 with the quadrangular faces)',18,2,False,3,'prism')
  elmt_list[14-1]=settype(14,'14-node second order pyramid (5 nodes associated with the vertices, 8 with the edges and 1 with the quadrangular face)',14,2,False,3,'pyramid')
  elmt_list[15-1]=settype(15,'1-node point',1,1,False,0,'point')
  elmt_list[16-1]=settype(16,'8-node second order quadrangle (4 nodes associated with the vertices and 4 with the edges)',8,2,False,2,'quadrangle')
  elmt_list[17-1]=settype(17,'20-node second order hexahedron (8 nodes associated with the vertices and 12 with the edges)',20,2,False,3,'hexahedron')
  elmt_list[18-1]=settype(18,'15-node second order prism (6 nodes associated with the vertices and 9 with the edges)',15,2,False,3,'prism')
  elmt_list[19-1]=settype(19,'13-node second order pyramid (5 nodes associated with the vertices and 8 with the edges)',15,2,False,3,'pyramid')
  elmt_list[20-1]=settype(20,'9-node third order incomplete triangle (3 nodes associated with the vertices, 6 with the edges)',9,3,True,2,'triangle')
  elmt_list[21-1]=settype(21,'10-node third order triangle (3 nodes associated with the vertices, 6 with the edges, 1 with the face)',10,3,False,2,'triangle')
  elmt_list[22-1]=settype(22,'12-node fourth order incomplete triangle (3 nodes associated with the vertices, 9 with the edges)',12,4,True,2,'triangle')
  elmt_list[23-1]=settype(23,'15-node fourth order triangle (3 nodes associated with the vertices, 9 with the edges, 3 with the face)',15,4,False,2,'triangle')
  elmt_list[24-1]=settype(24,'15-node fifth order incomplete triangle (3 nodes associated with the vertices, 12 with the edges)',15,5,True,2,'triangle')
  elmt_list[25-1]=settype(25,'21-node fifth order complete triangle (3 nodes associated with the vertices, 12 with the edges, 6 with the face)',21,5,False,2,'triangle')
  elmt_list[26-1]=settype(26,'4-node third order edge (2 nodes associated with the vertices, 2 internal to the edge)',4,3,False,2,'edge') #dim 1 or 2?
  elmt_list[27-1]=settype(27,'5-node fourth order edge (2 nodes associated with the vertices, 3 internal to the edge)',5,4,False,2,'edge')#dim 1 or 2?
  elmt_list[28-1]=settype(28,'6-node fifth order edge (2 nodes associated with the vertices, 4 internal to the edge)',6,5,False,2,'edge')#dim 1 or 2?
  elmt_list[29-1]=settype(29,'20-node third order tetrahedron (4 nodes associated with the vertices, 12 with the edges, 4 with the faces)',20,3,False,3,'tetrahedron')
  elmt_list[30-1]=settype(30,'35-node fourth order tetrahedron (4 nodes associated with the vertices, 18 with the edges, 12 with the faces, 1 in the volume)',35,4,False,3,'tetrahedron')
  elmt_list[31-1]=settype(31,'56-node fifth order tetrahedron (4 nodes associated with the vertices, 24 with the edges, 24 with the faces, 4 in the volume)',56,5,False,3,'tetrahedron')
  elmt_list[92-1]=settype(92,'64-node third order hexahedron (8 nodes associated with the vertices, 24 with the edges, 24 with the faces, 8 in the volume)',64,3,False,3,'hexahedron')
  elmt_list[93-1]=settype(93,'125-node fourth order hexahedron (8 nodes associated with the vertices, 36 with the edges, 54 with the faces, 27 in the volume)',125,4,False,3,'hexahedron') 
  return elmt_list

def get_elm_desc_by_type(Type):
  return elm_type_list()[Type-1]

#def system_run_out(cmd_str,**kwargs):
  #import  subprocess
  #verbose=kwargs.get('verbose',1)
  #name=kwargs.get('name','[fc_tools]')
  #stop=kwargs.get('stop',True)
  #if verbose>0:
    #print('%s Command line:\n  %s'%(name,cmd_str))
    #print('%s Running command. Be patient...'%name)
  #try:
    #out=None
    #out=subprocess.check_output(cmd_str,shell=True, stderr=subprocess.STDOUT)
  #except subprocess.CalledProcessError:
    #if out is not None:
      #Out=out.decode("utf-8")
      #for line in Out.splitlines():
        #print(line)
    #else:
      #print('%s Try manually to see error messages'%name)
    #if stop:
      #raise NameError('%s Execution of %s failed!\n'%(name,cmd_str))
    #else:
      #print('%s Execution of %s failed!\n'%(name,cmd_str))
      #return False
  
  #if out is not None:
    #Out=out.decode("utf-8")
  #else:
    #Out=''
  #return Out

def version():
  from fc_tools.Sys import isWindows
  env=Sys.environment()
  gmsh_cmd=env.gmsh_bin
  if not os.path.isfile(gmsh_cmd):
    print('[fc_oogmsh] Unable to find GMSH binary application')
    print('[fc_oogmsh]   <%s> does not exists'%gmsh_cmd)
    raise NameError('GMSH binary not found ')
  if isWindows():
    gmsh_str=u"%s -version "%gmsh_cmd
    shell=False
  else:
    gmsh_str=u"%s -version 2>&1"%gmsh_cmd
    shell=True
  from fc_tools.others import system_run_out
  res=system_run_out(gmsh_str,name='[fc_oogmsh]',verbose=0,stop=False,shell=shell)
  if not res:
    raise NameError('[fc_oogmsh] gmsh execution failed')
  
  return res.splitlines()[-1]

def getMinimalVersion(strformat):
  if strformat=='4.1':
    return '4.2.0'
  if strformat=='4.0':
    return '4.0.0'
  if strformat=='2.2':
    return '3.0.0'
  raise NameError('[fc_oogmsh] Unknow MSH file format %s!'%strformat)

def setformat():
  from distutils.version import StrictVersion
  ver=version();
  sver=StrictVersion(ver)
  if sver >= StrictVersion('4.2.0'):
    return '4.1'
  if sver >= StrictVersion('4.0.0'):
    return '4.0'
  if sver >= StrictVersion('3.0.0'):
    return '2.2'
  raise NameError('[fc_oogmsh] Unable to set format for gmsh version %s'%ver)
  
def isGoodMshFormatVersion(strformat):
  from distutils.version import StrictVersion
  ver=version();
  sver=StrictVersion(ver)
  if sver >= StrictVersion('4.2.0'):
    return StrictVersion(strformat) <= StrictVersion('4.1')
  if sver >= StrictVersion('4.0.0'):
    return StrictVersion(strformat) <= StrictVersion('4.0')
  if sver >= StrictVersion('3.0.0'):
    return StrictVersion(strformat) <= StrictVersion('2.2')
  return False
  
def getMSHfile_formats():
  setformat=lambda fmt,ver:dict(format=fmt,min_version=ver)
  return [setformat('2.2','3.0.0'),setformat('4.0','4.0.0'),setformat('4.1','4.2.0')]
