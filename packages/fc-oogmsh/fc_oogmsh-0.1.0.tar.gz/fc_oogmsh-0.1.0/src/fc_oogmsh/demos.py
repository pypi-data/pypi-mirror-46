import fc_oogmsh,sys

def demo01(**kwargs):
  # demo01(MshFileVersion='4.1')
  logfile=kwargs.pop('logfile',None)
  if logfile is not None:
     sys.stdout=open(logfile,"w")
  
  print('***********************')
  print('Running demo01 function')
  print('***********************')
  
  print('*** fc_oogmsh.buildmesh2d : 1st call')
  meshfile=fc_oogmsh.buildmesh2d('condenser11',25,force=True,verbose=3,**kwargs)
  print('*** fc_oogmsh.buildmesh2d : 2nd call')
  meshfile=fc_oogmsh.buildmesh2d('condenser11',25,force=True,**kwargs)
  print('*** fc_oogmsh.buildmesh2d : 3th call')
  meshfile=fc_oogmsh.buildmesh2d('condenser11',25,**kwargs)
  if logfile is not None:
    sys.stdout = sys.__stdout__
    
def demo02(**kwargs):
  # demo02(MshFileVersion='2.2')
  logfile=kwargs.pop('logfile',None)
  if logfile is not None:
     sys.stdout=open(logfile,"w")
  print('***********************')
  print('Running demo02 function')
  print('***********************')
  print('*** Build mesh file')
  MshFileVersion=kwargs.pop('MshFileVersion','4.1')
  meshfile=fc_oogmsh.buildmesh2d('condenser11',25,force=True,MshFileVersion=MshFileVersion,**kwargs)
  print('*** Read mesh file')
  if MshFileVersion=='2.2':
    oGh=fc_oogmsh.ooGmsh2(meshfile)
  else:
    oGh=fc_oogmsh.ooGmsh4(meshfile)
  print('*** Print oGh ->')
  print(oGh)
  
  
def demo03(**kwargs):
  print('***********************')
  print('Running demo03 function')
  print('***********************')
  print('*** Building the mesh')
  MshFileVersion=kwargs.pop('MshFileVersion','4.1')
  meshfile=fc_oogmsh.buildmesh2d('condenser11',25,MshFileVersion=MshFileVersion,**kwargs);
  print('*** Partitioning the mesh')
  pmfile=fc_oogmsh.buildpartmesh(meshfile,5,force=True,MshFileVersion=MshFileVersion,**kwargs);
  if MshFileVersion=='2.2':
    oGh=fc_oogmsh.ooGmsh2(pmfile)
  else:
    oGh=fc_oogmsh.ooGmsh4(pmfile)
  print('*** Print oGh ->')
  print(oGh)

  
def demo04(**kwargs):
  print('***********************')
  print('Running demo04 function')
  print('***********************')
  print('*** Build mesh file')
  MshFileVersion=kwargs.pop('MshFileVersion','4.1')
  pmfile=fc_oogmsh.buildpartrectangle(1,1,3,2,100,force=True, verbose=3,options='-string "Mesh.MetisAlgorithm=3;"',MshFileVersion=MshFileVersion,**kwargs)
  print('*** Read mesh file')
  if MshFileVersion=='2.2':
    oGh=fc_oogmsh.ooGmsh2(pmfile)
  else:
    oGh=fc_oogmsh.ooGmsh4(pmfile)
  print('*** Print oGh ->')
  print(oGh)
  
  
def demo05(**kwargs):
  print('***********************')
  print('Running demo05 function')
  print('***********************')
  print('*** Building the partitioned mesh')
  MshFileVersion=kwargs.pop('MshFileVersion','4.1')
  meshfile=fc_oogmsh.buildmesh2d('condenser11',25,force=True, options='-part 5', savemesh='./toto.msh',verbose=3,MshFileVersion=MshFileVersion,**kwargs);
  print('*** Reading the mesh file')
  if MshFileVersion=='2.2':
    oGh=fc_oogmsh.ooGmsh2(meshfile)
  else:
    oGh=fc_oogmsh.ooGmsh4(meshfile)
  print('*** Print oGh ->')
  print(oGh)
 
  
