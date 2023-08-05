# Copyright (C) 2017 Cuvelier F.
# License: GNU General Public License.
__version__='0.1.0' # automaticaly written by setpackages.py script
__packages__={'fc-tools': '0.0.22'} # automaticaly written by setpackages.py script

from . import simplicial

# from . import demos
#import benchs
from .utils import feval

from . import demos
from . import benchs

def gitinfo():
  return {'name': 'fc-meshtools', 'tag': '0.1.0', 'commit': 'c396db78f7b79872a04654db06a9c2ee4fbf1409', 'date': '2019-04-02', 'time': '18-02-15', 'status': '0'} # automatically updated
  if len(inf)>0: 
    return inf
  # Only for developpers
  import fc_tools,os
  from . import __path__
  D=os.path.realpath(os.path.join(__path__[0],os.path.pardir))
  if os.path.basename(D)=='src':
    D=os.path.realpath(os.path.join(D,os.path.pardir))
  return fc_tools.git.get_info(D)


