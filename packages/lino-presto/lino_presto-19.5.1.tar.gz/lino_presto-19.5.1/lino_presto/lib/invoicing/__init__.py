# -*- coding: UTF-8 -*-
# Copyright 2018-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""The :ref:`presto` extension of :mod:`lino_xl.lib.invoicing`.

This adds a new field :attr:`order
<lino_voga.lib.invoicing.models.Plan.order>` to the invoicing plan
and a "basket" button to the Order model.

.. autosummary::
   :toctree:

    models
    fixtures.demo_bookings


"""

from lino_xl.lib.invoicing import Plugin, _


class Plugin(Plugin):

    extends_models = ['Plan']

