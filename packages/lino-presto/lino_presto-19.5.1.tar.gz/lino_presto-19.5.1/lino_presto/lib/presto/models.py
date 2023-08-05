# -*- coding: UTF-8 -*-
# Copyright 2017-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals
from builtins import str

from lino.api import dd, rt, _
from django.db import models
from django.conf import settings

from lino.utils import join_elems
from etgen.html import E
# from lino.utils import ssin
from lino.core.fields import IncompleteDateField
from lino.mixins import CreatedModified, BabelDesignated
# from lino_xl.lib.beid.mixins import BeIdCardHolder
from lino_xl.lib.beid.mixins import SSIN
from lino.modlib.comments.mixins import Commentable
from lino.modlib.users.mixins import UserAuthored, My
# from lino.modlib.system.mixins import Lockable

# from lino.modlib.notify.mixins import ChangeNotifier
# from lino_xl.lib.notes.choicelists import SpecialTypes
from lino_xl.lib.clients.mixins import ClientBase
# from lino_xl.lib.notes.mixins import Notable
from lino_presto.lib.contacts.models import Person
# from lino_xl.lib.cal.choicelists import TaskStates
# from lino_xl.lib.cv.mixins import BiographyOwner
# from lino.utils.mldbc.fields import BabelVirtualField
# from lino_xl.lib.courses.mixins import Enrollable
# from lino_xl.lib.healthcare.mixins import HealthcareClient

from lino.mixins.periods import ObservedDateRange

from lino_xl.lib.clients.choicelists import ClientStates
from lino_xl.lib.contacts.choicelists import CivilStates
from lino_xl.lib.products.choicelists import PriceFactors

from lino_xl.lib.contacts.roles import ContactsUser, ContactsStaff
from lino.core.roles import Explorer

contacts = dd.resolve_app('contacts')

# from lino_xl.lib.orders.choicelists import OrderAreas



ClientStates.clear()
add = ClientStates.add_item
add('10', _("Newcomer"), 'newcomer')
add('20', _("Aktiv"), 'active')
add('30', _("Former"), 'former')


class IncomeCategories(dd.ChoiceList):
    verbose_name = _("Income category")
    verbose_name_plural = _("Income categories")

add = IncomeCategories.add_item
add("10", "A")
add("20", "B")
add("30", "C")
add("40", "D")

PriceFactors.clear()
add = PriceFactors.add_item
add("10", IncomeCategories, "income")


class LifeMode(BabelDesignated):
    # 02 allein ohne Kinder
    # 03 allein mit Kindern
    # 21 in Partnerschaft mit Kindern
    # 22 in Partnerschaft ohne Kinder
    # 31 bei Eltern
    # 32 alternierend bei Eltern
    # 35 bei einem Elternteil
    # 37 bei Pflegeeltern
    # 60 Adoptivfamilie
    # 81 in Einrichtung oder WG
    # 90 sonstige Möglichkeit
    # 01 lebt allein (nur alte Akten!)
    # 20 in Partnerschaft (nur alte Akten!)
    # 30 in Familie (nur alte Akten!)
    # 70 in Institution   (nur alte Akten!)
    # 80 Wohngemeinschaft  (nur alte Akten!)

    class Meta:
        app_label = 'presto'
        abstract = dd.is_abstract_model(__name__, 'LifeMode')
        verbose_name = _("Life mode")
        verbose_name_plural = _('Life modes')


class LifeModes(dd.Table):
    model = "presto.LifeMode"


