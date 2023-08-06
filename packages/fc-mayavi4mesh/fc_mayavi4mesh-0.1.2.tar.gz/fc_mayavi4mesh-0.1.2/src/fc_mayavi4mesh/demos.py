import numpy as np
import os
from mayavi import mlab
from fc_meshtools import simplicial as mshsim
import fc_mayavi4mesh.simplicial as mlab4sim
from fc_tools.colors import check_color

figure_options={'size': (600,600)}

def plotmesh2D(show=True):
  q2,me2,toG2=mshsim.getMesh2D(2)
  q1,me1,toG1=mshsim.getMesh2D(1)
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2)
  mlab.view(0,0)
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q1,me1,color='Red',line_width=2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab.view(0,0)
  if show:
    mlab.show()
  
  
def plotmesh3D(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q3,me3)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2)
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='Red')
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2)
  mlab.figure(3,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.02)
  mlab4sim.plotmesh(q1,me1,color='Magenta',line_width=2)
  from fc_tools.graphics import Plane
  P=[Plane(origin=[0,0,1],normal=[0,0,-1]), Plane(origin=[0,0,1],normal=[0,-1,-1])]
  mlab.figure(4,**figure_options)
  mlab4sim.plotmesh(q3,me3,cut_planes=P,color='DarkGrey')
  mlab4sim.plotmesh(q2,me2,cut_planes=P)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.view(-146,67,6)
  if show:
    mlab.show()
  
def plotmesh3Ds(show=True):
  q2,me2,toG2=mshsim.getMesh3Ds(2)
  q1,me1,toG1=mshsim.getMesh3Ds(1)
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='Red')
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.02)
  mlab4sim.plotmesh(q1,me1,color='Magenta',line_width=2)
  if show:
    mlab.show()

def plot2D(show=True):
  q2,me2,toG2=mshsim.getMesh2D(2)
  q1,me1,toG1=mshsim.getMesh2D(1)
  f=lambda x,y: 2*np.sin(np.sqrt(x**2+y**2))*np.cos(x)*np.sin(y)
  u2=f(q2[0],q2[1])
  u1=f(q1[0],q1[1])
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.view(0,0)
  mlab.figure(2,**figure_options)
  mlab4sim.plot(q1,me1,u1,line_width=2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(3,**figure_options)
  mlab4sim.plot(q2,me2,u2,plane=False)
  mlab4sim.plotmesh(q1,me1,z=u1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(4,**figure_options)
  mlab4sim.plot(q1,me1,u1,line_width=2,plane=False)
  mlab4sim.plotmesh(q2,me2,z=u2,color='LightGray',opacity=0.1)
  mlab.colorbar()
  if show:
    mlab.show()
  
def plot3D(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[0],q3[1],q3[2])
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plot(q3,me3,u3)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(3,**figure_options)
  mlab4sim.plot(q1,me1,u1,line_width=2,vmin=min(u3),vmax=max(u3))
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.02)
  mlab.colorbar()
  if show:
    mlab.show()
  
def plot3Ds(show=True):
  q2,me2,toG2=mshsim.getMesh3Ds(2)
  q1,me1,toG1=mshsim.getMesh3Ds(1)
  f=lambda x,y,z: np.cos(3*x-1)*np.sin(2*y-2)*np.sin(3*z)
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plot(q1,me1,u1,line_width=2,vmin=min(u2),vmax=max(u2))
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab.colorbar()
  if show:
    mlab.show()
  
def plotiso2D01(show=True):
  q2,me2,toG2=mshsim.getMesh2D(2)
  q1,me1,toG1=mshsim.getMesh2D(1)
  f=lambda x,y: 2*np.sin(np.sqrt(x**2+y**2))*np.cos(x)*np.sin(y)
  u2=f(q2[0],q2[1])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotiso(q2,me2,u2,contours=25,colormap='viridis')
  mlab4sim.plotmesh(q1,me1,color='black')
  mlab4sim.plotmesh(q2,me2,color='LightGray',representation='surface',opacity=0.4)
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plot(q2,me2,u2,colormap='viridis')
  mlab4sim.plotiso(q2,me2,u2,contours=np.arange(-1,1,0.2),colormap='viridis',color='White')
  mlab.view(0,0)
  mlab.colorbar()
  mlab.figure(3,**figure_options)
  mlab4sim.plotiso(q2,me2,u2,contours=25,colormap='viridis',plane=False)
  #mlab4sim.plotmesh(q1,me1,color='black',plane=False)
  mlab4sim.plotmesh(q2,me2,color='LightGray',representation='surface',opacity=0.4,z=u2)
  mlab.colorbar()
  mlab.figure(4,**figure_options)
  mlab4sim.plot(q2,me2,u2,colormap='viridis',plane=False)
  mlab4sim.plotiso(q2,me2,u2,contours=np.arange(-1,1,0.2),colormap='viridis',color='White',plane=False)
  mlab.colorbar()
  if show:
    mlab.show()
  
def plotiso3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[0],q3[1],q3[2])
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotiso(q2,me2,u2,line_width=2)
  mlab4sim.plotmesh(q2,me2, color='LightGray', opacity=0.1)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotiso(q2,me2,u2,line_width=2,color='White')
  mlab4sim.plotmesh(q1,me1, color='Black')
  mlab.colorbar()
  mlab.view(65,74,7)
  if show:
    mlab.show()

