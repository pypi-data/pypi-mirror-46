# Copyright (C) 2017-2019 F. Cuvelier
# License: GNU GPL version 3
__version__='0.1.0' # automaticaly written by setpackages.py script
__packages__={'fc-tools': '0.0.22', 'fc-meshtools': '0.1.0', 'fc-matplotlib4mesh': '0.1.0', 'fc-mayavi4mesh': '0.1.0'} # automaticaly written by setpackages.py script

from .demos import *
from .Sys import configure,printenv
from .oogmsh2 import ooGmsh2,isooGmsh2
from .oogmsh4 import ooGmsh4,isooGmsh4
from .gmsh import buildmesh,buildmesh2d,buildmesh3d,buildmesh3ds,buildpartmesh,buildpartrectangle

from fc_tools.others import isModuleFound
if isModuleFound('fc_matplotlib4mesh'):
  from . import Matplotlib
if isModuleFound('fc_mayavi4mesh'):
  from . import Mayavi

def gitinfo():
  return {'name': 'fc-oogmsh', 'tag': '0.1.0', 'commit': '012e216860f343dda3c522728501de05dae065ac', 'date': '2019-05-07', 'time': '09-46-26', 'status': '0'} # automatically updated
  if len(inf)>0: 
    return inf
  # Only for developpers
  import fc_tools,os
  D=os.path.realpath(os.path.join(__path__[0],os.path.pardir))
  if os.path.basename(D)=='src':
    D=os.path.realpath(os.path.join(D,os.path.pardir))
  return fc_tools.git.get_info(D)
