try:
    from .__version__ import VERSION
except:               # pragma: no cover
    VERSION='unknown'
from ._logging import logger as log
__all__ = []
