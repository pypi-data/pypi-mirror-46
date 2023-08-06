"""
hiPhive module.
"""

from .cluster_space import ClusterSpace
from .structure_container import StructureContainer
from .force_constant_potential import ForceConstantPotential
from .force_constants import ForceConstants
from .core.config import config
from .core.rotational_constraints import enforce_rotational_sum_rules

# check versions
from warnings import warn
from distutils.version import StrictVersion

from numpy import __version__ as np_version
if StrictVersion(np_version) < StrictVersion('1.12'):
    warn('\n'
         ' The numpy module is outdated (version {}).\n'
         ' hiphive requires at least numpy version 1.12.\n'
         ' Some functionality might not work as expected.\n'
         .format(np_version))

# clean up imports
del np_version
del warn, StrictVersion

__project__ = 'hiPhive'
__description__ = 'High-order force constants for the masses'
__authors__ = ['Fredrik Eriksson',
               'Erik Fransson',
               'Paul Erhart']
__copyright__ = '2018-2019'
__license__ = 'MIT'
__credits__ = ['Fredrik Eriksson',
               'Erik Fransson',
               'Paul Erhart']
__version__ = '0.4.1'
__all__ = ['ClusterSpace',
           'StructureContainer',
           'ForceConstantPotential',
           'ForceConstants',
           'config',
           'enforce_rotational_sum_rules',
           'io']
__maintainer__ = 'The hiPhive developers team'
__maintainer_email__ = 'hiphive@materialsmodeling.org'
__status__ = 'beta-version'
__url__ = 'http://hiphive.materialsmodeling.org/'
