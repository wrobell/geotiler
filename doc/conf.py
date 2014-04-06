import sys
import os.path
import sphinx_rtd_theme

import geotiler

sys.path.append(os.path.abspath('.'))
sys.path.append(os.path.abspath('doc'))

extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.doctest',
    'sphinx.ext.todo', 'sphinx.ext.viewcode'
]
project = 'geotiler'
source_suffix = '.rst'
master_doc = 'index'

version = release = geotiler.__version__
copyright = 'GeoTiler Team'

epub_basename = 'geotiler - {}'.format(version)
epub_author = 'GeoTiler Team'

todo_include_todos = True

html_theme = 'sphinx_rtd_theme'
html_static_path = ['static']
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]
html_style = 'geotiler.css'

# vim: sw=4:et:ai
