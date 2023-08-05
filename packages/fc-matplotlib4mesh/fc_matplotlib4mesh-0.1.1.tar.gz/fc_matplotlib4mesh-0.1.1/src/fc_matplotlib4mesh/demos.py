import numpy as np
import os
from fc_meshtools import simplicial as msimp
from fc_meshtools.simplicial import getMesh2D,getMesh3Ds,getMesh3D
import matplotlib.pyplot as plt
from fc_tools.Matplotlib import set_axes_equal,DisplayFigures,set_axes
from fc_matplotlib4mesh.sys import getDataPath
import fc_matplotlib4mesh.simplicial as plt4sim

def plotmesh2D(small=True):
  plt.ion()
  q2,me2,toG2=getMesh2D(2,small)
  q1,me1,toG1=getMesh2D(1,small)
  plt.close('all')
  plt.figure(1)
  plt4sim.plotmesh(q2,me2)
  set_axes_equal()
  plt.figure(2)
  plt4sim.plotmesh(q1,me1,color='Red',linewidth=2)
  plt4sim.plotmesh(q2,me2,color='LightGray',alpha=0.1)
  set_axes_equal()
  
def plotmesh3D(small=True):
  q3,me3=getMesh3D(3,small)[:2]
  q2,me2=getMesh3D(2,small)[:2]
  q1,me1=getMesh3D(1,small)[:2]
  plt.ion()
  plt.close('all')
  plt.figure(1)
  plt4sim.plotmesh(q3,me3)
  set_axes_equal()
  plt.figure(2)
  plt4sim.plotmesh(q2,me2,color='Red')
  set_axes_equal()
  plt.axis('off')
  plt.figure(3)
  plt4sim.plotmesh(q3,me3,color='LightGray',alpha=0.02)
  plt4sim.plotmesh(q1,me1,color='Magenta',linewidths=2)
  from fc_tools.graphics import Plane
  P=[Plane(origin=[0,0,1],normal=[0,0,-1]), Plane(origin=[0,0,1],normal=[0,-1,-1])]
  set_axes_equal()
  plt.axis('off')
  plt.figure(4)
  plt4sim.plotmesh(q3,me3,cut_planes=P,color='DarkGrey')
  plt4sim.plotmesh(q2,me2,cut_planes=P)
  plt4sim.plotmesh(q1,me1,color='Black',linewidths=2)
  set_axes_equal()
  plt.axis('off')
  
def plotmesh3Ds(small=True):
  q2,me2=getMesh3Ds(2,small)[:2]
  q1,me1=getMesh3Ds(1,small)[:2]
  plt.ion()
  plt.close('all')
  plt.figure(1)
  plt4sim.plotmesh(q2,me2,edgecolor='Red',facecolor=None)
  plt4sim.plotmesh(q1,me1,color='Black',linewidths=2)
  set_axes_equal()
  plt.figure(2)
  plt4sim.plotmesh(q2,me2,color='LightGray',alpha=0.1)
  plt4sim.plotmesh(q1,me1,color='Magenta',linewidths=2)
  plt.axis('off')
  set_axes_equal()
  
def plot2D(small=True):
  q2,me2=getMesh2D(2,small)[:2]
  q1,me1=getMesh2D(1,small)[:2]
  f=lambda x,y: (x**2+y**2)*np.cos(x)*np.sin(y)
  u2=f(q2[0],q2[1])
  u1=f(q1[0],q1[1])
  plt.close('all')
  plt.ion()
  DisplayFigures(nfig=4)
  plt.figure(1)
  ps1=plt4sim.plot(q2,me2,u2)
  plt4sim.plotmesh(q1,me1,color='Black',linewidths=2)
  plt.colorbar()
  set_axes_equal()
  plt.figure(2)
  ps2=plt4sim.plot(q1,me1,u1,linewidths=2)
  plt.colorbar(ps2)
  plt4sim.plotmesh(q2,me2,color='LightGray',alpha=0.1)
  plt.axis('off')
  set_axes_equal()
  plt.figure(3)
  ps3=plt4sim.plot(q2,me2,u2,plane=False)
  plt4sim.plotmesh(q1,me1,z=u1,color='Black',linewidths=2)
  plt.colorbar(ps3)
  plt.axis('off')
  fig=plt.figure(4)
  ps4=plt4sim.plot(q1,me1,u1,linewidths=2,plane=False)
  plt4sim.plotmesh(q2,me2,z=u2,color='LightGray',alpha=0.1)
  plt.colorbar(ps4)
  plt.axis('off')
  #fig.show()
  #fig.canvas.draw()
  #plt.pause(0.001)
  
