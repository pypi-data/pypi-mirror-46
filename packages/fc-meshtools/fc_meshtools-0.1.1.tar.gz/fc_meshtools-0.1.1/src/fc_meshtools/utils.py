import numpy as np
from fc_tools.graphics import Plane

def feval(fun,q):
  fun=np.vectorize(fun)
  if q.shape[0]==2:
    u=fun(q[0],q[1])
  if q.shape[0]==3:
    u=fun(q[0],q[1],q[2])
  return u

def cutMeshElements(q,me,cut_planes):
  ME=me
  if cut_planes != []:
    idxme=cutIndexMeshElements(q,me,cut_planes)
    ME=ME[:,idxme]
  return ME

def cutIndexMeshElements(q,me,cut_planes):
  # cut_planes is a list of fc_simesh.mayavi_tools.Plane objects
  idxme=np.arange(me.shape[1])
  for i in range(len(cut_planes)):
    assert( isinstance(cut_planes[i] , Plane) )
    idxme=np.setdiff1d(idxme,_cutIndexPlane(q,me,cut_planes[i]))
  return idxme

# private functions
      
def _cutIndexPlane(q,me,P):
  nq=q.shape[1]
  Z=np.dot( q.T-P.origin , P.normal) # using broadcasting
  idx=np.where(Z<0)[0]
  R=np.in1d(me[0],idx)
  for i in range(1,me.shape[0]):
    R[:]=R & np.in1d(me[i],idx) 
  return np.where(~R)[0]
