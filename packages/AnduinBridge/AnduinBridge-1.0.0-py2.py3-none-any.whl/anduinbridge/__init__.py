"""AnduinBridge enables remote processes to call Anduin injected
database routines by wrapping routines in local REST API. """
__version__ = '1.0.0'

from anduinbridge import AnduinRestServer, getAnduinData

__all__ = ['AnduinRestServer', 'getAnduinData']