def demop(**kwargs):
  env=fc_oogmsh.Sys.environment()
  print('***********************')
  print('Running pdemo function')
  print('***********************')
  geofile=kwargs.pop('geofile','condenser.geo')
  MshFileVersion=kwargs.pop('MshFileVersion','4.1')
  fc_oogmsh.gmsh.check_MshFileVersion(MshFileVersion)
  meshdir=kwargs.get('meshdir',env.mesh_dir)
  N=kwargs.pop('N',4)
  d=kwargs.pop('d',2)
  verbose=kwargs.pop('verbose',1)
  np=kwargs.pop('np',5)
  geofile=fc_oogmsh.gmsh.checkgeofile(d,geofile)
  linesep='-'*50;
  print(linesep)
  print('  One step: GEO file -> MSH partitioned file ')
  print(linesep)  
  
  print('1. Building a partitioned mesh file by using :\n')
  print('   -> gmsh version : '+fc_oogmsh.gmsh.version())
  print('   -> geo file : '+geofile)
  print('   -> mesh file format : '+MshFileVersion)
  print('   -> number of partitions : %d'%np);
  pmfile=fc_oogmsh.gmsh.buildpartmesh(geofile,np,d=d,N=N,verbose=verbose,force=True,MshFileVersion=MshFileVersion,savedir=meshdir)
  print('   -> partitioned msh file : '+pmfile)
  print('2. Reading the partitioned mesh file')
  if MshFileVersion=='2.2':
    pGh=fc_oogmsh.ooGmsh2(pmfile)
  else:
    pGh=fc_oogmsh.ooGmsh4(pmfile)
  print(pGh)
  print('   -> Mesh file format: '+pGh.MeshFormat['version'])
  
  

def gdemo(**kwargs):
  print('***********************')
  print('Running gdemo function')
  print('***********************')
  geofile=kwargs.pop('geofile','condenser')
  MshFileVersion=kwargs.pop('MshFileVersion','4.1')
  show=kwargs.pop('show',True)
  fc_oogmsh.gmsh.check_MshFileVersion(MshFileVersion)
  N=kwargs.pop('N',5)
  d=kwargs.pop('d',2)
  assert d in [2,2.5,3],'d value must be 2, 2.5 or 3, given %d!'%d
  np=kwargs.pop('np',1)  # number of partitions (default 1: no partition)
  graphic=kwargs.pop('graphic','mayavi') # could be 'no','matplotlib' or 'mayavi'
  assert graphic.lower() in ['no','matplotlib' ,'mayavi']
  print('1. Building a mesh file by using :')
  print('   -> gmsh version %s'%fc_oogmsh.gmsh.version())
  print('   -> geo file : %s'%geofile)
  print('   -> mesh file format : %s'%MshFileVersion)
  meshfile=fc_oogmsh.buildmesh(d,geofile,N,MshFileVersion=MshFileVersion,force=True,verbose=1)
  print('   -> msh file : %s'%meshfile)
  print('2. Reading mesh file')
  if MshFileVersion=='2.2':
    Gh=fc_oogmsh.ooGmsh2(meshfile)
  else:
    Gh=fc_oogmsh.ooGmsh4(meshfile)
  print('   -> Mesh file format: %s'%Gh.MeshFormat['version']);
  if np==1:
    pGh=None
    num=3
  else:
    print('3. Building partitioned mesh file')
    print('   -> number of partitions : %d'%np)
    pmfile=fc_oogmsh.gmsh.buildpartmesh(meshfile,np,'verbose',1,'force',True,'MshFileVersion',MshFileVersion);
    print('   -> partitioned msh file : %s'%pmfile)
    print('4. Reading the partitioned mesh file')
    if MshFileVersion=='2.2':
      pGh=fc_oogmsh.ooGmsh2(pmfile)
    else:
      pGh=fc_oogmsh.ooGmsh4(pmfile)
    print('   -> Mesh file format: %s'%pGh.MeshFormat['version'])
    num=5
  if graphic.lower()=='mayavi':
    from mayavi import mlab
    from fc_oogmsh.Mayavi import plot_physical_tags,plot_elementary_tags
    mlab.close(all=True) 
    print('%d. Plotting Gh with Mayavi'%num)
    plot_physical_tags(Gh)
    plot_elementary_tags(Gh)
    if show:
      print('  Close Mayavi scenes to continue...')
      mlab.show(stop=True)
    
  elif graphic.lower()=='matplotlib':  
    import matplotlib.pyplot as plt
    from fc_oogmsh.Matplotlib import plot_physical_tags,plot_elementary_tags
    print('%d. Plotting Gh with Matplotlib'%num)
    plt.close('all')
    plt.ion()
    plot_physical_tags(Gh)
    plot_elementary_tags(Gh)
  return Gh

