# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
Lino Presto extension of :mod:`lino.modlib.users`.

.. autosummary::
   :toctree:

    desktop
    fixtures.demo
    fixtures.demo2

"""

from lino.modlib.users import Plugin


class Plugin(Plugin):
    
    extends_models = ['User']

