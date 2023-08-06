from ._topfarm import *
from .deprectated_topfarm_problems import *
import pkg_resources

plugins = {
    entry_point.name: entry_point.load()
    for entry_point
    in pkg_resources.iter_entry_points('topfarm.plugins')
}

__version__ = '2.1.0'
__release__ = '2.1.0'


x_key = 'x'
y_key = 'y'
z_key = 'z'
type_key = 'type'
cost_key = 'cost'