@dd.python_2_unicode_compatible
class Client(Person,  SSIN,
             UserAuthored,
             CreatedModified,
             ClientBase):
    class Meta:
        app_label = 'presto'
        verbose_name = _("Client")
        verbose_name_plural = _("Clients")
        abstract = dd.is_abstract_model(__name__, 'Client')
        # ~ ordering = ['last_name','first_name']

    manager_roles_required = dd.login_required(ContactsStaff)
    validate_national_id = True

    life_mode = dd.ForeignKey('presto.LifeMode', blank=True, null=True)
    civil_state = CivilStates.field(blank=True)

    death_date = IncompleteDateField(
        blank=True, verbose_name=_("Date of death"))

    # translator_notes = dd.RichTextField(
    #     _("Translator"), blank=True, format='plain')
    # translator = dd.ForeignKey(
    #     "avanti.Translator",
    #     blank=True, null=True)

    # unemployed_since = models.DateField(
    #     _("Unemployed since"), blank=True, null=True,
    #     help_text=_("Since when the client has not been employed "
    #                 "in any regular job."))
    # seeking_since = models.DateField(
    #     _("Seeking work since"), blank=True, null=True,
    #     help_text=_("Since when the client is seeking for a job."))
    # work_permit_suspended_until = models.DateField(
    #     blank=True, null=True, verbose_name=_("suspended until"))

    # declared_name = models.BooleanField(_("Declared name"), default=False)

    # is_seeking = models.BooleanField(_("is seeking work"), default=False)
    # removed in chatelet, maybe soon also in Eupen (replaced by seeking_since)

    # unavailable_until = models.DateField(
    #     blank=True, null=True, verbose_name=_("Unavailable until"))
    # unavailable_why = models.CharField(
    #     _("reason"), max_length=100,
    #     blank=True)

    # family_notes = models.TextField(
    #     _("Family situation"), blank=True, null=True)

    # residence_notes = models.TextField(
    #     _("Residential situation"), blank=True, null=True)

    # health_notes = models.TextField(
    #     _("Health situation"), blank=True, null=True)

    # financial_notes = models.TextField(
    #     _("Financial situation"), blank=True, null=True)

    # integration_notes = models.TextField(
    #     _("Integration notes"), blank=True, null=True)

    # availability = models.TextField(
    #     _("Availability"), blank=True, null=True)

    # needed_course = dd.ForeignKey(
    #     'courses.Line', verbose_name=_("Needed activity"),
    #     blank=True, null=True)

    # obstacles = models.TextField(
    #     _("Other obstacles"), blank=True, null=True)
    # skills = models.TextField(
    #     _("Other skills"), blank=True, null=True)

    # client_state = ClientStates.field(
    #     default=ClientStates.newcomer.as_callable)

    # language_notes = dd.RichTextField(
    #     _("Language notes"), blank=True, format='plain')

    def __str__(self):
        return "%s %s (%s)" % (
            self.last_name.upper(), self.first_name, self.pk)

    @dd.displayfield(_("Name"))
    def name_column(self, ar):
        return str(self)

    # def get_overview_elems(self, ar):
    #     elems = super(Client, self).get_overview_elems(ar)
    #     # elems.append(E.br())
    #     elems.append(ar.get_data_value(self, 'eid_info'))
    #     # notes = []
    #     # for obj in rt.models.cal.Task.objects.filter(
    #     #         project=self, state=TaskStates.important):
    #     #     notes.append(E.b(ar.obj2html(obj, obj.summary)))
    #     # if len(notes):
    #     #     notes = join_elems(notes, " / ")
    #     #     elems.append(E.p(*notes, class_="lino-info-yellow"))
    #     return elems

    # def update_owned_instance(self, owned):
    #     owned.project = self
    #     super(Client, self).update_owned_instance(owned)

    # def full_clean(self, *args, **kw):
    #     if self.national_id:
    #         ssin.ssin_validator(self.national_id)
    #     super(Client, self).full_clean(*args, **kw)


dd.update_field(Client, 'user', verbose_name=_("Primary coach"))
# dd.update_field(Client, 'ref', verbose_name=_("Legacy file number"))
dd.update_field(Client, 'client_state', default=ClientStates.active)
dd.update_field(Client, 'overview', verbose_name=None)

from lino_presto.lib.contacts.models import PersonDetail


class ClientDetail(PersonDetail):
    main = "general humanlinks #address client invoicing #more cal.EntriesByProject"

    # general = dd.Panel("""
    # overview:30 general2:20 #courses.EnrolmentsByPupil:30
    # cal.GuestsByPartner
    # """, label=_("General"))

    # general = dd.Panel("""
    # overview:40 general_middle:20
    # general_bottom
    # """, label=_("General"))

    client = dd.Panel("""
    national_id nationality:15 civil_state life_mode
    client_state death_date
    #courses.EnrolmentsByPupil:30 
    topics.InterestsByPartner healthcare.SituationsByClient clients.ContactsByClient      
    """, label=_("Client"))

    invoicing = dd.Panel("""
    invoicing_left:30 orders.OrdersByProject:50
    sales.InvoicesByPartner
    """, label=_("Invoicing"))

    invoicing_left = """
    pf_income
    salesrule__invoice_recipient 
    payment_term salesrule__paper_type
    """

    # address = dd.Panel("""
    # address_box contact_box:30
    #  contacts.RolesByPerson
    # """, label=_("Address"))

    # more = dd.Panel("""
    # #obsoletes  client_state
    # # households.MembersByPerson:30 households.SiblingsByPerson
    # checkdata.ProblemsByOwner ledger.MovementsByPartner
    # #excerpts.ExcerptsByProject
    # """, label=_("More"))

    # career = dd.Panel("""
    # # unemployed_since seeking_since work_permit_suspended_until
    # cv.StudiesByPerson
    # # cv.TrainingsByPerson
    # cv.ExperiencesByPerson:40
    # """, label=_("Career"))

    # competences = dd.Panel("""
    # skills
    # obstacles
    # """, label=_("Competences"))


# Client.hide_elements('street_prefix', 'addr2')