def plot3D(small=True):
  q3,me3=getMesh3D(3,small)[:2]
  q2,me2=getMesh3D(2,small)[:2]
  q1,me1=getMesh3D(1,small)[:2]
  f=lambda x,y,z: np.cos(3*x)*np.sin(2*y)*np.sin(3*z)+x
  u3=f(q3[0],q3[1],q3[2])
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  plt.close('all')
  plt.ion()
  plt.figure(1)
  pp=plt4sim.plot(q3,me3,u3)
  plt4sim.plotmesh(q1,me1,color='Black',linewidths=2)
  plt.colorbar(pp)
  set_axes_equal()
  plt.figure(2)
  pp=plt4sim.plot(q2,me2,u2)
  plt4sim.plotmesh(q1,me1,color='Black',linewidths=2)
  plt.axis('off')
  set_axes_equal()
  plt.colorbar(pp)
  plt.figure(3)
  pp=plt4sim.plot(q1,me1,u1,linewidths=2,vmin=min(u3),vmax=max(u3))
  plt4sim.plotmesh(q3,me3,color='LightGray',alpha=0.1)
  plt.colorbar(pp)
  plt.axis('off')
  set_axes_equal()
  
def plot3Ds(small=True):
  q2,me2=getMesh3Ds(2,small)[:2]
  q1,me1=getMesh3Ds(1,small)[:2]
  f=lambda x,y,z: np.cos(3*x-1)*np.sin(2*y-2)*np.sin(3*z)
  u2=f(q2[0],q2[1],q2[2])
  u1=f(q1[0],q1[1],q1[2])
  plt.close('all')
  plt.ion()
  plt.figure(1)
  pp=plt4sim.plot(q2,me2,u2)
  plt4sim.plotmesh(q1,me1,color='Black',linewidths=2)
  plt.colorbar(pp)
  plt.axis('off')
  set_axes_equal()
  plt.figure(2)
  pp=plt4sim.plot(q1,me1,u1,linewidths=2,vmin=min(u2),vmax=max(u2))
  plt4sim.plotmesh(q2,me2,color='LightGray',alpha=0.1)
  plt.colorbar(pp)
  plt.axis('off')
  set_axes_equal()
  
def plotiso2D01(small=False):
  q2,me2=getMesh2D(2,small)[:2]
  q1,me1=getMesh2D(1,small)[:2]
  f=lambda x,y: (x**2+y**2)*np.cos(x)*np.sin(y)
  u2=f(q2[0],q2[1])
  plt.close('all')
  plt.ion()
  cmap=plt.cm.get_cmap(name='viridis')
  plt4sim.plotiso(q2,me2,u2,niso=25,cmap=cmap)
  plt.colorbar()
  plt4sim.plotmesh(q1,me1,color='black')
  plt4sim.plotmesh(q2,me2,color='LightGray',alpha=0.04)
  set_axes_equal()
  plt.figure(2)
  plt4sim.plot(q2,me2,u2,cmap=cmap)
  plt.colorbar()
  set_axes_equal()
  plt4sim.plotiso(q2,me2,u2,isorange=np.arange(-20,20,4),color='White')
    