def seedemo(show):
  import matplotlib.pyplot as plt
  from fc_tools.Matplotlib import DisplayFigures
  if show:
    DisplayFigures()
    import time
    print('    Waiting 3s before closing ...')
    time.sleep(3)
  plt.close('all')
  
def alldemos01(show=False,**kwargs):
  def set_output_to_logfile(logfile):    
    if logfile is not None:
      sys.stdout=open(logfile,"a+")
  def set_output_to_stdout(logfile): 
    if logfile is not None:    
      sys.stdout.close()
      sys.stdout = sys.__stdout__
  
  logfile=kwargs.pop('logfile',None)
  for MshFileVersion in fc_oogmsh.gmsh.ListMshFileVersion:
    print('*** alldemos with MshFileVersion=%s'%MshFileVersion)
    for i in range(1,6):
      str_cmd='demo'+'%02d'%i+'(**kwargs,MshFileVersion=MshFileVersion)'
      print('  -> Running : '+str_cmd)
      set_output_to_logfile(logfile)
      eval(str_cmd)
      set_output_to_stdout(logfile)
    str_cmd='Gh=gdemo(geofile="condenser",d=2,N=10,MshFileVersion=MshFileVersion,graphic="matplotlib")'
    print('  -> Running : '+str_cmd)
    set_output_to_logfile(logfile)
    Gh=gdemo(geofile="condenser",d=2,N=10,MshFileVersion=MshFileVersion,graphic="matplotlib")
    seedemo(show)
    set_output_to_stdout(logfile)
    str_cmd='Gh=gdemo(geofile="demisphere4surf",d=2.5,N=10,MshFileVersion=MshFileVersion,graphic="matplotlib")'
    print('  -> Running : '+str_cmd)
    set_output_to_logfile(logfile)
    Gh=gdemo(geofile="demisphere4surf",d=2.5,N=10,MshFileVersion=MshFileVersion,graphic="matplotlib")
    seedemo(show)
    set_output_to_stdout(logfile)
    str_cmd="Gh=gdemo(geofile='cylinderkey',d=3,N=10,MshFileVersion=MshFileVersion,graphic='matplotlib')"
    print('  -> Running : '+str_cmd)
    set_output_to_logfile(logfile)
    Gh=gdemo(geofile='cylinderkey',d=3,N=10,MshFileVersion=MshFileVersion,graphic='matplotlib')
    seedemo(show)
    set_output_to_stdout(logfile)
    str_cmd="Gh=gdemo(geofile='condenser',d=2,N=10,MshFileVersion=MshFileVersion,graphic='mayavi',show=False)"
    print('  -> Running : '+str_cmd)
    set_output_to_logfile(logfile)
    Gh=gdemo(geofile='condenser',d=2,N=10,MshFileVersion=MshFileVersion,graphic='mayavi',show=False)
    set_output_to_stdout(logfile)
    str_cmd="Gh=gdemo(geofile='demisphere4surf',d=2.5,N=10,MshFileVersion=MshFileVersion,graphic='mayavi',show=False)"
    print('  -> Running : '+str_cmd)
    set_output_to_logfile(logfile)
    Gh=gdemo(geofile='demisphere4surf',d=2.5,N=10,MshFileVersion=MshFileVersion,graphic='mayavi',show=False)
    set_output_to_stdout(logfile)
    str_cmd="Gh=gdemo(geofile='cylinderkey',d=3,N=10,MshFileVersion=MshFileVersion,graphic='mayavi',show=False)"
    print('  -> Running : '+str_cmd)
    set_output_to_logfile(logfile)
    Gh=gdemo(geofile='cylinderkey',d=3,N=10,MshFileVersion=MshFileVersion,graphic='mayavi',show=False)
    set_output_to_stdout(logfile)

def set_output_to_logfile(logfile):    
  if logfile is not None:
    sys.stdout=open(logfile,"a+")
    
def set_output_to_stdout(logfile): 
  if logfile is not None:    
    sys.stdout.close()
    sys.stdout = sys.__stdout__

def check_run(strfun,logfile,stop=False):
  valid=True
  fun=eval('lambda: '+strfun)
  try:
    set_output_to_logfile(logfile)
    fun()
  except:
    valid=False
    if stop:
      raise NameError('\n[fc_oogmsh]Stop! running %s FAILED!\n\n'%strfun)
  set_output_to_stdout(logfile)
  return valid

