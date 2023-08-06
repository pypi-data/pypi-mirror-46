# -*- coding: utf-8 -*-

"""Top-level package for nsbl."""
from pkg_resources import get_distribution, DistributionNotFound

__author__ = """Markus Binsteiner"""
__email__ = "makkus@frkl.io"

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = "unknown"
finally:
    del get_distribution, DistributionNotFound