def quiver2D01(small=True):
  (q,me)=getMesh2D(2,small)[:2]
  (q1,me1)=getMesh2D(1,small)[:2]
  f=lambda x,y:5*np.exp(-3*(x**2+y**2))*np.cos(x)*np.sin(y)
  u=f(q[0],q[1])
  w=[lambda x,y: y*np.cos(-(x**2+y**2)/10), lambda x,y: -x*np.cos(-(x**2+y**2)/10)]
  W=np.array([w[0](q[0],q[1]),w[1](q[0],q[1])])

  cmap=plt.cm.get_cmap(name='viridis')
  plt.ion()
  plt.close('all')
  plt.figure(1)
  plt4sim.quiver(q,W,scale=50,nvec=3000)
  plt4sim.plotmesh(q1,me1,color='Black')
  plt.colorbar()
  set_axes_equal()
  plt.figure(2)
  plt4sim.quiver(q,W,scalars=u,scale=50,nvec=3000)
  plt4sim.plotmesh(q1,me1,color='Black')
  #plt4sim.plotiso(q,me,u)
  plt.colorbar()
  set_axes_equal()
  plt.figure(3)
  plt4sim.quiver(q,W,scale=50,nvec=3000,color='Blue')
  plt4sim.plotmesh(q1,me1,color='Black')
  set_axes_equal()
  
def quiver3D01(small=True):
  (q3,me3)=getMesh3D(3,small)[:2]
  (q2,me2)=getMesh3D(2,small)[:2]
  (q1,me1)=getMesh3D(1,small)[:2]
  f=lambda x,y,z: 3*x**2-y**3+z**2+x*y
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z]
  q=q3
  u3=f(q[0],q[1],q[2])
  W3=np.array([w[0](q[0],q[1],q[2]),w[1](q[0],q[1],q[2]),w[2](q[0],q[1],q[2])])
  q=q2
  u2=f(q[0],q[1],q[2])
  W2=np.array([w[0](q[0],q[1],q[2]),w[1](q[0],q[1],q[2]),w[2](q[0],q[1],q[2])])
  q=q1
  u1=f(q[0],q[1],q[2])
  W1=np.array([w[0](q[0],q[1],q[2]),w[1](q[0],q[1],q[2]),w[2](q[0],q[1],q[2])])

  cmap=plt.cm.get_cmap(name='jet')
  plt.ion()
  plt.close('all')
  plt.figure(1)
  pq=plt4sim.quiver(q3,W3,scale=20,nvec=3000)
  plt.colorbar(pq)
  plt4sim.plotmesh(q1,me1,color='Black')
  set_axes_equal()
  plt.figure(2)
  pq=plt4sim.quiver(q3,W3,scalars=u3,scale=20,nvec=3000,cmap=cmap)
  plt4sim.plotmesh(q1,me1,color='Black')
  plt.colorbar(pq)
  set_axes_equal()
  plt.axis('off')
  plt.figure(3)
  plt4sim.quiver(q3,W3,scale=20,nvec=3000,color='Blue')
  plt4sim.plotmesh(q1,me1,color='Black')
  set_axes_equal()
  plt.axis('off')
  
def quiver3Ds01(small=True):
  (q2,me2)=getMesh3Ds(2,small)[:2]
  (q1,me1)=getMesh3Ds(1,small)[:2]
  f=lambda x,y,z: 3*x**2-y**3+z**2+x*y
  w=[lambda x,y,z: y*np.cos(-(x**2+y**2)/10), lambda x,y,z: -x*np.cos(-(x**2+y**2)/10), lambda x,y,z: z]
  q=q2
  u2=f(q[0],q[1],q[2])
  W2=np.array([w[0](q[0],q[1],q[2]),w[1](q[0],q[1],q[2]),w[2](q[0],q[1],q[2])])
  q=q1
  u1=f(q[0],q[1],q[2])
  W1=np.array([w[0](q[0],q[1],q[2]),w[1](q[0],q[1],q[2]),w[2](q[0],q[1],q[2])])

  cmap=plt.cm.get_cmap(name='jet')
  plt.close('all')
  plt.ion()
  plt.figure(1)
  pq=plt4sim.quiver(q2,W2,scale=20,nvec=3000)
  plt.colorbar(pq)
  plt4sim.plotmesh(q1,me1,color='Black')
  set_axes_equal()
  plt.figure(2)
  pq=plt4sim.quiver(q2,W2,scalars=u2,scale=20,nvec=3000,cmap=cmap)
  plt4sim.plotmesh(q1,me1,color='Black')
  plt.colorbar(pq)
  set_axes_equal()
  plt.axis('off')
  plt.figure(3)
  plt4sim.quiver(q2,W2,scale=20,nvec=3000,color='Blue')
  plt4sim.plotmesh(q1,me1,color='Black')
  set_axes_equal()
  plt.axis('off')
  
