import os
from mcutk.debugger import jlink
from mcutk.debugger import pyocd
from mcutk.debugger import redlink
from mcutk.debugger import ide

__all__ = ["getdebugger", 'jlink', 'pyocd', 'redlink']



def getdebugger(type, *args, **kwargs):
    """Return debugger instance."""
    supported = {
        "jlink": jlink.JLINK,
        "pyocd": pyocd.PYOCD,
        "redlink": redlink.RedLink,
        'ide': ide.IDE,
    }
    try:
        return supported[type](*args, **kwargs)
    except KeyError:
        raise ValueError("not supported debugger: %s"%type)

