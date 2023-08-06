import os
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

def setup(app):
   app.add_html_theme('sphinx_pyviz_theme', os.path.abspath(os.path.dirname(__file__)))