class Clients(contacts.Persons):
    model = 'presto.Client'
    # params_panel_hidden = True
    required_roles = dd.login_required(ContactsStaff)

    # insert_layout = dd.InsertLayout("""
    # first_name last_name
    # national_id
    # gender language
    # """, window_size=(60, 'auto'))

    column_names = "name_column:20 client_state \
    gsm:10 address_column age:10 email phone:10 id language:10 *"

    detail_layout = ClientDetail()

    parameters = ObservedDateRange(
        nationality=dd.ForeignKey(
            'countries.Country', blank=True, null=True,
            verbose_name=_("Nationality")),
        # observed_event=ClientEvents.field(blank=True),
        # client_state=ClientStates.field(blank=True, default='')
    )
    params_layout = """
    #aged_from #aged_to #gender nationality client_state 
    user start_date end_date observed_event 
    """

    @classmethod
    def param_defaults(cls, ar, **kw):
        kw = super(Clients, cls).param_defaults(ar, **kw)
        kw.update(client_state='')
        return kw

    @classmethod
    def get_request_queryset(self, ar):
        """This converts the values of the different parameter panel fields to
        the query filter.


        """
        qs = super(Clients, self).get_request_queryset(ar)
        pv = ar.param_values
        if pv.nationality:
            qs = qs.filter(nationality__exact=pv.nationality)

        # print(20150305, qs.query)

        return qs

    @classmethod
    def get_title_tags(self, ar):
        for t in super(Clients, self).get_title_tags(ar):
            yield t
        pv = ar.param_values

        if pv.nationality:
            yield str(pv.nationality)

        # if pv.client_state:
        #     yield str(pv.client_state)

        # if pv.start_date is None or pv.end_date is None:
        #     period = None
        # else:
        #     period = daterange_text(
        #         pv.start_date, pv.end_date)

    # @classmethod
    # def apply_cell_format(self, ar, row, col, recno, td):
    #     if row.client_state == ClientStates.newcomer:
    #         td.attrib.update(bgcolor="green")

    @classmethod
    def get_row_classes(cls, obj, ar):
        if obj.client_state == ClientStates.newcomer:
            yield 'green'
        if obj.client_state == ClientStates.former:
            yield 'yellow'
        # ~ if not obj.has_valid_card_data():
        # ~ return 'red'


class AllClients(Clients):
    auto_fit_column_widths = False
    column_names = "id client_state \
    life_mode \
    city country zip_code nationality \
    birth_date age:10 gender \
    user"
    detail_layout = None
    required_roles = dd.login_required(Explorer)


class ClientsByNationality(Clients):
    master_key = 'nationality'
    order_by = "city name".split()
    column_names = "city street street_no street_box addr2 name_column country language *"


class MyClients(My, Clients):
    pass


# class ClientsByTranslator(Clients):
#     master_key = 'translator'

from lino_xl.lib.countries.mixins import CountryCity


# from lino_xl.lib.cv.mixins import PersonHistoryEntry, HistoryByPerson


# class Residence(PersonHistoryEntry, CountryCity):

#     allow_cascaded_delete = ['person']

#     class Meta:
#         app_label = 'avanti'
#         verbose_name = _("Residence")
#         verbose_name_plural = _("Residences")

#     reason = models.CharField(_("Reason"), max_length=200, blank=True)


# class Residences(dd.Table):
#     model = 'avanti.Residence'

# class ResidencesByPerson(HistoryByPerson, Residences):
#     label = _("Former residences")
#     column_names = 'country city duration_text reason *'
#     auto_fit_column_widths = True


# @dd.receiver(dd.pre_analyze)
# def inject_cef_level_fields(sender, **kw):
#     for lng in settings.SITE.languages:
#         fld = dd.VirtualField(
#             CefLevel.field(
#                 verbose_name=lng.name, blank=True), cef_level_getter(lng))
#         dd.inject_field(
#             'avanti.Client', 'cef_level_'+lng.prefix, fld)

#     def fc(**kwargs):
#         return (**kwargs)


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     sender.modules.system.SiteConfigs.set_detail_layout("""
#     site_company next_partner_id:10 default_build_method
#     # site_calendar simulate_today hide_events_before
#     # default_event_type max_auto_events
#     """)

# class NotesByPartner(dd.Table):
#     # the project of a note is a course, and the partner of that
#     # course is the master.
#     model = 'notes.Note'
#     master_key = 'project'
#     column_names = "date type subject project user *"


# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     site = sender
#     # site.modules.ledger.Accounts.set_detail_layout("""
#     # ref:10 name id:5
#     # seqno group type clearable
#     # ledger.MovementsByAccount
#     # """)
#
#     site.modules.system.SiteConfigs.set_detail_layout("""
#     site_company next_partner_id:10
#     default_build_method
#     max_auto_events default_event_type site_calendar
#     """)
#
