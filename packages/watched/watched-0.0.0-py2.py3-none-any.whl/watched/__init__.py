# Import only the "public API" functions in the package's `__init__.py`.
# It's OK to use **explicit** relative imports in a package's root initfile.
from pkg_resources import get_distribution, DistributionNotFound

from .fibonacci import generate_nth_fibonacci

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    pass
