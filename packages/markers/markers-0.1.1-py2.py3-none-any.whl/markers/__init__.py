from ._version import version_info, __version__

from .markers import *
from .project import *
from .labeler import *

def _jupyter_nbextension_paths():
    return [{
        'section': 'notebook',
        'src': 'static',
        'dest': 'markers',
        'require': 'markers/extension'
    }]
