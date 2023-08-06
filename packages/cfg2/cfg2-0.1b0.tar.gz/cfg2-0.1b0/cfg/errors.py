from ._logging import logger
log = logger.getChild('errors')

class CustomTypeError(TypeError):
    def __init__(self,o):
        super().__init__(type(o).__name__)

__all__ = ['CustomTypeError']
