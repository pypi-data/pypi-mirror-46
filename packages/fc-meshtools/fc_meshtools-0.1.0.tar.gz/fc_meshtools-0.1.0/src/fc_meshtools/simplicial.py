import os
import numpy as np

def getDataPath(): 
  fullname=os.path.dirname(os.path.abspath(__file__))
  return fullname+os.sep+'data'

def get_dims(q,me,**kwargs):
  #qtrans=kwargs.pop('qtrans',False)
  #if qtrans:
  dim,nq=q.shape
  #else:
    #nq,dim=q.shape
  ndfe,nme=me.shape
  #assert ndfe==dim+1, 'Trouble with q %s and me %s shapes'%(str(q.shape), str(me.shape))
  return (dim,ndfe-1,nq,nme)

def getMesh2D(d=2,small=False):
  assert d==2 or d==1 or d==0
  data_path=getDataPath()
  s=''
  if small:
    s='_small'
  npzfile = np.load(data_path+os.sep+'mesh%dsimp2D%s.npz'%(d,s))
  q=npzfile['arr_0']
  me=npzfile['arr_1']
  toGlobal=npzfile['arr_2']
  return q,me,toGlobal

def getMesh3D(d=3,small=False):
  assert d==3 or d==2 or d==1 or d==0
  data_path=getDataPath()
  s=''
  if small:
    s='_small'
  npzfile = np.load(data_path+os.sep+'mesh%dsimp3D%s.npz'%(d,s))
  q=npzfile['arr_0']
  me=npzfile['arr_1']
  toGlobal=npzfile['arr_2']
  return q,me,toGlobal

def getMesh3Ds(d=2,small=False):
  assert d==2 or d==1 or d==0
  data_path=getDataPath()
  s=''
  if small:
    s='_small'
  npzfile = np.load(data_path+os.sep+'mesh%dsimp3Ds%s.npz'%(d,s))
  q=npzfile['arr_0']
  me=npzfile['arr_1']
  toGlobal=npzfile['arr_2']
  return q,me,toGlobal

def Volumes(q,me):
  from scipy import linalg
  from math import factorial
  dim,d,nq,nme=get_dims(q,me)
  if d==0:
    return np.ones((1,nme))
  X=np.zeros((d,dim,nme))
  for i in range(d):
    X[i]=q[:,me[i+1]]-q[:,me[0]]
  if dim==d:
    return np.array([abs(linalg.det(X[::,::,k]))/factorial(d) for k in np.arange(nme)])
  V=np.zeros((d,d,nme))
  for i in range(d):
    V[i,i]=(X[i]*X[i]).sum(axis=0)
    for j in range(i+1,d):
      V[i,j]=V[j,i]=(X[i]*X[j]).sum(axis=0)
  return np.array([np.sqrt(abs(linalg.det(V[::,::,k])))/factorial(d) for k in np.arange(nme)])

def GradBaCo(q,me):
  from scipy import sparse
  from scipy.sparse.linalg import spsolve
  dim,d,nq,nme=get_dims(q,me)
  A=np.zeros((d,dim,nme))
  I=np.zeros((d,dim,nme),dtype=int)
  J=np.zeros((d,dim,nme),dtype=int)
  L=np.arange(nme)
  for i in range(d):
    A[i]=q[:,me[i+1]]-q[:,me[0]]
    I[i]=np.tile(L*d+i,(dim,1))
    for j in range(dim):
      J[i,j]=L*dim+j
  N=d*dim*nme
  spA=sparse.csc_matrix((np.reshape(A,N),(np.reshape(I,N),np.reshape(J,N))),shape=(d*nme,dim*nme))
  spH=spA*spA.T
  Grad=np.hstack([-np.ones((d,1)),np.eye(d)])
  b=np.tile(Grad,(nme,1))
  #G=spsolve(spH,b)
  GradBaCo=spA.T*spsolve(spH,b)
  return GradBaCo.reshape((nme,dim,d+1)) #.swapaxes(1,2)
    
def GetMaxLengthEdges(q,me):
  dim,d,nq,nme=get_dims(q,me)
  ne=d+1;
  h=0.
  for i in range(ne):
    for j in range(i+1,ne):
      h=max(h,np.sum((q[:,me[i]]-q[:,me[j]])**2,axis=0).max())
  return np.sqrt(h)
  
def NormalFaces(q,me,GradBaCo):
  dim,d,nq,nme=get_dims(q,me)
  #(IndLocFaces,IndOpositePt)=getIndLocFaces(d)
  Normal=np.zeros((d+1,dim,nme))
  for i in range(d+1):
    #A=-self.GradBaCo[:,IndOpositePt[i],:]
    A=-GradBaCo[:,:,i]
    Normal[i,:,:]=A.T
    N2=np.sqrt(np.sum(A**2,axis=1))
    for j in range(dim):
      Normal[i,j,:]=Normal[i,j,:]/N2
  return Normal
    
def barycenters(q,me):
  dim,d,nq,nme=get_dims(q,me)
  Ba=np.zeros((dim,nme))
  for i in range(d+1):
    Ba+=q[:,me[i]]
  Ba/=(d+1)
  return Ba

def submesh(q,me,idxme):
  ME=me[:,idxme]
  idxq,I=np.unique(ME.flatten(),return_inverse=True)  
  Qreduce=q[:,idxq]      
  MEreduce=I.reshape(ME.shape)
  return Qreduce,MEreduce

def spAK(q,me):
  from scipy import sparse
  dim,d,nq,nme=get_dims(q,me)
  spAK=sparse.csc_matrix((dim*nme,d*nme))
  N=dim*nme
  Jset=(np.arange(nme)*d)
  Iset=(np.arange(nme)*dim).reshape((1,nme))
  I=Iset+(np.arange(dim)).reshape((dim,1))
  for j in range(d):
    J=np.tile(Jset+j,(dim,1))
    K=q[:,me[j+1]]-q[:,me[0]]
    spAK+=sparse.csc_matrix((K.reshape(N),(I.reshape(N),J.reshape(N))),shape=(dim*nme,d*nme))
  return spAK

def GradBaCo_spa(q,me):
  from scipy.sparse.linalg import spsolve
  n,d,nq,nme=get_dims(q,me)
  A=spAK(q,me)
  hG=np.hstack([-np.ones((d,1)),np.eye(d)])
  B=np.tile(hG,(nme,1))
  if d==n:
    return spsolve(A.T,B).reshape((nme,n,d+1))
  G=A*spsolve(A.T.dot(A),B)
  return G.reshape((nme,n,d+1))