def plotiso3Ds01(show=True):
  q2,me2,toG2=mshsim.getMesh3Ds(2)
  q1,me1,toG1=mshsim.getMesh3Ds(1)
  f=lambda x,y,z: np.cos(3*x-1)*np.sin(2*y-2)*np.sin(3*z)
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plot(q2,me2,u2, opacity=0.7)
  mlab4sim.plotiso(q2,me2,u2, line_width=1.5)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plot(q2,me2,u2)
  mlab4sim.plotiso(q2,me2,u2, line_width=1.5,color='White')
  mlab4sim.plotmesh(q1,me1, color='Black')
  mlab.colorbar()
  if show:
    mlab.show()
  
def slicemesh3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=(-1,0,1))
  mlab.view(132,53,7)
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  for normal,color in [((1,0,0),'red'),((0,1,0),'magenta'),((0,0,1),'Maroon')]:
    mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=normal,color=color)
  mlab.view(155,66,7)
  if show:
    mlab.show()
  
def slice3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[0],q3[1],q3[2])
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.slice(q3,me3,u3,origin=(0,0,1),normal=(-1,0,1))
  mlab.view(132,53,7)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  for normal in [(1,0,0),(0,1,0),(0,0,1)]:
    mlab4sim.slice(q3,me3,u3,origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  if show:
    mlab.show()
  
def sliceiso3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x-y)*np.sin(2*y+x)*np.sin(3*z)
  u3=f(q3[0],q3[1],q3[2])
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.sliceiso(q3,me3,u3,origin=(0,0,1),normal=(-1,0,1))
  mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=(-1,0,1),color='DarkGray')
  mlab.view(132,53,7)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  #for normal in [(1,0,0),(0,1,0),(0,0,1)]: # BUG: core dump
  for normal in [(0,0,1),(1,-1,0),(1,1,0)]:
    mlab4sim.slicemesh(q3,me3,origin=(0,0,1),normal=normal, color='LightGray')
    mlab4sim.sliceiso(q3,me3,u3,contours=15,origin=(0,0,1),normal=normal)
  mlab.view(155,66,7)
  mlab.colorbar()
  if show:
    mlab.show()
  
def slice_unstructured_grid3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u3=f(q3[0],q3[1],q3[2])
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mp=mlab4sim.plot(q3,me3,u3,opacity=0.05)
  sug1=mlab4sim.slice_unstructured_grid(mp,normal=[0,1,1],origin=[0,0,1],w_enabled=True,property={'representation':'surface'})
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  mlab.figure(2,**figure_options)
  mpm=mlab4sim.plotmesh(q3,me3,opacity=0.05)
  sug2=mlab4sim.slice_unstructured_grid(mpm,normal=[0,1,1],origin=[0,0,1])
  mlab4sim.plotmesh(q1,me1,color='Black',line_width=2)
  if show:
    mlab.show()  
  
