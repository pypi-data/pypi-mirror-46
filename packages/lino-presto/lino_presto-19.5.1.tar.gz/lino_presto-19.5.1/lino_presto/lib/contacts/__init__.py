# -*- coding: UTF-8 -*-
# Copyright 2014-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
An extension of :mod:`lino_xl.lib.contacts`
"""

from lino_xl.lib.contacts import Plugin


class Plugin(Plugin):
    extends_models = ['Partner', 'Person', 'Company']

    # Override to add Workers Menu
    def setup_main_menu(self, site, user_type, m):
        m = m.add_menu(self.app_label, self.verbose_name)
        # We use the string representations and not the classes because
        # other installed applications may want to override these tables.
        for a in ('contacts.Workers', 'contacts.Companies', 'contacts.Persons'):
            m.add_action(a)
