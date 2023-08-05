import matplotlib.pyplot as plt
from fc_tools.Matplotlib import set_axes_equal,DisplayFigures,set_axes
import fc_matplotlib4mesh.simplicial as plt4sim
from fc_tools.colors import check_color,selectColors
from fc_tools.others import LabelBaseNameSimp
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
      #mlab.figure(name,**figure_options)
      plt.figure()
      #plt.title(name)
      colors=selectColors(len(ptags))
      LabName=LabelBaseNameSimp(Gh.dim,Gh.d,EltDesc['d'])
      Legend=[];Labels=[]
      for i in range(len(ptags)):
        q,me,toG=Gh.get_localmesh_PhysicalTag(Type,ptags[i])
        pm=plt4sim.plotmesh(q,me,color=colors[i])
        Legend.append(pm)
        Labels.append(r'$%s_{%d}$'%(LabName,ptags[i]))
      set_axes_equal()
      plt.legend(Legend,Labels,loc='best', ncol=int(len(Legend)/10)+1)
      plt.title(name)
      set_axes(plt.gca(),Gh.bbox)

def plot_elementary_tags(Gh):
  LType=[1,2,4] # Line, Triangle and Tetrahedron
  Legends=[]
  for Type in LType:
    EltDesc=get_elm_desc_by_type(Type)
    etags=Gh.get_ElementaryTags(Type)
    if etags is not None:
      name='Elementary tags for %s elements (type=%d)'%(EltDesc['desc'],EltDesc['elm_type'])
      #mlab.figure(name,**figure_options)
      plt.figure()
      #plt.title(name)
      colors=selectColors(len(etags))
      LabName=LabelBaseNameSimp(Gh.dim,Gh.d,EltDesc['d'])
      Legend=[];Labels=[]
      for i in range(len(etags)):
        q,me,toG=Gh.get_localmesh_ElementaryTag(Type,etags[i])
        pm=plt4sim.plotmesh(q,me,color=colors[i])
        Legend.append(pm)
        Labels.append(r'$%s_{%d}$'%(LabName,etags[i]))
      set_axes_equal()
      plt.legend(Legend,Labels,loc='best', ncol=int(len(Legend)/10)+1)
      plt.title(name)
      set_axes(plt.gca(),Gh.bbox)
    