def quiver2D01(show=True):
  q2,me2,toG2=mshsim.getMesh2D(2)
  q1,me1,toG1=mshsim.getMesh2D(1)
  f=lambda x,y: 2*np.sin(np.sqrt(x**2+y**2))*np.cos(x)*np.sin(y)
  u=f(q2[0],q2[1])
  w=[lambda x,y: y*np.cos(-(x**2+y**2)/10), lambda x,y: -x*np.cos(-(x**2+y**2)/10)]
  W=np.array([w[0](q2[0],q2[1]),w[1](q2[0],q2[1])])
  mlab.close(all=True) 
  nq=q2.shape[1]
  mlab.figure(1,**figure_options)
  mlab4sim.quiver(q2,me2,W, scale_factor=0.05 ,line_width=1, mask_points=nq//2000,colormap='viridis')
  mlab4sim.plotmesh(q1,me1,color='black')
  mlab.vectorbar()
  mlab.view(0,0)
  mlab.figure(2,**figure_options)
  mlab4sim.quiver(q2,me2,W, scalars=u, scale_factor=0.05,line_width=1, mask_points=nq//2000)
  mlab4sim.plotmesh(q1,me1,color='black')
  mlab.scalarbar()
  mlab.view(0,0)
  if show:
    mlab.show()
    
def quiver3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u=f(q3[0],q3[1],q3[2])
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([w[0](q3[0],q3[1],q3[2]),
              w[1](q3[0],q3[1],q3[2]),
              w[2](q3[0],q3[1],q3[2])])
  mlab.close(all=True)
  nq=q3.shape[1]
  mlab.figure(1,**figure_options)
  mlab4sim.quiver(q3,me3,W,line_width=1, mask_points=nq//3000)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.05)
  mlab.vectorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.quiver(q3,me3,W,scalars=u, line_width=1, mask_points=nq//3000)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.scalarbar()
  if show:
    mlab.show()
  
def quiver3Ds01(show=True):
  q2,me2,toG2=mshsim.getMesh3Ds(2)
  q1,me1,toG1=mshsim.getMesh3Ds(1)
  f=lambda x,y,z: 3*x**2-y**3+z**2+x*y
  u=f(q2[0],q2[1],q2[2])
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z]
  W=np.array([w[0](q2[0],q2[1],q2[2]),
              w[1](q2[0],q2[1],q2[2]),
              w[2](q2[0],q2[1],q2[2])])
  mlab.close(all=True)
  nq=q2.shape[1]
  mlab.figure(1,**figure_options)
  mlab4sim.quiver(q2,me2,W,line_width=1)
  mlab4sim.plotmesh(q1,me1,color='black',line_width=2)
  mlab.vectorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.quiver(q2,me2,W,scalars=u, line_width=1)
  mlab4sim.plotmesh(q1,me1,color='black',line_width=2)
  mlab.scalarbar()
  if show:
    mlab.show()
  
def iso_surface3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u=f(q3[0],q3[1],q3[1])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.iso_surface(q3,me3,u,contours=5)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.iso_surface(q3,me3,u,contours=np.linspace(-0.8,0.8,10))
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  if show:
    mlab.show()
  
def streamline3D01(show=True):
  q3,me3,toG3=mshsim.getMesh3D(3)
  q2,me2,toG2=mshsim.getMesh3D(2)
  q1,me1,toG1=mshsim.getMesh3D(1)
  f=lambda x,y,z: 3*x**2-y**3+z**2+x*y
  u=f(q3[0],q3[1],q3[2])
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z/5]
  W=np.array([w[0](q3[0],q3[1],q3[2]),
              w[1](q3[0],q3[1],q3[2]),
              w[2](q3[0],q3[1],q3[2])])
  
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.streamline(q3,me3,u,W)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  s_options={'visible':True}
  sw_options={'normal':(0,0,1),'resolution':6}
  st_options={'integration_direction':'both'}
  mlab4sim.streamline(q3,me3,u,W,seedtype='plane',linetype='tube',
                   seed_options=s_options,
                   seed_widget_options=sw_options,
                   streamtracer_options=st_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()

  mlab.figure(3,**figure_options)
  sw_options={'center':(0.9,0,1), 'radius':0.1,'phi_resolution':8,
              'theta_resolution':12,'enabled':False}
  st_options={'integration_direction':'both'}
  mlab4sim.streamline(q3,me3,u,W,seed_widget_options=sw_options,
                   streamtracer_options=st_options,colormap='jet')
  sw_options['center']=(0,0,1)
  sw_options['radius']=0.3
  mlab4sim.streamline(q3,me3,u,W,seed_widget_options=sw_options,
                   streamtracer_options=st_options,colormap='jet')
  mlab.scalarbar()
  mlab.view(46.6,58,6.7)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)

  mlab.figure(4,**figure_options)
  sw_options={'origin':(0,-1,0),'point1':(0,-1,2),'point2':(0,1,0),
              'enabled':True,'resolution':6}
  st_options={'integration_direction':'both'}
  mlab4sim.streamline(q3,me3,u,W,seedtype='plane',
                   seed_widget_options=sw_options,
                   streamtracer_options=st_options,colormap='jet')
  mlab.scalarbar()
  mlab.view(46.6,58,6.7)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)  
  if show:
    mlab.show()
  
def volume3D01(show=True):
  q3,me3=mshsim.getMesh3D(3)[:2]
  q2,me2=mshsim.getMesh3D(2)[:2]
  q1,me1=mshsim.getMesh3D(1)[:2]
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)
  u=f(q3[0],q3[1],q3[2])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.volume(q3,me3,u)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.colorbar()
  mlab.figure(2,**figure_options)
  mvol=mlab4sim.volume(q3,me3,u)
  mvol._volume_property.scalar_opacity_unit_distance=0.2
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab.colorbar()
  if show:
    mlab.show() 
  
