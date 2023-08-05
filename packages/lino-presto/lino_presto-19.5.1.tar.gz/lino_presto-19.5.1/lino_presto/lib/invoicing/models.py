# -*- coding: UTF-8 -*-
# Copyright 2018-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

from lino_xl.lib.invoicing.models import *
from lino.api import _


class Plan(Plan):
    """An extended invoicing plan.

    .. attribute:: order

        If this field is nonempty, select only enrolments of that
        given order.

    """

    class Meta(Plan.Meta):
        app_label = 'invoicing'
        abstract = dd.is_abstract_model(__name__, 'Plan')

    order = dd.ForeignKey('orders.Order', blank=True, null=True)


Plans.detail_layout = """user area today min_date max_date
    partner order
    invoicing.ItemsByPlan
    """


# from lino.modlib.users.mixins import StartPlan
from lino_xl.lib.invoicing.actions import StartInvoicing


class StartInvoicingForOrder(StartInvoicing):
    """Start an invoicing plan for this order.

    This action is installed onto the :class:`orders.Order
    <lino_xl.lib.orders.Order>` model as `start_invoicing`.

    """
    show_in_bbar = True
    select_rows = True
    update_after_start = True

    def get_options(self, ar):
        order = ar.selected_rows[0]
        assert isinstance(order, rt.models.orders.Order)
        return dict(order=order, partner=None, area=order.journal.room.invoicing_area)


@dd.receiver(dd.pre_analyze)
def install_start_action(sender=None, **kwargs):
    rt.models.orders.Order.start_invoicing = StartInvoicingForOrder()
    

