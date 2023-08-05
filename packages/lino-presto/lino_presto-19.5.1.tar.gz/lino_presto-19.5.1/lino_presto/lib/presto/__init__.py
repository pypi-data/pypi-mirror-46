# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

"""
The main plugin for Lino Presto.

.. autosummary::
   :toctree:

    user_types

"""


from lino.api import ad, _
from itertools import groupby


class Plugin(ad.Plugin):
    "See :class:`lino.core.plugin.Plugin`."

    verbose_name = _("Master")

    needs_plugins = ['lino_xl.lib.countries']

    municipality_type = '50'

    def setup_main_menu(self, site, user_type, m):
        mg = site.plugins.contacts
        m = m.add_menu(mg.app_label, mg.verbose_name)
        # m.add_separator()
        m.add_action('presto.Clients')
        # m.add_action('presto.MyClients')
        # m.add_action('presto.Translators')
        # m.add_action('courses.CourseProviders')
        # m.add_action('coachings.CoachedClients')
        # m.add_action('coachings.MyCoachings')

    def setup_config_menu(self, site, user_type, m):
        mg = site.plugins.contacts
        # mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('presto.LifeModes')

    def setup_explorer_menu(self, site, user_type, m):
        mg = site.plugins.contacts
        # mg = self.get_menu_group()
        m = m.add_menu(mg.app_label, mg.verbose_name)
        m.add_action('presto.AllClients')

    def walk_invoice_entries(self, obj):
        # used by sales/service_report.weasy.html
        # from lino.core.gfks import gfk2lookup
        if obj.partner is None or obj.partner.city_id is None:
            return []
        if obj.invoicing_max_date is None:
            return []

        places = set()

        def collect(pl):  # calls itself
            places.add(pl)
            for spl in self.site.models.countries.Place.objects.filter(parent=pl):
                collect(spl)

        collect(obj.partner.city)
        # print("20190506", places)
        qs = self.site.models.cal.Event.objects.filter(
            start_date__lte=obj.invoicing_max_date)
        if obj.invoicing_min_date is not None:
            qs = qs.filter(start_date__gte=obj.invoicing_min_date)
        qs = qs.filter(project__city__in=places)
        # qs = qs.filter(invoicings__voucher__partner__city__in=places)
        qs = qs.filter(state=self.site.models.cal.EntryStates.took_place)
        # qs = qs.filter(**gfk2lookup(obj.__class__.owner, ))
        qs = qs.order_by('project__name', 'start_date', 'start_time')
        return groupby(qs, lambda x: x.project)