def vectors2D01(show=True):  
  q2,me2=mshsim.getMesh2D(2)[:2]
  q1,me1=mshsim.getMesh2D(1)[:2]
  f=lambda x,y: np.cos(3*x-y)*np.sin(2*y+x)
  u2=f(q2[0],q2[1])
  w=[lambda x,y: y*np.cos(x+y), lambda x,y: -x*np.cos(y)]
  W=np.array([w[0](q2[0],q2[1]),
              w[1](q2[0],q2[1])])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mv2=mlab4sim.vectors(q2,me2,W, scale_factor=0.2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab.vectorbar(mv2,orientation='vertical')
  mlab.view(0,0)
  mlab.figure(2,**figure_options)
  mv1=mlab4sim.vectors(q2,me2,W,scalars=u2, mask_points=2, scale_factor=0.3,colormap='viridis')
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab.scalarbar(mv1,orientation='vertical')
  mlab.view(0,0)
  if show:
    mlab.show()  
  
def vectors3D01(show=True):
  q3,me3=mshsim.getMesh3D(3)[:2]
  q2,me2=mshsim.getMesh3D(2)[:2]
  q1,me1=mshsim.getMesh3D(1)[:2]
  f=lambda x,y,z: np.cos(3*x-y)*np.sin(2*y+x)*np.sin(3*z)
  u3=f(q3[0],q3[1],q3[2])
  u2=f(q2[0],q2[1],q2[2])
  w=[lambda x,y,z: y*np.cos(x+y-z), lambda x,y,z: -x*np.cos(-x+y+z), lambda x,y,z: (2-z)*z*np.sin(x+y+z)]
  W=np.array([w[0](q3[0],q3[1],q3[2]),
              w[1](q3[0],q3[1],q3[2]),
              w[2](q3[0],q3[1],q3[2])])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.vectors(q3,me3,W, mask_points=2, scale_factor=0.2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab.vectorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.vectors(q3,me3,W,scalars=u3, mask_points=2, scale_factor=0.2,colormap='viridis')
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.05)
  mlab.scalarbar()
  if show:
    mlab.show()
  
def vectors3Ds01(show=True):
  q2,me2=mshsim.getMesh3Ds(2)[:2]
  q1,me1=mshsim.getMesh3Ds(1)[:2]
  f=lambda x,y,z: np.cos(3*x-y)*np.sin(2*y+x)*np.sin(3*z)
  u2=f(q2[0],q2[1],q2[2])
  w=[lambda x,y,z: y*np.cos(x+y-z), lambda x,y,z: -x*np.cos(z+x-y), lambda x,y,z: z*np.cos(x-y)]
  W=np.array([w[0](q2[0],q2[1],q2[2]),
              w[1](q2[0],q2[1],q2[2]),
              w[2](q2[0],q2[1],q2[2])])
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.vectors(q2,me2,W, mask_points=2, scale_factor=0.2)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.2)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab.vectorbar()
  mlab.figure(2,**figure_options)
  mlab4sim.vectors(q2,me2,W,scalars=u2, mask_points=2, scale_factor=0.2,colormap='viridis')
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.2)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab.scalarbar()
  if show:
    mlab.show()
  
def plot_node_indices2D01(small=True,show=True):
  q2,me2=mshsim.getMesh2D(2,small=small)[:2]
  q1,me1=mshsim.getMesh2D(1,small=small)[:2]
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2,opacity=0.5)
  mlab4sim.plot_node_indices(q2)
  mlab.view(0,0)
  node_prop= {'color':check_color('White'),
            'frame':True,
            'frame_color':check_color('Black'),
            'background_color':check_color('OrangeRed'),
            'background_opacity':0.6}
  fig=mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2,opacity=0.5)
  mlab4sim.plot_node_indices(q2,property=node_prop)
  mlab.view(0,0)
  #fig.scene.set_size((800,800))
  if show:
    mlab.show()
  
