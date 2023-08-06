from tvtk.api import tvtk
from mayavi import mlab
import numpy as np

from fc_tools.others import LabelBaseName,simplicial_dimension,merge_two_dicts
from fc_tools.colors import check_color,selectColors
from fc_tools.graphics import Plane

import fc_meshtools.simplicial as msimp
from fc_meshtools.utils import cutMeshElements

def plotmesh(q,me,**kwargs):
  """
  mesh plotting
  
  Parameters
  ----------
    q : mesh vertices, dim-by-nq or nq-by-dim numpy array where
        dim is the space dimension (2 or 3) and nq the number of vertices.
    me: mesh elements connectivity array where elements are d-simplices. 
        me is a (d+1)-by-nme or nme-by-(d+1) numpy array where nme is the number 
        of mesh elements and d is the simplicial dimension:
          d=0: points, 
          d=1: lines, 
          d=2: triangle, 
          d=3: tetrahedron
                  
  Returns
  -------
    handles: 
        
  """
  kind=kwargs.pop('kind', 'simplicial')
  kwargs['color']=check_color(kwargs.pop('color', 'Blue'))
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    move=kwargs.pop('move',None)
    Q=move_mesh(q,move);ME=me
    indices=kwargs.pop('indices',None)
    if indices is not None:
      Q,ME=msimp.submesh(Q,ME,indices)  
    return eval("_plotmesh_SubTh"+str(d)+"simp"+str(dim)+"D(Q,ME,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def plot(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    return eval("_plot_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'
  
def plotiso(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert d==2
    return eval("_plotiso_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def slicemesh(q,me,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim==3 and d==3
    return eval("_slicemesh_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def slice(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim==3 and d==3
    return eval("_slice_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def sliceiso(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim==3 and  d==3
    return eval("_sliceiso_SubTh"+str(d)+"simp"+str(dim)+"D(q,me,u,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def quiver(q,me,V,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim>=2
    return _quiver_simp(q,V,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'
  
def volume(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  scalars_name=kwargs.pop('scalars_name', 'scalar_volume')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim==3 and d==3, 'dim=%d and d=%d'%(dim,d)
    ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=scalars_name)
    return mlab.pipeline.volume(ug,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'
  
  
def slice_unstructured_grid(*args,**kwargs):
  assert len(args) in [1,2,3]
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  w_enabled=kwargs.pop('w_enabled',False) # Widget enabled
  property=kwargs.pop('property',{})
  if 'color' in property:
    property['color']=check_color(property['color'])
  if 'edge_color' in property:
    property['edge_color']=check_color(property['edge_color'])  
  if len(args)==1:
    obj=args[0]
    parent=get_UnstructuredGrid_from_parent(obj)
    assert parent is not None, 'Unable to find tvtk UnstructuredGrid in input object'
    sug=mlab.pipeline.slice_unstructured_grid(parent,**kwargs)
  else:
    q=args[0];me=args[1];
    if len(args)==3:
      u=args[2]
      scalars_name=kwargs.pop('scalars_name', 'scalar_volume')
      
    kind=kwargs.pop('kind', 'simplicial')
    if kind=='simplicial':
      dim,d,nq,nme=msimp.get_dims(q,me)
      assert dim==3 and d==3, 'dim=%d and d=%d'%(dim,d)
      if len(args)==3:
        ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=scalars_name)
      else:
        ug=_UnstructuredGrid(q,me)
      sug=mlab.pipeline.slice_unstructured_grid(ug,**kwargs)
    else:
      assert False,'Not yet implemented for '+kind+' mesh elements'
  sug.implicit_plane.widget.enabled = w_enabled
  if normal is not None:
    sug.implicit_plane.plane.normal=sug.implicit_plane.widget.normal=normal
  if origin is not None:  
    sug.implicit_plane.plane.origin=sug.implicit_plane.widget.origin=origin  
  sug.actor.property.trait_set(**property)
  return sug

def vectors(q,me,V,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  scalars=kwargs.pop('scalars', None)
  scalars_name=kwargs.pop('scalars_name', 'scalars')
  vectors_name=kwargs.pop('vectors_name', 'vectors')
  if kind=='simplicial':
    
    if q.shape[0]==2:
      q=np.vstack((q,np.zeros((1,q.shape[1]))))
    if V.shape[0]==2:  
      V=np.vstack((V,np.zeros((1,V.shape[1]))))
    dim,d,nq,nme=msimp.get_dims(q,me)
    ug_options={'vectors':V,'vectors_name':vectors_name}
    if scalars is not None:
      assert scalars.shape==(nq,) or scalars.shape==(1,nq)
      ug_options['scalars']=scalars
      ug_options['scalars_name']=scalars_name
    ug=_UnstructuredGrid(q,me,**ug_options)
    return mlab.pipeline.vectors(ug,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'

  
def iso_surface(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim==3 and d==3
    return _iso_surface_SubTh3simp3D(q,me,u,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'

def streamline(q,me,u,V,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim==3 and d==3
    return _streamline_SubTh3simp3D(q,me,u,V,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'
  
default_node_property= {'color':check_color('Black'),
                        'frame_color':check_color('Black'),
                        'background_color':check_color('White'),
                        'background_opacity':0,
                        'line_offset':2,
                        'line_spacing':2,
                        'justification':'centered',
                        'vertical_justification':'centered',
                        'bold':False,
                        'italic':False,
                        'shadow':False,
                        'frame':True }
  
def plot_node_indices(q,**kwargs):
  property=merge_two_dicts(default_node_property,kwargs.pop('property', default_node_property))
  indices=kwargs.pop('indices', None)
  toGlobal=kwargs.pop('toGlobal', None)
  assert len(kwargs)==0, 'Unknown options : %s'%str(kwargs)
  nq=q.shape[1]
  if indices is None:
    indices=np.arange(nq)
    Q=q
  else:
    Q=q[:,indices]
  if toGlobal is not None:
    assert toGlobal.shape[0]==nq
    ug=_UnstructuredGrid(Q,None,scalars=toGlobal[indices])
  else:  
    ug=_UnstructuredGrid(Q,None,scalars=indices)
  lab=mlab.pipeline.labels(ug)
  lab.mapper.label_mode='label_scalars'
  lab.number_of_labels=Q.shape[1]
  lab.visible_points.enabled=True
  lab.property.trait_set(**property)
  return lab

default_element_property={'color':check_color('Black'),
                         'frame_color':check_color('Black'),
                         'background_color':check_color('GhostWhite'),
                         'background_opacity':0,
                         'line_offset':2,
                         'line_spacing':2,
                         'justification':'centered',
                         'vertical_justification':'centered',
                         'bold':False,
                         'italic':False,
                         'shadow':False,
                         'frame':False }

def plot_element_indices(q,me,**kwargs):
  property=merge_two_dicts(default_element_property,kwargs.pop('property', default_element_property))
  indices=kwargs.pop('indices', None)
  visible_enabled=kwargs.pop('visible_enabled', False)
  mesh_color=check_color(kwargs.pop('mesh_color', 'k'))
  assert len(kwargs)==0, 'Unknown options : %s'%str(kwargs)
  nme=me.shape[1]
  if indices is None:
    indices=np.arange(nme)
    ME=me
  else:
    ME=me[:,indices]
  Ba=msimp.barycenters(q,ME)
  ug=_UnstructuredGrid(Ba,None,scalars=indices)
  lab=mlab.pipeline.labels(ug)
  lab.mapper.label_mode='label_scalars'
  lab.visible_points.enabled=True
  lab.number_of_labels=ME.shape[1]
  #property={'color':color,'frame_color':color,'justification':'centered','vertical_justification':'centered'}
  lab.property.trait_set(**property)
  if visible_enabled:
    pm=plotmesh(q,ME,color=mesh_color)
    return lab,pm
  return lab

def plot_mesh_indices(q,me,**kwargs):
  elt_indices=kwargs.pop('element_indices', None)
  node_indices=kwargs.pop('node_indices', None)
  visible_enabled=kwargs.pop('visible_enabled', False)
  mesh_color=check_color(kwargs.pop('mesh_color', 'k'))
  element_property=kwargs.pop('element_property', default_element_property)
  node_property=kwargs.pop('node_property', default_node_property)
  assert len(kwargs)==0, 'Unknown options : %s'%str(kwargs)
  nme=me.shape[1]
  if elt_indices is None:
    if node_indices is None:
      elt_indices=np.arange(nme)
      node_indices=np.unique(me.flatten())
    else: 
      elt_indices=np.arange(nme)[np.any(np.isin(me,node_indices),axis=0)] # find elements containing at least one point with index in node_indices
  else:
    if node_indices is None:
      node_indices=np.unique(me[:,elt_indices].flatten())
  
  pvn=plot_node_indices(q,indices=node_indices,property=node_property)
  if visible_enabled:
    pen,pm=plot_element_indices(q,me,indices=elt_indices,property=element_property,visible_enabled=True)
    return pvn,pen,pm
  else:
    pen=plot_element_indices(q,me,indices=elt_indices,property=element_property)
    return pvn,pen
      
def plot_normal_faces(q,me,**kwargs):
  Colors=kwargs.pop('colors',selectColors(me.shape[0],backgrounds=np.array([list(check_color('LightGray')),[1,1,1],[0,0,0]])))
  indices=kwargs.pop('indices', None)
  Ba=kwargs.pop('barycenters', None)
  Normal=kwargs.pop('normals', None)
  visible_enabled=kwargs.pop('visible_enabled', False)
  mesh_color=check_color(kwargs.pop('mesh_color', 'k'))
  nq=q.shape[1]
  nme=me.shape[1]
  if q.shape[0]==2:
    q=np.vstack((q,np.zeros((1,nq))))
  if indices is None:
    indices=np.arange(nme)
    ME=me;Q=q
  else:
    Q,ME=msimp.submesh(q,me,indices)
  nQ=Q.shape[1];nME=ME.shape[1]  
  if Ba is None:
    Ba=msimp.barycenters(Q,ME)
  if Normal is None:
    G=msimp.GradBaCo(Q,ME)
    Normal=msimp.NormalFaces(Q,ME,G)  
  if Ba.shape[1] != nME:
    assert Ba.shape[1]==nme
    Ba=Ba[:,indices]
  if Ba.shape[0]==2:
    Ba=np.vstack((Ba,np.zeros((1,nME))))
  if Normal.shape[2] != nME:
    assert Normal.shape[2]==nme
    Normal=Normal[:,:,indices]
  if Normal.shape[1]==2:
    N=np.zeros((Normal.shape[0],3,Normal.shape[2]))
    N[:,:2,:]=Normal
    Normal=N
    
  h=msimp.GetMaxLengthEdges(Q,ME)
  QBa=np.hstack((Q,Ba))
  nba=np.arange(ME.shape[1])+Q.shape[1]
  mv=[None]*ME.shape[0];sf=[None]*ME.shape[0]
  for i in range(ME.shape[0]):
    ug=_UnstructuredGrid(Ba,None,vectors=Normal[i,:,:],vectors_name='Normal[%d]'%i)
    mv[i]=mlab.pipeline.vectors(ug)
    mv[i].glyph.color_mode='no_coloring'
    mv[i].glyph.glyph.scale_factor=h/4
    mv[i].actor.property.color=tuple(Colors[i])
    mv[i].actor.property.line_width=3
    ug=_UnstructuredGrid(QBa,np.vstack((ME[i],nba)),d=1)
    sf[i]=mlab.pipeline.surface(ug,color=tuple(Colors[i]),opacity=0.3)
  if visible_enabled:
    pm=plotmesh(Q,ME,color=mesh_color)
    return mv,sf,pm
  return mv,sf

def get_cell_type(d):
  if d==1:
    return tvtk.Line().cell_type
  if d==2:
    return tvtk.Triangle().cell_type
  if d==3:
    return tvtk.Tetra().cell_type
  assert False, "Unknow cell_type for %d-simplicial element"%d

def move_mesh(q,U):
  if U is None:
    return q
  if isinstance(U,list):
    U=np.array(U).T
  assert U.shape==q.shape
  return q+U 

#
# private functions
#
def _plotmesh_SubTh1simp2D(q,me,**kwargs):
  lighting=kwargs.pop('lighting', False)
  z=kwargs.pop('z',np.zeros((q.shape[1],)))
  ug=_UnstructuredGrid(np.vstack((q,z)),me)
  sf=mlab.pipeline.surface(ug,**kwargs)
  sf.actor.property.lighting=lighting
  return sf

def _plotmesh_SubTh2simp2D(q,me,**kwargs):
  lighting=kwargs.pop('lighting', False)
  representation=kwargs.pop('representation','wireframe')
  kwargs['representation']=representation  
  z=kwargs.pop('z',np.zeros((q.shape[1],)))
  tm1=mlab.triangular_mesh(q[0],q[1],z.flatten(),me.T,**kwargs)
  tm1.actor.property.lighting=lighting
  return tm1
    
def _plotmesh_SubTh1simp3D(q,me,**kwargs):
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  ug=_UnstructuredGrid(q,ME,d=1)
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf
  
def _plotmesh_SubTh2simp3D(q,me,**kwargs):
  representation=kwargs.get('representation', 'wireframe') # or 'points' or 'surface'
  lighting=kwargs.pop('lighting',False)
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  
  color=kwargs.pop('color',(0,0,1))
  ug=_UnstructuredGrid(q,ME,d=2)
  edge_visibility=kwargs.pop('edge_visibility',False)
  edge_color=check_color(kwargs.pop('edge_color',(0,0,0)))
  defaut_prop={'edge_color':edge_color, 'edge_visibility': edge_visibility,
                                  'color': color,'representation':representation,
                                  'lighting':lighting}
  property=merge_two_dicts(defaut_prop,kwargs.pop('property',{}))
  sf=mlab.pipeline.surface(ug,**kwargs)
  sf.actor.property.trait_set(**property)
  return sf

def _plotmesh_SubTh3simp3D(q,me,**kwargs):
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  ug=_UnstructuredGrid(q,ME)
  sf=mlab.pipeline.surface(ug,opacity=0.1)
  sf2=mlab.pipeline.surface(mlab.pipeline.extract_edges(sf), **kwargs )
  return sf2

def _plot_SubTh1simp2D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  plane=kwargs.pop('plane', True )
  
  ug=_UnstructuredGrid(q,me,scalars=U,scalars_name=name,plane=plane)
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf 
  
def _plot_SubTh2simp2D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  plane=kwargs.pop('plane', True )
  lighting=kwargs.pop('lighting', False )
  property=merge_two_dicts({'lighting':lighting},kwargs.pop('property',{}))
  ug=_UnstructuredGrid(q,me,scalars=U,scalars_name=name,plane=plane)
  sf=mlab.pipeline.surface(ug,**kwargs)
  sf.actor.property.trait_set(**property)
  return sf 
  
def _plot_SubTh1simp3D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  ug=_UnstructuredGrid(q,me,scalars=U,scalars_name=name,d=1)
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf 
 
def _plot_SubTh2simp3D(q,me,U,**kwargs):
  lighting=kwargs.pop('lighting', False )
  name=kwargs.pop('scalars_name', 'unknown' )
  ug=_UnstructuredGrid(q,me,scalars=U,scalars_name=name)
  sf=mlab.pipeline.surface(ug,**kwargs)
  return sf

def _plot_SubTh3simp3D(q,me,U,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  ug=_UnstructuredGrid(q,me,scalars=U,scalars_name=name)
  sf=mlab.pipeline.surface(mlab.pipeline.extract_edges(ug),**kwargs)
  return sf

def _plotiso_SubTh2simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  N=kwargs.pop('N',10) # number of contours
  color=check_color(kwargs.pop('color', None))
  if color is not None:
    kwargs['color']=color
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  if isinstance(contours,np.ndarray):
    contours=list(contours)
  ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf 

def _plotiso_SubTh2simp2D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  #cmap=kwargs.pop('cmap', 'blue-red')
  vmin=kwargs.get('vmin', min(u));kwargs['vmin']=vmin
  vmax=kwargs.get('vmax', max(u));kwargs['vmax']=vmax
  N=kwargs.pop('N',10) # number of contours
  color=kwargs.pop('color', None)
  if color is not None:
    kwargs['color']=check_color(color)
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  if isinstance(contours,np.ndarray):
    contours=list(contours)
  plane=kwargs.pop('plane', True )
  ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=name,plane=plane)
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf

  
def _slice_SubTh3simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  w_enabled=kwargs.pop('w_enabled',False) # Widget enabled
  ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  scp=mlab.pipeline.scalar_cut_plane(ug,**kwargs)
  scp.implicit_plane.widget.enabled = w_enabled
  if normal is not None:
    scp.implicit_plane.plane.normal=scp.implicit_plane.widget.normal=normal
  if origin is not None:
    scp.implicit_plane.plane.origin=scp.implicit_plane.widget.origin=origin
  return scp

def _sliceiso_SubTh3simp3D(q,me,u,**kwargs):
  contours=kwargs.pop('contours',10) 
  name=kwargs.pop('scalars_name', 'unknown' )
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  w_enabled=kwargs.pop('w_enabled',False) # Widget enabled
  color=check_color(kwargs.pop('color', None))
  if color is not None:
    kwargs['color']=color
    
  ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  scp=mlab.pipeline.scalar_cut_plane(ug,**kwargs)
  
  if normal is not None:
    scp.implicit_plane.plane.normal=scp.implicit_plane.widget.normal=normal
  if origin is not None:
    scp.implicit_plane.plane.origin=scp.implicit_plane.widget.origin=origin
  
  scp.contour.number_of_contours=contours
  scp.enable_contours=True
  scp.implicit_plane.widget.enabled = w_enabled
  return scp
  
def _slicemesh_SubTh3simp3D(q,me,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  normal=kwargs.pop('normal',None) 
  origin=kwargs.pop('origin',None)
  color=check_color(kwargs.pop('color', (0,0,1)))
  w_enabled=kwargs.pop('w_enabled',False)
  ug=_UnstructuredGrid(q,me)
  scp=mlab.pipeline.scalar_cut_plane(ug,color=color,**kwargs)
  scp.implicit_plane.widget.enabled = w_enabled # first : due to BUG with normal??
  if normal is not None:
    scp.implicit_plane.plane.normal=scp.implicit_plane.widget.normal=normal
  if origin is not None:
    scp.implicit_plane.plane.origin=scp.implicit_plane.widget.origin=origin
  return scp

def _streamline_SubTh3simp3D(q,me,u,V,**kwargs):
  scalars_name=kwargs.pop('scalars_name', 'scalar data' )
  vectors_name=kwargs.pop('vectors_name', 'vector data' )
  seed_options=kwargs.pop('seed_options', None)
  seed_widget_options=kwargs.pop('seed_widget_options', None)
  streamtracer_options=kwargs.pop('streamtracer_options', None)
  ug=_UnstructuredGrid(q,me,scalars=u,vectors=V,scalars_name=scalars_name,vectors_name=vectors_name)
  sf=mlab.pipeline.streamline(ug,**kwargs)
  if seed_options is not None:
    sf.seed.trait_set(**seed_options)
  if streamtracer_options is not None:
    sf.stream_tracer.trait_set(**streamtracer_options)
  if seed_widget_options is not None:
    sf.seed.widget.trait_set(**seed_widget_options)
  e=sf.seed.widget.enabled
  sf.seed.widget.enabled=0
  sf.seed.widget.enabled=1
  sf.seed.widget.enabled=e
  return sf

def _quiver_simp(q,V,**kwargs):
  dim=q.shape[0]
  assert dim>=2
  scalars=kwargs.get('scalars', None )
  name=kwargs.pop('name', None)
  color=kwargs.pop('color', None)
  if color is not None:
    kwargs['color']=check_color(color)
  if scalars is None:
    Norm=np.sqrt(np.sum(V**2,axis=0))
    vmin=min(Norm);vmax=max(Norm)
  else:
    vmin=min(scalars);vmax=max(scalars)
  vmin=kwargs.pop('vmin',vmin)
  kwargs['vmin']=vmin
  vmax=kwargs.pop('vmax',vmax)
  kwargs['vmax']=vmax
  if name is None:
    kwargs['name']='quiver: dim=%d'%(dim)
  if dim==3:
    z=q[2]
    Vz=V[2]
  else:
    z=np.zeros((q.shape[1],))
    Vz=z
  mq=mlab.quiver3d(q[0],q[1],z,V[0],V[1],Vz,**kwargs)
  if scalars is not None:
    color_mode=kwargs.pop('color_mode', 'color_by_scalar' )
    mq.glyph.color_mode=color_mode
  else: # bug with vmin, vmax in mlab.quiver3d?
    mq.glyph.mask_input_points=True
    mq.module_manager.vector_lut_manager.data_range=np.array([vmin,vmax])
    mq.module_manager.vector_lut_manager.use_default_range=False
  return mq

def _iso_surface_SubTh3simp3D(q,me,u,**kwargs):
  name=kwargs.pop('scalars_name', 'unknown' )
  N=kwargs.pop('N',10) # number of contours
  color=check_color(kwargs.pop('color', None))
  if color is not None:
    kwargs['color']=color
  contours=kwargs.pop('contours', list(np.linspace(min(u),max(u),N)))
  if isinstance(contours,np.ndarray):
    contours=list(contours)
  ug=_UnstructuredGrid(q,me,scalars=u,scalars_name=name)
  sf=mlab.pipeline.iso_surface(ug,contours=contours,**kwargs)
  return sf

def _UnstructuredGrid(q,me=None,**kwargs):
  scalars=kwargs.get('scalars', None )
  scalars_name=kwargs.get('scalars_name', 'scalar data' )
  vectors=kwargs.get('vectors', None )
  vectors_name=kwargs.get('vectors_name', 'vector data' )
  plane=kwargs.pop('plane', True )
  d=kwargs.pop('d', None)
  
  dim,nq=q.shape
  if (dim==2):
    if (scalars is None) or (plane):
      Z=np.zeros((1,nq))
    else:
      Z=scalars.reshape((1,nq))
    q=np.vstack((q,Z))
    if vectors is not None:
      if vectors.shape[0]==2:
        vectors=vectors.T
  
  ug = tvtk.UnstructuredGrid(points=q.T) # points value: shape[1] must be 3
  if me is not None:
    if d is None:
      d=me.shape[0]-1
    ug.set_cells(get_cell_type(d), me.T) # 
  if scalars is not None:
    ug.point_data.scalars = scalars
    ug.point_data.scalars.name=scalars_name
  if vectors is not None:
    if vectors.shape[0]==3:
      vectors=vectors.T
    ug.point_data.vectors = vectors
    ug.point_data.vectors.name=vectors_name
  return ug

def get_UnstructuredGrid_from_parent(obj):
  import tvtk
  par=obj
  while par is not None:
    if hasattr(par,'parent'):
      par=par.parent
      if hasattr(par,'data'):
        if isinstance(par.data,tvtk.tvtk_classes.unstructured_grid.UnstructuredGrid):
          return par
    else:
      par=None
     
