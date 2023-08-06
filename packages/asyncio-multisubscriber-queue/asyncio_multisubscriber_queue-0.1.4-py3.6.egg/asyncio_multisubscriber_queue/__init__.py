import sys

__version__ = '0.1.4'
__MIN_PYTHON__ = (3, 6)


if sys.version_info < __MIN_PYTHON__:
    sys.exit('python {}.{} or later is required'.format(*__MIN_PYTHON__))


from .queue import MultisubscriberQueue