def plot_node_indices3Ds01(small=True,show=True):
  q2,me2=mshsim.getMesh3Ds(2,small=small)[:2]
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plot_node_indices(q2)
  node_prop= {'color':check_color('White'),
            'frame':True,
            'frame_color':check_color('Black'),
            'background_color':check_color('OrangeRed'),
            'background_opacity':0.6}
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=1,representation='surface',edge_visibility=True)
  mlab4sim.plot_node_indices(q2,property=node_prop)
  if show:
    mlab.show()
  
def plot_node_indices3D01(small=True,show=True):
  q3,me3,toG3=mshsim.getMesh3D(3,small=small)  
  q2,me2,toG2=mshsim.getMesh3D(2,small=small)
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  # Only plot the 40 first node indices
  mlab4sim.plot_node_indices(q3,indices=np.arange(40)) 
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  node_prop= {'color':check_color('White'),
            'frame':True,
            'frame_color':check_color('Black'),
            'background_color':check_color('OrangeRed'),
            'background_opacity':0.6}
  mlab4sim.plot_node_indices(q3,indices=np.arange(0,q3.shape[1],50),property=node_prop)
  mlab.figure(3,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=1,representation='surface',edge_visibility=True)
  mlab4sim.plot_node_indices(q2,indices=np.arange(0,q2.shape[1],20),property=node_prop)
  if show:
    mlab.show()
  
def plot_element_indices2D01(small=True,show=True):
  q2,me2=mshsim.getMesh2D(2,small=small)[:2]
  q1,me1=mshsim.getMesh2D(1,small=small)[:2]
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2,opacity=0.5)
  mlab4sim.plot_element_indices(q2,me2)
  mlab.view(0,0)
  elt_prop={'color':check_color('Indigo'),
          'frame':True,
          'frame_color':check_color('Indigo'),
          'background_color':check_color('Lavender'),
          'background_opacity':0.6}
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2,opacity=0.5)
  mlab4sim.plot_element_indices(q2,me2,property=elt_prop)
  mlab.view(0,0)
  if show:
    mlab.show()
  
def plot_element_indices3Ds01(small=True,show=True):
  q2,me2=mshsim.getMesh3Ds(2,small=small)[:2]
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plot_element_indices(q2,me2)
  elt_prop={'color':check_color('Indigo'),
          'frame':True,
          'frame_color':check_color('Indigo'),
          'background_color':check_color('Lavender'),
          'background_opacity':0.6}
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=1,representation='surface',edge_visibility=True)
  mlab4sim.plot_element_indices(q2,me2,property=elt_prop)
  if show:
    mlab.show()
  
def plot_element_indices3D01(small=True,show=True):
  q3,me3,toG3=mshsim.getMesh3D(3,small=small)  
  q2,me2,toG2=mshsim.getMesh3D(2,small=small)
  mlab.close(all=True)
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  # Only plot the 40 first element indices
  mlab4sim.plot_element_indices(q3,me3,indices=np.arange(40)) 
  elt_prop={'color':check_color('Indigo'),
          'frame':True,
          'frame_color':check_color('Indigo'),
          'background_color':check_color('Lavender'),
          'background_opacity':0.6}
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plot_element_indices(q3,me3,indices=np.arange(0,me3.shape[1],50),property=elt_prop)
  mlab.figure(3,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plot_element_indices(q3,me3,indices=np.arange(0,me3.shape[1],50),property=elt_prop,visible_enabled=True)
  mlab.figure(4,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=1,representation='surface',edge_visibility=True)
  mlab4sim.plot_element_indices(q2,me2,indices=np.arange(0,me2.shape[1],20),property=elt_prop)
  if show:
    mlab.show()
  
def plot_mesh_indices2D01(small=True,show=True):
  q2,me2=mshsim.getMesh2D(2,small=small)[:2]
  q1,me1=mshsim.getMesh2D(1,small=small)[:2]
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.4)
  mlab4sim.plot_mesh_indices(q2,me2)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2,opacity=0.5)
  mlab4sim.plot_mesh_indices(q2,me2)
  mlab.view(0,0)
  elt_prop={'color':check_color('Indigo'),
          'frame':True,
          'frame_color':check_color('Indigo'),
          'background_color':check_color('Lavender'),
          'background_opacity':0.6}
  node_prop= {'color':check_color('White'),
            'frame':True,
            'frame_color':check_color('Black'),
            'background_color':check_color('OrangeRed'),
            'background_opacity':0.6}
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.4)
  mlab4sim.plotmesh(q1,me1,color='k',line_width=2,opacity=0.5)
  mlab4sim.plot_mesh_indices(q2,me2,element_property=elt_prop,node_property=node_prop)
  mlab.view(0,0)
  if show:
    mlab.show()
  
