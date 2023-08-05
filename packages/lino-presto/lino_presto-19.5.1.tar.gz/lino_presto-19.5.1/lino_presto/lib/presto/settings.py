# -*- coding: UTF-8 -*-
# Copyright 2018-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.projects.std.settings import *


class Site(Site):
    verbose_name = "Lino Presto"
    url = "http://presto.lino-framework.org"

    # demo_fixtures = 'std demo minimal_ledger euvatrates demo_bookings payments demo2'.split()
    # demo_fixtures = 'std demo minimal_ledger demo_bookings payments demo2'.split()
    # demo_fixtures = 'std minimal_ledger demo demo2'.split()
    demo_fixtures = 'std minimal_ledger demo demo_bookings demo2 checkdata'

    languages = 'en de fr'

    textfield_format = 'html'
    obj2text_template = "**{0}**"
    project_model = 'presto.Client'
    workflows_module = 'lino_presto.lib.presto.workflows'
    custom_layouts_module = 'lino_presto.lib.presto.layouts'
    user_types_module = 'lino_presto.lib.presto.user_types'
    auto_configure_logger_names = "atelier django lino lino_xl lino_presto"
    default_build_method = 'weasy2pdf'

    def get_installed_apps(self):
        yield super(Site, self).get_installed_apps()
        # yield 'lino.modlib.gfks'
        yield 'lino_presto.lib.users'
        yield 'lino_presto.lib.contacts'
        yield 'lino_presto.lib.cal'
        yield 'lino_presto.lib.ledger'
        yield 'lino_presto.lib.orders'
        yield 'lino.modlib.dashboard'
        yield 'lino_xl.lib.countries'
        # yield 'lino_xl.lib.properties'
        yield 'lino_xl.lib.clients'
        yield 'lino_xl.lib.households'
        #yield 'lino_xl.lib.lists'
        yield 'lino_xl.lib.addresses'
        yield 'lino_xl.lib.phones'
        yield 'lino_xl.lib.humanlinks',
        yield 'lino_xl.lib.topics'
        # yield 'lino_xl.lib.extensible'
        yield 'lino_xl.lib.healthcare'
        yield 'lino_presto.lib.products'
        yield 'lino_presto.lib.sales'
        # yield 'lino_xl.lib.vat'
        yield 'lino_presto.lib.invoicing'

        yield 'lino_xl.lib.sepa'
        # yield 'lino_xl.lib.finan'
        # yield 'lino_xl.lib.bevats'
        # yield 'lino_xl.lib.ana'
        # yield 'lino_xl.lib.sheets'

        yield 'lino_xl.lib.notes'
        # yield 'lino_xl.lib.skills'
        yield 'lino.modlib.uploads'
        yield 'lino_xl.lib.excerpts'
        yield 'lino_xl.lib.appypod'
        yield 'lino.modlib.export_excel'
        yield 'lino.modlib.checkdata'
        yield 'lino.modlib.tinymce'
        yield 'lino.modlib.weasyprint'

        yield 'lino_presto.lib.presto'

    def setup_plugins(self):
        super(Site, self).setup_plugins()
        self.plugins.healthcare.configure(client_model='presto.Client')
        self.plugins.topics.configure(menu_group='contacts')
        self.plugins.countries.configure(country_code='BE')
        self.plugins.clients.configure(client_model='presto.Client', menu_group='contacts')
        self.plugins.orders.configure(worker_model='contacts.Worker')
        self.plugins.ledger.configure(purchase_stories=False, sales_stories=False)
        # self.plugins.comments.configure(
        #     commentable_model='tickets.Ticket')

