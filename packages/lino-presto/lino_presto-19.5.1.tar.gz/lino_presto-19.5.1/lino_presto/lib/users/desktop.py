# Copyright 2016-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.modlib.users.desktop import *
from lino.modlib.office.roles import OfficeUser
from lino.api import dd, _


class UserDetail(UserDetail):

    main = "general calendar dashboard.WidgetsByUser"

    general = dd.Panel("""
    box1
    remarks:40 AuthoritiesGiven:20
    """, label=_("General"))

    calendar = dd.Panel("""
    event_type access_class #cash_daybook
    cal.SubscriptionsByUser
    # cal.MembershipsByUser
    """, label=dd.plugins.cal.verbose_name,
                        required_roles=dd.login_required(OfficeUser))

    

    box1 = """
    username user_type:20 partner
    first_name last_name initials
    email language #team
    id created modified
    """

# Users.detail_layout = UserDetail()