def plot_mesh_indices3Ds01(small=True,show=True):
  q2,me2=mshsim.getMesh3Ds(2,small=small)[:2]
  mlab.close(all=True) 
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=0.1)
  mlab4sim.plot_element_indices(q2,me2)
  elt_prop={'color':check_color('Indigo'),
          'frame':True,
          'frame_color':check_color('Indigo'),
          'background_color':check_color('Lavender'),
          'background_opacity':0.6}
  node_prop= {'color':check_color('White'),
            'frame':True,
            'frame_color':check_color('Black'),
            'background_color':check_color('OrangeRed'),
            'background_opacity':0.6}
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q2,me2,color='LightGray',opacity=1,representation='surface',edge_visibility=True)
  mlab4sim.plot_mesh_indices(q2,me2,element_property=elt_prop,node_property=node_prop)
  if show:
    mlab.show()
  
def plot_mesh_indices3D01(small=True,show=True):
  q3,me3,toG3=mshsim.getMesh3D(3,small=small)  
  q2,me2,toG2=mshsim.getMesh3D(2,small=small)
  q1,me1=mshsim.getMesh3D(1,small=True)[:2]
  node_idx=np.arange(0,q3.shape[1],100)
  elt_idx=np.arange(30)
  mlab.close(all=True)
  
  mlab.figure(1,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k')
  # Only plot the 40 first element indices
  mlab4sim.plot_mesh_indices(q3,me3,element_indices=elt_idx)
  
  mlab.figure(2,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab4sim.plot_mesh_indices(q3,me3,node_indices=node_idx,visible_enabled=True)
  
  mlab.figure(3,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab4sim.plot_mesh_indices(q3,me3,node_indices=node_idx,element_indices=elt_idx,visible_enabled=True) 
  
  elt_prop={'color':check_color('Indigo'),
          'frame':True,
          'frame_color':check_color('Indigo'),
          'background_color':check_color('Lavender'),
          'background_opacity':0.6}
  node_prop= {'color':check_color('White'),
            'frame':True,
            'frame_color':check_color('Black'),
            'background_color':check_color('OrangeRed'),
            'background_opacity':0.6}
  mlab.figure(4,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k')
  # Only plot the 40 first element indices
  mlab4sim.plot_mesh_indices(q3,me3,element_indices=elt_idx,element_property=elt_prop,node_property=node_prop)
  
  mlab.figure(5,**figure_options)
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab4sim.plot_mesh_indices(q3,me3,node_indices=node_idx,element_property=elt_prop,node_property=node_prop,visible_enabled=True)
  
  mlab.figure(6,**figure_options)
  mlab4sim.plotmesh(q1,me1,color='k')
  mlab4sim.plotmesh(q3,me3,color='LightGray',opacity=0.1)
  mlab4sim.plot_mesh_indices(q3,me3,node_indices=node_idx,element_indices=elt_idx,element_property=elt_prop,node_property=node_prop,visible_enabled=True) 
  if show:
    mlab.show() 
  
def rundemo(demo,show):
  print('[fc_mayavi4mesh] Running demo %s'%demo)
  eval(demo+'(show=False)')
  seedemo(show)
  
def seedemo(show):
  if show:
    print('  Close Mayavi scenes to continue...')
    mlab.show()
  mlab.close(all=True)
  
def alldemos(show=False):
  ListOfDemos=['plotmesh2D','plotmesh3D','plotmesh3Ds','plot2D','plot3D','plot3Ds',
     'plotiso2D01','plotiso3D01','plotiso3Ds01','slicemesh3D01','slice3D01',
     'sliceiso3D01','quiver2D01','quiver3D01','quiver3Ds01','iso_surface3D01',
     'streamline3D01']
  for demo in ListOfDemos:
    rundemo(demo,show)
  
