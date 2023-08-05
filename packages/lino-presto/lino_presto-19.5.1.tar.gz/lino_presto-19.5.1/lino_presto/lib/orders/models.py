# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino_xl.lib.orders.models import *
from lino.api import _


class Enrolment(Enrolment):

    # class Meta(Enrolment.Meta):
    #     app_label = 'orders'
    #     abstract = dd.is_abstract_model(__name__, 'Enrolment')
    #     verbose_name = _("Enrolment")
    #     verbose_name_plural = _('Enrolments')
    #     unique_together = ('order', 'worker')

    def get_guest_role(self):
        return self.guest_role or self.order.journal.room.guest_role


# class Missions(Orders):
#     label = _("Missions")
#
#
# class Contracts(Orders):
#     label = _("Contracts")


# OrderAreas.clear()
# add = OrderAreas.add_item
# add('100', _("Missions"), 'default', 'orders.Missions')
# add('200', _("Contracts"), 'contracts', 'orders.Contracts')


