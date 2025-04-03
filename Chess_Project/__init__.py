"""
Chess game package initialization.
Makes all submodules accessible through Chess_Project namespace.
"""

# Define which modules should be available for import
__all__ = ['engine', 'gui', 'utils']

# Enable relative imports between subpackages
from . import engine
from . import gui
from . import utils
