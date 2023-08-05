import os
import os.path as op

def get_geodirs(dim,d):
  s=get_pathname(dim,d)
  assert s is not None,"Unable to find geo directory for dim=%d and d=%d"%(dim,d)
  env=environment()
  return env.geo_dir+os.sep+s

def get_pathname(dim,d):
  if dim==2 and d==2:
    return '2d'
  if dim==3 and d==2:
    return '3ds'
  if dim==3 and d==3:
    return '3d'
  return None

def configure(**kwargs):
  from fc_tools.others import mkdir_p
  reset=kwargs.get('reset', False )
  verbose=kwargs.get('verbose', True )
  conffile=getLocalConfFile()
  if op.isfile(conffile) and not reset:
    import imp
    #f = open(conffile)
    #env = imp.load_source('env', 'sys', f)
    #env = imp.load_source('env', f)
    env = imp.load_source('env', conffile)
    gmsh_bin=env.gmsh_bin
    mesh_dir=env.mesh_dir
    geo_dir=env.geo_dir
    #f.close()
  else:
    gmsh_bin,geo_dir,mesh_dir=getDefaultConf()
  gmsh_bin=kwargs.get('gmsh', gmsh_bin )
  mesh_dir=kwargs.get('meshdir', mesh_dir )
  geo_dir=kwargs.get('geodir', geo_dir )
  if not os.path.isfile(gmsh_bin):
    print('[fc_oogmsh] Unable to find GMSH binary application')
    print('[fc_oogmsh]   <%s> does not exists'%gmsh_bin)
    print('[fc_oogmsh]   Use configure(gmsh=r"...")')
    raise NameError('GMSH binary not found ')
  if not os.path.isdir(geo_dir):
    raise NameError('Not a directory :\n''geo_dir''=%s\n'%geo_dir)
  if not os.path.isdir(mesh_dir):
    mkdir_p(mesh_dir)
  if verbose:
    print('[fc_oogmsh] Using GMSH binary:\n  %s'%gmsh_bin)
    print('[fc_oogmsh] Default .geo file directory:\n  %s'%geo_dir)
    print('[fc_oogmsh] Default mesh directory:\n  %s'%mesh_dir)
    print('[fc_oogmsh] Writing in:\n  %s'%conffile)
  mkdir_p(op.dirname(conffile))
  fid=open(conffile,'w')
  fid.write('## Automaticaly generated with fc_oogmsh.configure()\n');
  fid.write('gmsh_bin=r"%s"\n'%gmsh_bin)
  fid.write('mesh_dir=r"%s"\n'%mesh_dir)
  fid.write('geo_dir=r"%s"\n'%geo_dir)
  fid.close()
  
def environment():
  conffile=getLocalConfFile()
  if op.isfile(conffile) is False:
    print('Trying to use default parameters!\n Using fc_oogmsh.configure to configure.\n')
    configure()
  import imp
  #f = open(conffile)
  #env = imp.load_source('env', 'sys', f)
  env = imp.load_source('env', conffile)
  #f.close()
  return env

def printenv():
  import fc_oogmsh
  env=environment()
  conffile=getLocalConfFile()
  print('fc_oogmsh package version %s'%fc_oogmsh.__version__)
  print('Configuration file: %s'%conffile)
  print('   gmsh_bin: %s'%env.gmsh_bin)
  print('   mesh_dir: %s'%env.mesh_dir)
  print('    geo_dir: %s'%env.geo_dir)
  
def getLocalDir():
  import getpass,appdirs
  return appdirs.user_data_dir('fc_oogmsh',getpass.getuser())

def getLocalConfFile():
  userdir=getLocalDir()
  from platform import python_version
  return op.join(userdir,'configure_loc_%s.py'%python_version())
  #BUG with python 2: (so uses platform module)
  #import sys
  #return op.join(userdir,'configure_loc_%d.%d.%d.py'%(sys.version_info.major,sys.version_info.minor,sys.version_info.micro))

def getDefaultConf():
  return getDefaultGmshBin(),getDefaultGeoDir(),getDefaultMeshDir()

def getDefaultGmshBin():
  import platform
  if platform.system() == 'Windows':
    default_gmsh_bin=os.path.join(os.environ['HOMEDRIVE'],os.environ['HOMEPATH'],'Softwares','GMSH','gmsh.exe');
  elif platform.system() == 'Darwin': # For OS X
    default_gmsh_bin=os.path.join(os.environ['HOME'],'GMSH','Gmsh.app','Contents','MacOS','gmsh');
  elif platform.system() == 'Linux':
    default_gmsh_bin=os.path.join(os.environ['HOME'],'bin','gmsh');
  else:
    default_gmsh_bin=''
  return default_gmsh_bin

def getDefaultMeshDir():
  userdir=getLocalDir()
  return op.join(userdir,'meshes')

def getDefaultGeoDir():
  fullname=op.dirname(op.abspath(__file__))
  Path=fullname[:fullname.rfind(os.sep)]
  #return os.path.join(fc_oogmsh.__path__[0],'geodir')
  return os.path.join(Path,'fc_oogmsh','geodir')
