"""
Implementation of the command-line I{xyscript} tool.
"""
from __future__ import absolute_import

# For backward compatibility
__all__ = ['pullsubmodule', 'initproject', 'package', "pps", 'syn','main']
from xyscript.api import pullsubmodule, initproject, pps, package, syn, main