from mayavi import mlab
from fc_tools.Mayavi import fc_legend
import fc_mayavi4mesh.simplicial as mlab4sim
from fc_tools.colors import check_color,selectColors
from fc_oogmsh.gmsh import get_elm_desc_by_type
figure_options={'size': (600,600)}  

def plot_physical_tags(Gh):
  LType=[1,2,4] # Line, Triangle and Tetrahedron
  Legends=[]
  for Type in LType:
    EltDesc=get_elm_desc_by_type(Type)
    ptags=Gh.get_PhysicalTags(Type)
    if ptags is not None:
      name='Physical tags for %s elements (type=%d)'%(EltDesc['desc'],EltDesc['elm_type'])
      mlab.figure(name,**figure_options)
      colors=selectColors(len(ptags))
      for i in range(len(ptags)):
        q,me,toG=Gh.get_localmesh_PhysicalTag(Type,ptags[i])
        mlab4sim.plotmesh(q,me,color=colors[i])
      L=fc_legend(ptags,colors,EltDesc['d'])
      Legends.append(L)
      if Gh.dim==2:  mlab.view(0,0)
    
def plot_elementary_tags(Gh):
  LType=[1,2,4] # Line, Triangle and Tetrahedron
  Legends=[]
  for Type in LType:
    EltDesc=get_elm_desc_by_type(Type)
    ptags=Gh.get_ElementaryTags(Type)
    if ptags is not None:
      name='Elementary tags for %s elements (type=%d)'%(EltDesc['desc'],EltDesc['elm_type'])
      mlab.figure(name,**figure_options)
      #mlab.title('Elementary tags for %s elements (type=%d)'%(EltDesc['desc'],EltDesc['elm_type']))
      colors=selectColors(len(ptags))
      for i in range(len(ptags)):
        q,me,toG=Gh.get_localmesh_ElementaryTag(Type,ptags[i])
        mlab4sim.plotmesh(q,me,color=colors[i])
         
      L=fc_legend(ptags,colors,EltDesc['d'])
      Legends.append(L)
      if Gh.dim==2:  mlab.view(0,0)    
  return Legends