def plotGradBaCo2D(small=True):  
  q2,me2=msimp.getMesh2D(2,small)[:2]
  q1,me1=msimp.getMesh2D(1,small)[:2]

  dim,d,nq,nme=msimp.get_dims(q2,me2)
  G=msimp.GradBaCo(q2,me2)
  Ba=msimp.barycenters(q2,me2)
  Normal=msimp.NormalFaces(q2,me2,G)

  plt.close('all')
  plt.ion()
  plt.figure(1)
  plt4sim.plotmesh(q2,me2)
  plt4sim.plotGradBaCo(q2,me2,scale=None)
  set_axes_equal()
  set_axes(plt.gca(),np.array([-2,2,2,5.2]))
  plt.figure(2)
  #plt4sim.plotmesh(q1,me1,color='Red',linewidth=2)
  plt4sim.plotmesh(q2,me2,color='LightGray',alpha=0.5)
  plt4sim.plotGradBaCo(q1,me1,scale=None)
  set_axes_equal()
  set_axes(plt.gca(),np.array([-2,2,2,5.2]))
  
def plotGradBaCo3Ds(small=True): 
  q2,me2=msimp.getMesh3Ds(2,small)[:2]
  q1,me1=msimp.getMesh3Ds(1,small)[:2]
  dim,d,nq,nme=msimp.get_dims(q2,me2)
  
  plt.close('all')
  plt.ion()
  plt.figure(1)

  plt4sim.plotmesh(q2,me2,facecolor='lightgray',edgecolor='k',alpha=0.3)
  plt4sim.plotGradBaCo(q2,me2,length=0.2,index=np.arange(0,nme,8))
  set_axes_equal()
  
  plt.figure(2)
  #plt4sim.plotmesh(q1,me1,color='Red',linewidth=2)
  plt4sim.plotmesh(q2,me2,color='LightGray',edgecolor='k',alpha=0.1)
  plt4sim.plotmesh(q1,me1,color='k',linewidth=2,alpha=0.2)
  plt4sim.plotGradBaCo(q1,me1,length=0.1)
  set_axes_equal()
  
def plotGradBaCo3D(small=True):
  q3,me3=msimp.getMesh3D(3,small)[:2]
  q2,me2=msimp.getMesh3D(2,small)[:2]
  q1,me1=msimp.getMesh3D(1,small)[:2]
  dim,d,nq3,nme3=msimp.get_dims(q3,me3)
  dim,d,nq2,nme2=msimp.get_dims(q2,me2)
  
  plt.close('all')
  plt.ion()
  
  plt.figure(1)
  plt4sim.plotmesh(q3,me3,facecolor='lightgray',edgecolor='k',alpha=0.01)
  plt4sim.plotGradBaCo(q3,me3,length=0.05,index=np.arange(0,nme3,10))
  set_axes_equal()
  plt.figure(2)
  plt4sim.plotmesh(q2,me2,color='LightGray',edgecolor='k',alpha=0.1)
  plt4sim.plotGradBaCo(q2,me2,length=0.1,index=np.arange(0,nme2,6))
  set_axes_equal()
  plt.figure(3)
  plt4sim.plotmesh(q2,me2,color='LightGray',edgecolor='k',alpha=0.1)
  plt4sim.plotGradBaCo(q1,me1,length=0.1)
  set_axes_equal()
  
def rundemo(demo,show):
  print('[fc_matplotlib4mesh] Running demo %s'%demo)
  eval(demo)
  seedemo(show)
  
def seedemo(show):
  if show:
    DisplayFigures()
    import time
    print('    Waiting 3s before closing ...')
    time.sleep(3)
  plt.close('all')
  
def alldemos(show=False):
  #ListOfDemos=['plotmesh2D()','plot2D()']
  ListOfDemos=['plotmesh2D()','plotmesh3D()','plotmesh3Ds()','plot2D()','plot3D()','plot3Ds()',
               'plotiso2D01()','quiver2D01()','quiver3D01()','quiver3Ds01()']
  for demo in ListOfDemos:
    rundemo(demo,show)  
