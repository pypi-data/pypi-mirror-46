import logging,os
logging.basicConfig(level=logging.DEBUG if 'DEBUG' in os.environ else logging.WARNING)
logger = logging.getLogger('askpass')
__all__=['logger']
