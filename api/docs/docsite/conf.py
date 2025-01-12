import sys
import os
import shlex

from datetime import datetime
from importlib import import_module

sys.path.insert(0, os.path.abspath('./rst/rest_api/_swagger'))

project = u'Distronode API'
copyright = u'2024, Red Hat'
author = u'Red Hat'

pubdateshort = '2024-11-22'
pubdate = datetime.strptime(pubdateshort, '%Y-%m-%d').strftime('%B %d, %Y')

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
# html_title = None
html_title = 'Distronode API community documentation'

# A shorter title for the navigation bar.  Default is the same as html_title.
# html_short_title = None
html_short_title = 'API community documentation'

htmlhelp_basename = 'API_docs'

# include the swagger extension to build rest api reference
#'swagger',
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.ifconfig',
    'sphinx_distronode_theme',
    'notfound.extension',
    'swagger',
]

notfound_urls_prefix = "/projects/api/en/latest/"
notfound_template = "404.rst"

html_theme = 'sphinx_distronode_theme'
html_theme_path = ["_static"]

pygments_style = "distronode"
highlight_language = "YAML+Jinja"

source_suffix = '.rst'
master_doc = 'index'

version = 'latest'
shortversion = 'latest'
# The full version, including alpha/beta/rc tags.
release = 'API latest'

language = 'en'

locale_dirs = ['locale/']  # path is example but recommended.
gettext_compact = False  # optional.

rst_epilog = """
.. |atapi| replace:: *API API Guide*
.. |atrn| replace:: *API Release Notes*
.. |aa| replace:: Distronode Automation
.. |aap| replace:: Distronode Automation Platform
.. |ab| replace:: distronode-builder
.. |at| replace:: API
.. |At| replace:: API
.. |ah| replace:: Automation Hub
.. |EE| replace:: Execution Environment
.. |EEs| replace:: Execution Environments
.. |Ee| replace:: Execution environment
.. |Ees| replace:: Execution environments
.. |ee| replace:: execution environment
.. |ees| replace:: execution environments
.. |versionshortest| replace:: v%s
.. |pubdateshort| replace:: %s
.. |pubdate| replace:: %s
.. |rhel| replace:: Red Hat Enterprise Linux
.. |rhaa| replace:: Red Hat Distronode Automation
.. |rhaap| replace:: Red Hat Distronode Automation Platform
.. |RHAT| replace:: Red Hat Distronode Automation Platform controller

""" % (
    version,
    pubdateshort,
    pubdate,
)
