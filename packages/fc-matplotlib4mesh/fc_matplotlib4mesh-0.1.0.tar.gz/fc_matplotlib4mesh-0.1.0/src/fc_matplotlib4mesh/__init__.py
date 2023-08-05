# Copyright (C) 2017 Cuvelier F.
# License: GNU General Public License.
__version__='0.1.0' # automaticaly written by setpackages.py script
__packages__={'fc-tools': '0.0.22', 'fc-meshtools': '0.1.0'} # automaticaly written by setpackages.py script
#from .simplicial import plotmesh,plot,plotiso,quiver
from . import simplicial
from . import demos

def gitinfo():
  return {'name': 'fc-matplotlib4mesh', 'tag': '0.1.0', 'commit': '37ff705c699665ad5209e57136d4e035f76506c5', 'date': '2019-04-02', 'time': '18-02-47', 'status': '0'} # automatically updated
  if len(inf)>0: 
    return inf
  # Only for developpers
  import fc_tools,os
  D=os.path.realpath(os.path.join(__path__[0],os.path.pardir))
  if os.path.basename(D)=='src':
    D=os.path.realpath(os.path.join(D,os.path.pardir))
  return fc_tools.git.get_info(D)
