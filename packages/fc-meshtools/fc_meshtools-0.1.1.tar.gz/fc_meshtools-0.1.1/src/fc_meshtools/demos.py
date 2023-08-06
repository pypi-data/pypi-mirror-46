import numpy as np
import os

from fc_meshtools import simplicial,feval

def simplicial2D(**kwargs):
  verbose=kwargs.pop('verbose',False)
  small=kwargs.pop('small',True)
  if verbose:
    print('*** Running simplicial2D demo')
  u=lambda x,y:  3*np.exp(-((x-1)**2+y**2)/10)*np.cos(x-1)*np.sin(y);
  q2,me2,toGlobal2=simplicial.getMesh2D(2,small)
  if verbose:
    print('  -> d=2, q: %s array, me: %s array'%(str(q2.shape),str(me2.shape)))
  q1,me1,toGlobal1=simplicial.getMesh2D(1,small)
  if verbose:
    print('  -> d=1, q: %s array, me: %s array'%(str(q1.shape),str(me1.shape)))
  
  res=0
  E=np.max(np.abs(q2[:,toGlobal1]-q1))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 1: failed with E=%g'%E)
    else:
      print('  Test 1: OK')
  
  U2=feval(u,q2)
  U1=feval(u,q1)
  E=np.max(np.abs(U2[toGlobal1]-U1))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 2: failed with E=%g'%E)
    else:
      print('  Test 2: OK')
  return res==0
  
def simplicial3Ds(**kwargs):
  verbose=kwargs.pop('verbose',False)
  small=kwargs.pop('small',True)
  if verbose:
    print('*** Running simplicial3D demo')
  u=lambda x,y,z:  3*np.exp(-((x-1)**2+y**2)/10)*np.cos(x-1)*np.sin(y-z);
  q2,me2,toGlobal2=simplicial.getMesh3Ds(2,small)
  if verbose:
    print('  -> d=2, q: %s array, me: %s array'%(str(q2.shape),str(me2.shape)))
  q1,me1,toGlobal1=simplicial.getMesh3Ds(1,small)
  if verbose:
    print('  -> d=1, q: %s array, me: %s array'%(str(q1.shape),str(me1.shape)))
  
  res=0
  E=np.max(np.abs(q2[:,toGlobal1]-q1))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 1: failed with E=%g'%E)
    else:
      print('  Test 1: OK')
  
  U2=feval(u,q2)
  U1=feval(u,q1)
  E=np.max(np.abs(U2[toGlobal1]-U1))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 2: failed with E=%g'%E)
    else:
      print('  Test 2: OK')
  return res==0
      
def simplicial3D(**kwargs):
  verbose=kwargs.pop('verbose',False)
  small=kwargs.pop('small',True)
  if verbose:
    print('*** Running simplicial3D demo')
  u=lambda x,y,z:  3*np.exp(-((x-1)**2+y**2)/10)*np.cos(x-1)*np.sin(y-z);
  q3,me3,toGlobal3=simplicial.getMesh3D(3,small)
  if verbose:
    print('  -> d=3, q: %s array, me: %s array'%(str(q2.shape),str(me2.shape)))
  q2,me2,toGlobal2=simplicial.getMesh3D(2,small)
  if verbose:
    print('  -> d=2, q: %s array, me: %s array'%(str(q2.shape),str(me2.shape)))
  q1,me1,toGlobal1=simplicial.getMesh3D(1,small)
  if verbose:
    print('  -> d=1, q: %s array, me: %s array'%(str(q1.shape),str(me1.shape)))
  
  res=0
  E=np.max(np.abs(q3[:,toGlobal2]-q2))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 1: failed with E=%g'%E)
    else:
      print('  Test 1: OK')
  E=np.max(np.abs(q3[:,toGlobal1]-q1))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 2: failed with E=%g'%E)
    else:
      print('  Test 2: OK')
  
  U3=feval(u,q3)
  U2=feval(u,q2)
  U1=feval(u,q1)
  E=np.max(np.abs(U3[toGlobal1]-U1))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 3: failed with E=%g'%E)
    else:
      print('  Test 3: OK')
      
  E=np.max(np.abs(U3[toGlobal2]-U2))
  res=res+(E >1e-15)
  if verbose:
    if E >1e-15:
      print('  Test 4: failed with E=%g'%E)
    else:
      print('  Test 4: OK')    
  return res==0
  
def rundemo(demo,show):
  print('[fc_meshtools] Running %s'%demo)
  isOK=eval(demo)
  if isOK:
    print('  -> OK')
  else:
    print('  -> Failed')
  
def alldemos(show=False):
  ListOfDemos=['simplicial2D()','simplicial3Ds()','simplicial3D()']
  for demo in ListOfDemos:
    rundemo(demo,show)  
