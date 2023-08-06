from .EdbotClient import EdbotClient
from .util import *

from pkg_resources import get_distribution

__version__ = get_distribution('edbot').version