# -*- coding: UTF-8 -*-
# Copyright 2012-2019 Rumma & Ko Ltd
# This file is part of Lino Presto.
#

"""See :ref:`presto`.

.. autosummary::
   :toctree:

   lib
   projects


"""

from os.path import join, dirname

SETUP_INFO = dict()
# execfile(join(dirname(__file__), 'setup_info.py'))
with open(join(dirname(__file__), 'setup_info.py')) as setup_info:
    exec(setup_info.read())
__version__ = SETUP_INFO['version']
intersphinx_urls = dict(
    docs="http://presto.lino-framework.org",
    dedocs="http://de.presto.lino-framework.org")
srcref_url = 'https://github.com/lino-framework/presto/blob/master/%s'
doc_trees = ['docs', 'dedocs']


