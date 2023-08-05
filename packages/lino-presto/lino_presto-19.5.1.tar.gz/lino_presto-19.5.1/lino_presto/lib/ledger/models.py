# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import _
from lino_xl.lib.ledger.models import *

class JournalDetail(JournalDetail):

    main = """
    name ref:5
    journal_group:15 voucher_type:20 trade_type:20 seqno:5 id:5 room
    account partner build_method:20 template:20 uploads_volume 
    dc force_sequence #invert_due_dc yearly_numbering auto_fill_suggestions auto_check_clearings must_declare
    printed_name 
    MatchRulesByJournal
    """


# JournalGroups.clear()
add = JournalGroups.add_item
add("05", _("Orders"), 'orders', menu_group=dd.plugins.orders)
# add("10", _("Sales"), 'sales', menu_group=dd.plugins.sales)
JournalGroups.sort()