def close_all(graphic):
  if graphic.lower()=='mayavi':
    from mayavi import mlab
    from fc_oogmsh.Mayavi import plot_physical_tags,plot_elementary_tags
    mlab.close(all=True) 
  elif graphic.lower()=='matplotlib':  
    import matplotlib.pyplot as plt
    from fc_oogmsh.Matplotlib import plot_physical_tags,plot_elementary_tags
    plt.close('all')
    
def save_all(graphic,filename,directory):
  if graphic.lower()=='mayavi':
    from fc_tools.Mayavi import SaveAllFigsAsFiles
  #  SaveAllFigsAsFiles(filename,dir=directory,tag=True)
  elif graphic.lower()=='matplotlib':  
    from fc_tools.Matplotlib import SaveAllFigsAsFiles
  SaveAllFigsAsFiles(filename,dir=directory,tag=True)
    
def alldemos(show=False,**kwargs):
  import numpy
  
  logfile=kwargs.pop('logfile',None)
  save=kwargs.pop('save',False)
  MSHformats=fc_oogmsh.gmsh.getMSHfile_formats()
  graphics=['matplotlib','mayavi']
  setsample=lambda name,d,N,np: dict(name=name,d=d,N=N,np=np)
  samples=[setsample('condenser.geo',2,10,5),setsample('demisphere5.geo',2.5,6,5),setsample('cylinderkey.geo',3,6,5)]
  
  N=3*len(MSHformats)*len(samples)
  valids=numpy.ones((N,), dtype=bool)
  expected_valids=numpy.ones((N,), dtype=bool)
  titles=[]
  strfuns=[]
  k=0
  allisOK=True
  for sample in samples:
    # gdemo
    for graphic in graphics:
      for MSHformat in MSHformats:
        strfun="fc_oogmsh.demos.gdemo(geofile='"+sample['name']+"',d=%g,N=%d"%(sample['d'],sample['N'])+",graphic='"+graphic+"',show=False,MshFileVersion='"+MSHformat['format']+"')"
        strfuns.append(strfun)
        #fun=eval('lambda: '+strfun)
        resume="MSH format=%s, geofile='%s', d=%g, N=%d, graphic='%s'"%(MSHformat['format'],sample['name'],sample['d'],sample['N'],graphic)
        titles.append('gdemo with '+resume)
        valids[k]=check_run(strfun,logfile)
        expected_valids[k]=fc_oogmsh.gmsh.isGoodMshFormatVersion(MSHformat['format'])
        s='OK' if valids[k] else 'FAILED'
        print('[fc-oogmsh] %8s : running %s'%(s,titles[k]))
        if valids[k]!=expected_valids[k] :
          print('   -> RESULT NOT EXPECTED : FAILED...FAILED')
          allisOK=False
        if save:
          if valids[k]:
            #import fc_tools
            directory='figures'
            #fc_tools.others.mkdir_p(figures)
            filename='figure_'+str(sample['d']).replace('.','')+'_'+graphic+'_msh'+MSHformat['format'].replace('.','')+'_gmsh'+fc_oogmsh.gmsh.version().replace('.','') #+'_python'+fc_tools.Sys.getSoftware()[1].replace('.','')
            save_all(graphic,filename,directory)
        k+=1
        close_all(graphic)
    
    # demop
    for MSHformat in MSHformats:
      strfun="fc_oogmsh.demos.demop(geofile='"+sample['name']+"',d=%g,N=%d,np=%d"%(sample['d'],sample['N'],sample['np'])+",MshFileVersion='"+MSHformat['format']+"')"
      strfuns.append(strfun)
      fun=eval('lambda: '+strfun)
      resume='MSH format=%s, geofile=''%s'', d=%g, N=%d, np=%d'%(MSHformat['format'],sample['name'],sample['d'],sample['N'],sample['np'])
      titles.append('demop with '+resume)
      valids[k]=check_run(strfun,logfile)
      expected_valids[k]=fc_oogmsh.gmsh.isGoodMshFormatVersion(MSHformat['format'])
      s='OK' if valids[k] else 'FAILED'
      print('[fc-oogmsh] %8s : running %s'%(s,titles[k]))
      if valids[k]!=expected_valids[k] :
        print('   -> RESULT NOT EXPECTED : FAILED...FAILED')
        allisOK=False
      k+=1
  return allisOK
