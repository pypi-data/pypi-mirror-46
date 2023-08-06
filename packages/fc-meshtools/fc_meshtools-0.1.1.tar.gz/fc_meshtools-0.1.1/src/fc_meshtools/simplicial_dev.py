import os
import numpy as np

from fc_meshtools.simplicial import get_dims

def buildAKt_v01(q):
  # q (d+1)-by-n numpy array. Vertices of a d-simplex in R^n
  # Return The transpose AK matrix
  return q[1:]-q[0]

def buildHK_v01(q):
  AKt=buildAKt_v01(q)
  return AKt.dot(AKt.T)


def detVec(A):
  # A is d-by-d-by-nme array
  import numpy as np
  d=A.shape[0];
  assert(A.shape[1]==d)
  nme=A.shape[2];
  if d==1:
    return A[0,0]
  else:
    if d==2:
      return A[0,0]*A[1,1]-A[0,1]*A[1,0]
    else:
      D=np.zeros((nme,))
      for ii in range(d):
        D=D+(-1)**(ii)*(A[0,ii]*detVec(np.delete(np.delete(A,ii,1),0,0)))
      return D

def AK3D_v00(q,me):
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  A=np.zeros((d,nme,dim))
  for k in np.arange(nme):
    for i in np.arange(dim):
      for j in np.arange(d):
        A[j,k,i]=q[me[j+1,k],i]-q[me[0,k],i]
  return A

def AK3D_v01(q,me):
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  A=np.zeros((d,nme,dim))
  for i in range(d):
    A[i]=q[me[i+1]]-q[me[0]]
  return A
  
def AK3D(q,me):
  return AK3D_v01(q,me)
#def buildAK3D(q,me):
  #dim,d,nq,nme=get_dims(q,me)
  #if d==0:
    #return np.ones((1,nme))
  #AK=np.zeros((d,nme,dim))
  #for i in range(d):
    #AK[i]=q[me[i+1]]-q[me[0]]
  #return AK
  
def HK3D_v00(q,me):
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  H=np.zeros((d,d,nme))
  for k in np.arange(nme):
    At=q[me[1:,k]]-q[me[0,k]] # At.shape==(d,dim)
    H[:,:,k]=np.dot(At,At.T)
  return H

def HK3D_v01(q,me):
  AK=AK3D(q,me)
  dim,d,nq,nme=get_dims(q,me)
  V=np.zeros((d,d,nme))
  for i in range(d):
    V[i,i]=(AK[i]*AK[i]).sum(axis=1)
    for j in range(i+1,d):
      V[i,j]=V[j,i]=(AK[i]*AK[j]).sum(axis=1)
  return V    

def HK3D(q,me):
  return HK3D_v01(q,me)

#def buildHK3D(q,me):
  #AK=buildAK3D(q,me)
  #dim,d,nq,nme=get_dims(q,me)
  #V=np.zeros((d,d,nme))
  #for i in range(d):
    #V[i,i]=(AK[i]*AK[i]).sum(axis=1)
    #for j in range(i+1,d):
      #V[i,j]=V[j,i]=(AK[i]*AK[j]).sum(axis=1)
  #return V    

def genVolumes_v01(q,me):
  from scipy import linalg
  from math import factorial,sqrt
  dim,d,nq,nme=get_dims(q,me)
  #print('dim=%d, d=%d, nq=%d, nme=%d'%(dim,d,nq,nme))
  if d==0:
    return np.ones((1,nme))
  vols=np.zeros((nme,))
  fd=factorial(d);
  for k in np.arange(nme):
    At=q[me[1:,k]]-q[me[0,k]]
    vols[k]=sqrt(abs(linalg.det(At.dot(At.T))))/fd
  return vols

def genVolumes_v02(q,me):
  from scipy import linalg
  from math import factorial,sqrt
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  vols=np.zeros((nme,))
  fd=factorial(d);
  for k in np.arange(nme):
    vols[k]=sqrt(abs(linalg.det(buildHK_v01(q[me[:,k]]))))/fd
  return vols
  
def genVolumes_v03(q,me):
  from scipy import linalg
  from math import factorial,sqrt
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  return np.array([np.sqrt(abs(linalg.det(buildHK_v01(q[me[:,k]]))))/factorial(d) for k in np.arange(nme)])
    
  
def genVolumes_v04(q,me):
  from scipy import linalg
  from math import factorial,sqrt
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  HK=buildHK3D(q,me)
  return np.sqrt(abs(detVec(HK)))/factorial(d)
  
  
  
def dimVolumes_v01(q,me):
  from scipy import linalg
  from math import factorial
  dim,d,nq,nme=get_dims(q,me)
  assert dim==d
  vols=np.zeros((nme,))
  fd=factorial(d);
  for k in np.arange(nme):
    At=q[me[1:,k]]-q[me[0,k]]
    vols[k]=abs(linalg.det(At))/fd
  return vols

def dimVolumes_v02(q,me):
  from scipy import linalg
  from math import factorial
  dim,d,nq,nme=get_dims(q,me)
  assert dim==d
  vols=np.zeros((nme,))
  fd=factorial(d);
  for k in np.arange(nme):
    vols[k]=abs(linalg.det(buildAKt_v01(q[me[:,k]])))/fd
  return vols
  
def dimVolumes_v03(q,me):
  from scipy import linalg
  from math import factorial,sqrt
  dim,d,nq,nme=get_dims(q,me)
  assert dim==d
  return np.array([abs(linalg.det(buildAKt_v01(q[me[:,k]])))/factorial(d) for k in np.arange(nme)]) 

def dimVolumes_v04(q,me):
  from scipy import linalg
  from math import factorial,sqrt
  dim,d,nq,nme=get_dims(q,me)
  assert dim==d
  AK=buildAK3D(q,me).swapaxes(1,2)
  return abs(detVec(AK))/factorial(d)

def spAK_v01(q,me):
  from scipy import sparse
  n,d,nq,nme=get_dims(q,me)
  spA=sparse.lil_matrix((d*nme,n*nme))
  idx=np.arange(n); jdx=np.arange(d);
  for k in np.arange(nme):
    spA[np.ix_(jdx,idx)]=buildAKt_v01(q[me[:,k]])
    idx+=n;jdx+=d
  return (spA.T).tocsc()
  
def spAK_v20(q,me):
  from scipy import sparse
  dim,d,nq,nme=get_dims(q,me)
  A=np.zeros((d,dim,nme))
  I=np.zeros((d,dim,nme),dtype=int)
  J=np.zeros((d,dim,nme),dtype=int)
  L=np.arange(nme)
  for i in range(d):
    A[i]=(q[me[i+1]]-q[me[0]]).T
    I[i]=np.tile(L*d+i,(dim,1))
    for j in range(dim):
      J[i,j]=L*dim+j
  N=d*dim*nme
  return sparse.csc_matrix((np.reshape(A,N),(np.reshape(J,N),np.reshape(I,N))),shape=(dim*nme,d*nme))
  
  
