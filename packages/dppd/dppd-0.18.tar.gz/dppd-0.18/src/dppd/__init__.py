# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound as e:  # pragma: no cover
    __version__ = 'unknown' + str(e)
finally:
    del get_distribution, DistributionNotFound

from .base import dppd, register_verb, register_type_methods_as_verbs
from . import single_verbs  # noqa:F401


all = [
    dppd, register_verb, register_type_methods_as_verbs
]
