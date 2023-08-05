# -*- coding: UTF-8 -*-
# Copyright 2017-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""Defines the user types for Lino Presto.

This is used as the :attr:`user_types_module
<lino.core.site.Site.user_types_module>` for Presto sites.

Redefines the choices in :class:`lino.modlib.users.UserTypes`.

"""

from __future__ import unicode_literals

from lino.api import _
from lino.modlib.users.choicelists import UserTypes
from lino.core.roles import UserRole, SiteAdmin, SiteUser, SiteStaff
from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino_xl.lib.products.roles import ProductsUser, ProductsStaff
from lino_xl.lib.excerpts.roles import ExcerptsUser, ExcerptsStaff
from lino_xl.lib.orders.roles import OrdersUser, OrdersStaff
from lino.modlib.office.roles import OfficeStaff, OfficeUser
from lino_xl.lib.cal.roles import GuestOperator
from lino_xl.lib.ledger.roles import LedgerStaff
from lino_xl.lib.sepa.roles import SepaUser, SepaStaff
from lino_xl.lib.topics.roles import TopicsUser


class Secretary(SiteStaff, ContactsUser, OfficeUser,
                GuestOperator, TopicsUser,
                LedgerStaff, SepaUser, OrdersUser, ExcerptsUser,
                ProductsStaff):
    pass


class Worker(SiteUser, ContactsUser, OfficeUser,
                GuestOperator,
                SepaUser, OrdersStaff, ExcerptsUser,
                ProductsUser):
    pass


class SiteAdmin(SiteAdmin, ContactsStaff, OfficeStaff,
                GuestOperator, LedgerStaff, SepaStaff, OrdersStaff,
                ExcerptsStaff, ProductsStaff, TopicsUser):
    pass

UserTypes.clear()

add = UserTypes.add_item

add('000', _("Anonymous"), UserRole, name='anonymous', readonly=True)
add('100', _("Secretary"), Secretary, name="secretary")
add('200', _("Worker"), Worker, name="worker")
add('900', _("Administrator"), SiteAdmin, name='admin')

