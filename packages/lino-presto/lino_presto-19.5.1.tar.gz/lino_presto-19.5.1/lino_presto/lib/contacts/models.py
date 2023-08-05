# -*- coding: UTF-8 -*-
# Copyright 2013-2018 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from __future__ import unicode_literals

from lino.api import dd, rt, _

from lino_xl.lib.contacts.models import *
# from lino_xl.lib.courses.mixins import Enrollable
from lino_xl.lib.beid.mixins import SSIN



class Partner(Partner, mixins.CreatedModified):

    class Meta(Partner.Meta):
        app_label = 'contacts'
        # verbose_name = _("Partner")
        # verbose_name_plural = _("Partners")
        abstract = dd.is_abstract_model(__name__, 'Partner')

    isikukood = models.CharField(
        _("isikukood"), max_length=20, blank=True)

    hidden_columns = 'created modified'

    faculty = None
    """Required by :mod:`lino_xl.lib.working`.
    """

    # def get_overview_elems(self, ar):
    #     # In the base classes, Partner must come first because
    #     # otherwise Django won't inherit `meta.verbose_name`. OTOH we
    #     # want to get the `get_overview_elems` from AddressOwner, not
    #     # from Partner (i.e. AddressLocation).
    #     elems = super(Partner, self).get_overview_elems(ar)
    #     elems += AddressOwner.get_overview_elems(self, ar)
    #     return elems


class PartnerDetail(PartnerDetail):

    main = "general contact #tickets invoicing misc "

    general = dd.Panel("""
    overview:20 general2:20 general3:40
    # notes.NotesByPartner orders.OrdersByPartner
    """, label=_("General"))

    general2 = """
    id language
    url
    """

    # tickets = "tickets.SponsorshipsByPartner"

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    address_box
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    ledger = dd.Panel("""
    vat.VouchersByPartner
    ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)

    invoicing = dd.Panel("""
    invoicing_left:30 #orders.OrdersByProject:50
    sales.InvoicesByPartner
    """, label=_("Invoicing"))

    invoicing_left = """
    pf_income
    salesrule__invoice_recipient 
    payment_term salesrule__paper_type
    """

    purchases = dd.Panel("""
    purchase_account vat_regime vat_id
    ana.InvoicesByPartner
    """, label=_("Purchases"))

    misc = dd.Panel("""
    created modified
    """, label=_("Miscellaneous"))


class Person(Partner, Person):
    """
    Represents a physical person.
    """

    class Meta(Person.Meta):
        app_label = 'contacts'
        # verbose_name = _("Person")
        # verbose_name_plural = _("Persons")
        #~ ordering = ['last_name','first_name']
        abstract = dd.is_abstract_model(__name__, 'Person')

    def get_queryset(self, ar):
        return self.model.objects.select_related('country', 'city')

    def get_print_language(self):
        "Used by DirectPrintAction"
        return self.language

dd.update_field(Person, 'first_name', blank=False)
# dd.update_field(Person, 'last_name', blank=False)

# class PersonDetail(PersonDetail, PartnerDetail):
class PersonDetail(PartnerDetail):

    main = "general contact humanlinks misc cal.GuestsByPartner"

    general = dd.Panel("""
    overview:20 general2:40 #general3:40
    contacts.RolesByPerson:20
    """, label=_("General"))

    general2 = """
    title first_name:15 middle_name:15
    last_name
    gender:10 birth_date age:10
    id language
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    humanlinks = dd.Panel("""
    humanlinks.LinksByHuman:30 
    households.MembersByPerson:20 households.SiblingsByPerson:50
    """, label=_("Human Links"))

    contact = dd.Panel("""
    # lists.MembersByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    # tickets = "tickets.SponsorshipsByPartner"

    misc = dd.Panel("""
    url
    created modified
    # notes.NotesByPartner    
    """, label=_("Miscellaneous"))


class Persons(Persons):

    detail_layout = PersonDetail()


class Company(Partner, Company):
    class Meta(Company.Meta):
        app_label = 'contacts'
        abstract = dd.is_abstract_model(__name__, 'Company')

    # class Meta:
    #     verbose_name = _("Organisation")
    #     verbose_name_plural = _("Organisations")

    # vat_id = models.CharField(_("VAT id"), max_length=200, blank=True)


class CompanyDetail(PartnerDetail):

    main = "general contact invoicing misc"

    ledger = dd.Panel("""
    vat.VouchersByPartner
    ledger.MovementsByPartner
    """, label=dd.plugins.ledger.verbose_name)

    general = dd.Panel("""
    overview:20 general2:40 general3:40
    contacts.RolesByCompany
    """, label=_("General"))

    general2 = """
    prefix:20 name:40
    type vat_id
    url
    """

    general3 = """
    email:40
    phone
    gsm
    fax
    """

    contact = dd.Panel("""
    # lists.MembersByPartner
    remarks:30 sepa.AccountsByPartner
    """, label=_("Contact"))

    address_box = """
    country region city zip_code:10
    addr1
    street_prefix street:25 street_no street_box
    addr2
    """

    # tickets = "tickets.SponsorshipsByPartner"

    misc = dd.Panel("""
    id language
    created modified
    # notes.NotesByPartner
    """, label=_("Miscellaneous"))


# class Companies(Companies):
#     detail_layout = CompanyDetail()


# Partners.set_detail_layout(PartnerDetail())
# Companies.set_detail_layout(CompanyDetail())

# @dd.receiver(dd.post_analyze)
# def my_details(sender, **kw):
#     contacts = sender.modules.contacts

#     contacts.Partners.set_detail_layout(contacts.PartnerDetail())
#     contacts.Companies.set_detail_layout(contacts.CompanyDetail())


class Worker(Person, SSIN):
    class Meta:
        app_label = 'contacts'
        verbose_name = _("Worker")
        verbose_name_plural = _("Workers")
        abstract = dd.is_abstract_model(__name__, 'Worker')

class Workers(Persons):
    model = 'contacts.Worker'
