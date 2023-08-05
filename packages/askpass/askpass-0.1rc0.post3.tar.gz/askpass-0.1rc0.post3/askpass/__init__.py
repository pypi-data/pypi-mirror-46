try:
    from .__version__ import VERSION
except:               # pragma: no cover
    VERSION='unknown'
from ._logging import logger
from .pinentry import Pinentry
from .askpass import AskPass
__all__ = ['logger','Pinentry','AskPass']
