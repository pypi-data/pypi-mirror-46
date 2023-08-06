# Copyright (C) 2017 Cuvelier F.
# License: GNU General Public License.
__version__='0.1.2' # automaticaly written by setpackages.py script
__packages__={'fc-tools': '0.0.22', 'fc-meshtools': '0.1.1'} # automaticaly written by setpackages.py script
#from .simplicial import plotmesh,plot,plotiso,quiver
from . import simplicial
from . import demos

def gitinfo():
  return {'name': 'fc-matplotlib4mesh', 'tag': '0.1.2', 'commit': 'd156387725190a72fbdfef280eeea272479b2064', 'date': '2019-05-14', 'time': '15-59-07', 'status': '0'} # automatically updated
  if len(inf)>0: 
    return inf
  # Only for developpers
  import fc_tools,os
  D=os.path.realpath(os.path.join(__path__[0],os.path.pardir))
  if os.path.basename(D)=='src':
    D=os.path.realpath(os.path.join(D,os.path.pardir))
  return fc_tools.git.get_info(D)
