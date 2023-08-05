import numpy as np

def set_mesh(N,verbose,**kwargs):
  import fc_oogmsh,fc_meshtools
  from fc_bench.bench import bData
  d=kwargs.pop('d',2) # in [2,2.5,3]
  Type=kwargs.pop('Type',None) # Type of simplices 1: Lines, 2: Triangles, 4: Tedrahedra 
  qtrans=kwargs.pop('qtrans',False)
  geofile=kwargs.pop('geofile','condenser11')
  meshfile=fc_oogmsh.buildmesh(d,geofile,N,verbose=0,**kwargs)
  oGh=fc_oogmsh.ooGmsh(meshfile)
  
  if Type is None:
    Type=2 # Triangles
    if oGh.dim==3 and (4 in oGh.types):
      Type=4
  assert Type in oGh.types
  q,me=oGh.extractElement(Type,qtrans=qtrans)
  dim,d,nq,nme=fc_meshtools.simplicial.get_dims(q,me)
  if verbose:
    print('# geofile: %s'%geofile)
    print('#    type: %d'%Type)
    print('#   -> dim=%d, d=%d'%(dim,d))
  
  bDs=[bData('{:>8}'.format('N'),N,'{:8}'),bData('{:>8}'.format('nq'),nq,'{:8}'),bData('{:>9}'.format('nme'),nme,'{:9}')]
  return ((q,me),bDs)

def bench_dimVolumes():
  import fc_bench
  from fc_meshtools.simplicial_dev import dimVolumes_v01,dimVolumes_v02,dimVolumes_v03,dimVolumes_v04
  Lfun=[dimVolumes_v01,dimVolumes_v02,dimVolumes_v03,dimVolumes_v04]
  Error=lambda out1,out2: np.max(abs(out1-out2))
  fc_bench.bench(Lfun,set_mesh,LN=np.arange(5,30,5),d=3,Type=4,geofile='cylinderkey',error=Error)
  
# kwargs={'LN',np.arange(5,30,5),'d':3,'Type':4,'geofile':'cylinderkey'}  

# bench_AK3D(LN=[20,40,60,80])
def bench_AK3D(**kwargs):
  import fc_bench
  from fc_meshtools.simplicial import AK3D_v00,AK3D_v01
  d=kwargs.pop('d', 2)
  LN=kwargs.pop('LN', np.arange(5,30,5))
  geofile=kwargs.pop('geofile', 'condenser')
  Type=kwargs.pop('Type', 2)
  Lfun=[AK3D_v00,AK3D_v01]
  Error=lambda out1,out2: np.max(abs(out1-out2))
  fc_bench.bench(Lfun,set_mesh,LN=LN,d=d,Type=Type,geofile=geofile,error=Error,**kwargs)

# fc_meshtools.benchs.bench_HK3D()
def bench_HK3D(**kwargs):
  import fc_bench
  from fc_meshtools.simplicial_dev import HK3D_v00,HK3D_v01
  d=kwargs.pop('d', 2)
  LN=kwargs.pop('LN', np.arange(5,30,5))
  geofile=kwargs.pop('geofile', 'condenser')
  Type=kwargs.pop('Type', 2)
  Lfun=[HK3D_v00,HK3D_v01]
  Error=lambda out1,out2: np.max(abs(out1-out2))
  fc_bench.bench(Lfun,set_mesh,LN=LN,d=d,Type=Type,geofile=geofile,error=Error,**kwargs)
