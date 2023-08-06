# Copyright (C) 2017 Cuvelier F.
# License: GNU General Public License.
__version__='0.1.2' # automaticaly written by setpackages.py script
__packages__={'fc-tools': '0.0.22', 'fc-meshtools': '0.1.0'} # automaticaly written by setpackages.py script
#from .simplicial import plotmesh,plot,plotiso,slicemesh,slice,sliceiso,quiver,iso_surface,streamline
from . import simplicial
from . import demos

def gitinfo():
  return {'name': 'fc-mayavi4mesh', 'tag': '0.1.2', 'commit': '491cdcb6adf4ee4554f8fb4550479c93e38310b3', 'date': '2019-05-13', 'time': '15-38-34', 'status': '0'} # automatically updated
  if len(inf)>0: 
    return inf
  # Only for developpers
  import fc_tools,os
  D=os.path.realpath(os.path.join(__path__[0],os.path.pardir))
  if os.path.basename(D)=='src':
    D=os.path.realpath(os.path.join(D,os.path.pardir))
  return fc_tools.git.get_info(D)
