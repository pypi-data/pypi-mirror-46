import logging,os
logging.basicConfig(level=logging.DEBUG
        if os.getenv('DEBUG',None)
        else logging.ERROR)
logger = logging.getLogger('cfg')
__all__=['logger']
log = logger.getChild('_logging')
