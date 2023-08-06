import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Patch
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d as a3
from mpl_toolkits.mplot3d.art3d import Poly3DCollection,Line3DCollection
from matplotlib.collections import PolyCollection,LineCollection

from fc_tools.others import LabelBaseName,simplicial_dimension
from fc_tools.colors import check_color,selectColors
from fc_tools.Matplotlib import set_axes
from fc_tools.graphics import Plane

import fc_meshtools.simplicial as msimp

def plotmesh(q,me,**kwargs):
  """
  mesh plotting
  
  Parameters
  ----------
    q : mesh vertices, dim-by-nq numpy array where
        dim is the space dimension (2 or 3) and nq the number of vertices.
    me: mesh elements connectivity array where elements are d-simplices. 
        me is a (d+1)-by-nme numpy array where nme is the number 
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
    #q,me,dim,d=simplicial_dimension(q,me)
    dim,d,nq,nme=msimp.get_dims(q,me)
    move=kwargs.pop('move',None)
    Q=move_mesh(q,move)
    return eval("_plotmesh_SubTh"+str(d)+"simp"+str(dim)+"D(Q,me,**kwargs)")
  assert False,'Not yet implemented for '+kind+' mesh elements'

def plot(q,me,u,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    #q,me,dim,d=simplicial_dimension(q,me)
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

def quiver(q,me,V,**kwargs):
  kind=kwargs.pop('kind', 'simplicial')
  if kind=='simplicial':
    dim,d,nq,nme=msimp.get_dims(q,me)
    assert dim>=2
    return quiver_simp(q,V,**kwargs)
  assert False,'Not yet implemented for '+kind+' mesh elements'
  

def cutIndex(q,me,cut_planes):
  # cut_planes is a list of fc_simesh.mayavi_tools.Plane objects
  idxme=np.arange(me.shape[1])
  for i in range(len(cut_planes)):
    assert( isinstance(cut_planes[i] , Plane) )
    #idxme=np.intersect1d(idxme,cutIndexPlane(sTh,cut_planes[i]))
    idxme=np.setdiff1d(idxme,cutIndexPlane(q,me,cut_planes[i]))
  return idxme
      
def cutIndexPlane(q,me,P):
  nq=q.shape[1]
  Z=np.dot( q.T-P.origin , P.normal) # using broadcasting
  idx=np.where(Z<0)[0]
  R=np.in1d(me[0],idx)
  for i in range(1,me.shape[0]):
    R[:]=R & np.in1d(me[i],idx) 
  return np.where(~R)[0]

def cutMeshElements(q,me,cut_planes):
  ME=me
  if cut_planes != []:
    idxme=cutIndex(q,me,cut_planes)
    ME=ME[:,idxme]
  return ME

def move_mesh(q,U):
  if U is None:
    return q
  if isinstance(U,list):
    U=np.array(U)
  assert U.shape==q.shape, 'Trouble with shapes: U %s and q %s'%(str(U.shape),str(q.shape))
  return q+U 



def quiver(q,V,**kwargs):
  dim,nq=q.shape
  assert V.shape==q.shape
  scalars=kwargs.pop('scalars', None )
  scale_factor=kwargs.pop('scale_factor', 1 )
  scale=kwargs.pop('scale', 1/scale_factor )
  color=check_color(kwargs.pop('color', None))
  colormap=kwargs.pop('colormap','viridis')
  #kwargs['cmap']=kwargs.pop('map',plt.cm.get_cmap(name=colormap))
  nvec=kwargs.pop('nvec', None ) 
  
  N=nq
  toGlobal=np.arange(N)
  
  if np.isscalar(nvec):
    if nvec<N:
      I=np.random.choice(N,nvec,replace=False)
      N=nvec
      Q=q[:,I]
      toGlobal=toGlobal[I]
  W=np.zeros((dim,N))
  for i in np.arange(dim):
    W[i]=V[i,toGlobal]
    
  if color is not None:
    kwargs['color']=color
  else:
    if scalars is None:
      scalars=np.sqrt(np.sum(V**2,axis=0))
    if kwargs.get('clim',None) is None: 
      vmin=np.min(scalars);vmax=np.max(scalars)
      vmin=kwargs.pop('vmin',vmin)
      vmax=kwargs.pop('vmax',vmax)
      kwargs['clim']=kwargs.pop('clim',[vmin,vmax])  
      
  args=[]
  if scalars is not None:
    if dim==2:
      args.append(scalars[toGlobal])
    if dim==3:
      cmap = plt.get_cmap()
      # One arrow : 3 lines (shaft,headA and headB) so 3 colors
      # Three arrows with colors value v1,v2 and v3: array is [ v1,v2,v3,v1,v1,v2,v2,v3,v3]!  
      #       for N arrows [shaft1,...,shaftN, headA1,headB1,headA2,headB2,...,headAN,headBN]
      C=scalars[toGlobal] # First all -- 
      C=np.concatenate((C,np.repeat(C,2))) 
      kwargs['colors']=cmap(C)
      kwargs['array']=C # for colormap
  Q=q[:,toGlobal]
  if dim==2:    
    return plt.quiver(Q[0],Q[1],W[0],W[1],scale=scale,*args,**kwargs)
  if dim==3:
    fig = plt.gcf()
    if len(fig.axes)>0:
      ax=fig.axes[0]
    else:
      ax = fig.gca( projection='3d')
    # SEE Matplotlib.pdf 3.0.3 page 1956
    return ax.quiver(Q[0],Q[1],Q[2],W[0]/scale,W[1]/scale,W[2]/scale,**kwargs)
  assert False,"dimension must be 2 or 3 but is %d"%dim

def plotElementsNumber(q,me,**kwargs):
  dim,d,nq,nme=simp.get_dims(q,me)
  Ba=simp.barycenters(q,me)
  fig = plt.gcf()
  ax = fig.axes[0]
  if dim==2:
    for k in range(nme):
      ax.annotate(str(k),(Ba[k,0],Ba[k,1]),verticalalignment='center', horizontalalignment='center',clip_on=True,**kwargs)
      # FC : annotate more efficient than text...
      
def plotGradBaCo(q,me,**kwargs):
  from fc_meshtools import simplicial as simp
  #scale=kwargs.get('scale', 10)
  G=kwargs.pop('GradBaCo',None)
  index=kwargs.pop('index',None)
  dim,d,nq,nme=simp.get_dims(q,me)
  if index is None:
    index=np.arange(nme)
  if G is None:
    G=simp.GradBaCo(q,me)
  Ba=simp.barycenters(q,me)
  Normal=simp.NormalFaces(q,me,G)
  Colors=selectColors(d+1)
  fig=plt.gcf()
  if dim==2:
    for i in range(d+1):
      plt.quiver(Ba[0,index],Ba[1,index],Normal[i,0,index],Normal[i,1,index],color=Colors[i],**kwargs)
      xlist = []
      ylist = [] 
      for k in index:
        xlist.extend((Ba[0,k],q[0,me[i,k]]))
        xlist.append(None)
        ylist.extend((Ba[1,k],q[1,me[i,k]]))
        ylist.append(None)
      plt.plot(xlist,ylist,color=Colors[i],ls=':') 
  elif dim==3:
    ax = fig.gca(projection='3d')
    S=np.zeros((d+1,len(index),2,3))
    for i in range(d+1):
      #plt.quiver(Ba[0],Ba[1],Ba[2],Normal[i,0,:],Normal[i,1,:],Normal[i,2,:],units='xy',color=Colors[i],scale_units=scale)
      ax.quiver(Ba[0,index],Ba[1,index],Ba[2,index],Normal[i,0,index],Normal[i,1,index],Normal[i,2,index],color=Colors[i],**kwargs)
      S[i,:,0]=Ba[:,index].T
      S[i,:,1]=q[:,me[i,index]].T
      ax.add_collection3d(Line3DCollection(S[i],linestyles=':',color=Colors[i]))
      #xlist = [];ylist = [];zlist =[]
      #for k in range(nme):
        #xlist.extend((Ba[0,k],q[me[i,k],0]))
        #xlist.append(None)
        #ylist.extend((Ba[1,k],q[me[i,k],1]))
        #ylist.append(None)
        #zlist.extend((Ba[2,k],q[me[i,k],2]))
        #zlist.append(None)
      ##plt.plot3(xlist,ylist,zlist,color=Colors[i],ls=':')
      #ax.plot(xlist,ylist,zlist,color=Colors[i],ls=':')


# "Private" functions

def _plotmesh_SubTh0simp2D(q,me,**kwargs):
  kwargs['marker']=kwargs.get('marker','o')
  z=kwargs.pop('z',None)
  fig = plt.gcf()
  if z is None:
    ax = fig.gca()
    return ax.plot(q[0],q[1],linestyle='',**kwargs)
  assert isinstance(z,np.ndarray) and z.shape[0]==nq
  z.resize((nq,1))
  return plotmesh_SubTh0simp3D(np.concatenate((q,z),axis=1),me,**kwargs)
  
def _plotmesh_SubTh0simp3D(q,me,**kwargs):
  kwargs['marker']=kwargs.get('marker','o')
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  return ax.scatter(q[0],q[1],q[2],**kwargs)#c=color,marker=marker,**kwargs)
  
  
def _plotmesh_SubTh1simp1D(q,me,**kwargs):
  #lim=kwargs.pop('lim',True)
  z=kwargs.pop('z',None)
  nme=me.shape[1]
  nq=q.shape[1]
  fig = plt.gcf()
  if z is None:
    ax = fig.gca()
    q=np.concatenate((q,np.zeros((nq,1))),axis=1)
    coll= ax.add_collection(LineCollection(q[me],**kwargs))
    #box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1])])
    #set_axes(ax,box)
    return coll
  assert isinstance(z,np.ndarray) and z.shape[0]==nq
  z.resize((nq,1))
  return plotmesh_SubTh1simp2D(np.concatenate((q,z),axis=1),me,**kwargs)  
  
def _plotmesh_SubTh1simp2D(q,me,**kwargs):
  lim=kwargs.pop('lim',True)
  z=kwargs.pop('z',None)
  nme=me.shape[1]
  nq=q.shape[1]
  fig = plt.gcf()
  if z is None:
    ax = fig.gca()
    coll= ax.add_collection(LineCollection(q[:,me].T,**kwargs))
    box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1])])
    set_axes(ax,box)
    return coll
  assert isinstance(z,np.ndarray) and z.shape[0]==nq
  z.resize((1,nq))
  return _plotmesh_SubTh1simp3D(np.concatenate((q,z),axis=0),me,**kwargs)

def _plotmesh_SubTh1simp3D(q,me,**kwargs):
  lim=kwargs.pop('lim',True)
  nme=me.shape[1]
  nq=q.shape[1]
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  coll= ax.add_collection(Line3DCollection(q[:,me].T,**kwargs))
  if lim:
    box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1]),np.min(q[2]),np.max(q[2])])
    set_axes(ax,box)
  return coll

def _plotmesh_SubTh2simp2D(q,me,**kwargs):
  lim=kwargs.pop('lim',True)
  color=check_color(kwargs.pop('color','Blue'))
  kwargs['edgecolor']=check_color(kwargs.pop('edgecolor',color))
  facecolor=check_color(kwargs.pop('facecolor',None))
  if facecolor is None:
    facecolor='none'
  z=kwargs.pop('z',None)
  if z is None:
    fig = plt.gcf()
    ax = fig.gca()
    polys=PolyCollection(q[:,me].T,**kwargs)
    polys.set_facecolor(facecolor)
    coll=ax.add_collection(polys)
    if lim:
      box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1])])
      set_axes(ax,box)
    return coll
    #return plt.triplot(q[0],q[1],triangles=me,**kwargs)
  nq=q.shape[1]
  assert isinstance(z,np.ndarray) and z.shape[0]==nq
  z=z.reshape((1,nq))
  return _plotmesh_SubTh2simp3D(np.concatenate((q,z),axis=0),me,lim=lim,**kwargs)
  
def _plotmesh_SubTh2simp3D(q,me,**kwargs):
  lim=kwargs.pop('lim',True)
  color=check_color(kwargs.pop('color','Blue'))
  kwargs['edgecolor']=check_color(kwargs.pop('edgecolor',color))
  kwargs['facecolor']=check_color(kwargs.pop('facecolor',color))
  #if facecolor is None:
    #facecolor='none'
  cut_planes=kwargs.pop('cut_planes',[])
  ME=cutMeshElements(q,me,cut_planes)
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  polys=Poly3DCollection(q[:,ME].swapaxes(0,2),**kwargs)
  #polys.set_facecolor(facecolor)
  coll=ax.add_collection(polys)# BUG: with alpha=... don't work with ax.add_collection3d
  if lim:
    box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1]),np.min(q[2]),np.max(q[2])])
    set_axes(ax,box)
  #p=Patch(facecolor=facecolor,edgecolor=edgecolor,**kwargs)  
  return Patch(**kwargs)
  #return coll

def _plotmesh_SubTh3simp3D(q,me,**kwargs):
  lim=kwargs.pop('lim',True)
  cut_planes=kwargs.pop('cut_planes',[])
  color=check_color(kwargs.pop('color','Blue'))
  kwargs['edgecolor']=check_color(kwargs.pop('edgecolor',color))
  kwargs['facecolor']=check_color(kwargs.pop('facecolor',color))

  ME=cutMeshElements(q,me,cut_planes)
  
  nq=q.shape[1]
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  EDGES=np.concatenate((ME[[0,1]],ME[[0,2]],ME[[0,3]],ME[[1,2]],ME[[1,3]],ME[[2,3]]),axis=1)  
  EDGES=np.unique(EDGES,axis=1)
  QQ=q[:,EDGES].swapaxes(0,2)
  coll=ax.add_collection(Line3DCollection(QQ,**kwargs))  # linewidths=0.4, linestyles=':')
  if lim:
    box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1]),np.min(q[2]),np.max(q[2])])
    set_axes(ax,box)
  return Patch(**kwargs)

def _plot_SubTh2simp2D(q,me,u,**kwargs):
  plane=kwargs.pop('plane',True)
  shading=kwargs.pop('shading','gouraud')
  kwargs['vmin']=kwargs.get('vmin',np.min(u))
  kwargs['vmax']=kwargs.get('vmax',np.max(u))
  fig = plt.gcf()
  if plane:
    return plt.tripcolor(q[0],q[1],me.T, u, shading=shading,**kwargs)#vmin=vmin,vmax=vmax, shading=shading,**kwargs)
  nq=q.shape[1]
  assert isinstance(u,np.ndarray) and u.shape[0]==nq
  Q=np.concatenate((q,u.reshape((1,nq))),axis=0)
  return _plot_SubTh2simp3D(Q,me,u,**kwargs)

def _plot_SubTh1simp1D(q,me,u,**kwargs):
  vmin=kwargs.pop('vmin',None)
  vmax=kwargs.pop('vmax',None)
  cmap=kwargs.pop('cmap',None)
  q=q.reshape((q.shape[0],))
  idx=np.argsort(q)
  plt.plot(q[idx],u[idx],**kwargs)

def _plot_SubTh1simp2D(q,me,u,**kwargs):
  assert isinstance(u,np.ndarray)
  lim=kwargs.pop('lim',True)
  plane=kwargs.pop('plane',True)
  vmin=kwargs.pop('vmin',np.min(u))
  vmax=kwargs.pop('vmax',np.max(u))
  fig = plt.gcf()
  if plane:
    ax = plt.gca()
    coll=ax.add_collection(LineCollection(q[:,me].T,array=np.mean(u[me],axis=0),norm=matplotlib.colors.Normalize(vmin=vmin, vmax=vmax),**kwargs))
    if lim:
      box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1])])
      set_axes(ax,box)
    return coll
  nq=q.shape[1]
  u=u.reshape((1,nq))
  assert isinstance(u,np.ndarray) and u.shape[1]==nq
  Q=np.concatenate((q,u),axis=0)
  return _plot_SubTh1simp3D(Q,me,u.reshape((nq,)),vmin=vmin, vmax=vmax,lim=lim,**kwargs)

def _plot_SubTh1simp3D(q,me,u,**kwargs):
  lim=kwargs.pop('lim',True)
  vmin=kwargs.pop('vmin',np.min(u))
  vmax=kwargs.pop('vmax',np.max(u))
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  U=np.mean(u[me],axis=0)#.reshape((me.shape[1],))
  coll=ax.add_collection(Line3DCollection(q[:,me].T,array=U,norm=matplotlib.colors.Normalize(vmin=vmin, vmax=vmax),**kwargs))
  if lim:
    box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1]),np.min(q[2]),np.max(q[2])])
    set_axes(ax,box)
  return coll  
  
def _plot_SubTh2simp3D(q,me,u,**kwargs):
  vmin=kwargs.pop('vmin',np.min(u))
  vmax=kwargs.pop('vmax',np.max(u))
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  U=np.mean(u[me],axis=0).reshape((me.shape[1],))
  coll=ax.add_collection(Poly3DCollection(q[:,me].T,array=U,norm=matplotlib.colors.Normalize(vmin=vmin, vmax=vmax),**kwargs))
  box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1]),np.min(q[2]),np.max(q[2])])
  set_axes(ax,box)
  return coll

def _plot_SubTh3simp3D(q,me,u,**kwargs):
  s=kwargs.pop('s',1)
  kwargs['vmin']=kwargs.get('vmin',np.min(u))
  kwargs['vmax']=kwargs.get('vmax',np.max(u))
  
  fig = plt.gcf()
  if len(fig.axes)>0:
    ax=fig.axes[0]
  else:
    ax = fig.gca( projection='3d')
  sc=ax.scatter3D(q[0],q[1],q[2],s=s,c=u,**kwargs) 
  box=np.array([np.min(q[0]),np.max(q[0]),np.min(q[1]),np.max(q[1]),np.min(q[2]),np.max(q[2])])
  set_axes(ax,box)
  return sc

def _plotiso_SubTh2simp2D(q,me,u,**kwargs):
  plane=kwargs.pop('plane',True)
  niso=kwargs.pop('niso', 15 )
  isorange=kwargs.pop('isorange', None )
  color=check_color(kwargs.pop('color', None ))
  cmap=kwargs.pop('cmap',plt.cm.get_cmap(name='viridis'))
  if isorange is None and niso>1 :
    vmin=kwargs.get('vmin', min(u))
    vmax=kwargs.get('vmax', max(u))
    isorange=np.linspace(vmin,vmax,num=niso)
  else:
    if np.isscalar(isorange):
      isorange=np.array([isorange])
    else:
      isorange=np.sort(isorange)
  if color is not None:
    kwargs['colors']=np.tile(color,(len(isorange),1))
  else:
    kwargs['cmap']=cmap
  fig = plt.gcf()
  if plane:
    return plt.tricontour(q[0],q[1],me.T, u,isorange,**kwargs)
  nq=q.shape[1]
  assert isinstance(u,np.ndarray) and u.shape[0]==nq
  Q=np.concatenate((q,u.reshape((nq,1))),axis=1)
  assert False, "Not yet implemented"
  return _plotiso_SubTh2simp3D(Q,me,u,isorange=isorange,**kwargs)
