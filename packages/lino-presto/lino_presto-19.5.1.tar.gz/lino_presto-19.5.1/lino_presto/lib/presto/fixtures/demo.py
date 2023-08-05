# -*- coding: UTF-8 -*-
# Copyright 2018-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)
"""Demo data for Lino Presto.

- Create a client MTI child for most persons.

"""
from __future__ import unicode_literals

import datetime
from decimal import Decimal
from django.conf import settings
from django.utils.text import format_lazy

from lino.utils import ONE_DAY
from lino.utils.mti import mtichild
from lino.utils.ssin import generate_ssin
from lino.api import dd, rt, _
from lino.utils import Cycler
from lino.utils import mti
from lino.utils.mldbc import babel_named as named, babeld
from lino.modlib.users.utils import create_user

AMOUNTS = Cycler("5.00", None, None, "15.00", "20.00", None, None)

from lino.utils.quantities import Duration
from lino.core.requests import BaseRequest
from lino_xl.lib.products.choicelists import DeliveryUnits
from lino_xl.lib.ledger.utils import DEBIT, CREDIT
from lino_xl.lib.ledger.choicelists import VoucherStates, JournalGroups
from lino_xl.lib.cal.choicelists import Recurrencies, Weekdays, EntryStates, PlannerColumns

Place = rt.models.countries.Place
Country = rt.models.countries.Country
Role = rt.models.contacts.Role
Partner = rt.models.contacts.Partner
Person = rt.models.contacts.Person
Worker = rt.models.contacts.Worker
LifeMode = rt.models.presto.LifeMode
EventType = rt.models.cal.EventType
Room = rt.models.cal.Room
GuestRole = rt.models.cal.GuestRole
Enrolment = rt.models.orders.Enrolment
OrderItem = rt.models.orders.OrderItem
SalesRule = rt.models.invoicing.SalesRule
User = rt.models.users.User
UserTypes = rt.models.users.UserTypes
Company = rt.models.contacts.Company
Client = rt.models.presto.Client
ClientStates = rt.models.presto.ClientStates
Product = rt.models.products.Product
Tariff = rt.models.invoicing.Tariff
PaperType = rt.models.sales.PaperType
ProductTypes = rt.models.products.ProductTypes
ProductCat = rt.models.products.ProductCat
Account = rt.models.ledger.Account
Topic = rt.models.topics.Topic
Journal = rt.models.ledger.Journal
PriceRule = rt.models.products.PriceRule
Area = rt.models.invoicing.Area
ClientContactType = rt.models.clients.ClientContactType

def objects():

    # yield skills_objects()

    eupen = Place.objects.get(name__exact='Eupen')
    stvith = Place.objects.get(name__exact='Sankt Vith')
    # kettenis = Place.objects.get(name__exact='Kettenis')
    belgium = Country.objects.get(isocode__exact='BE')

    yield named(Topic, _("Health problems"))
    yield named(Topic, _("Handicap"))
    yield named(Topic, _("Messie"))

    yield babeld(LifeMode, _("Single"))
    yield babeld(LifeMode, _("Living together"))
    yield babeld(LifeMode, _("Married couple"))
    yield babeld(LifeMode, _("Family with children"))
    yield babeld(LifeMode, _("Three-generation household"))
    yield babeld(LifeMode, _("Single with children"))

    t1 = babeld(Tariff, _("By presence"), number_of_events=1)
    yield t1

    t10 = babeld(Tariff, _("Maximum 10"), number_of_events=1, max_asset=10)
    yield t10

    obj = Company(
        name="Home Helpers",
        country_id="BE", city=eupen, vat_id="BE12 3456 7890")
    yield obj
    settings.SITE.site_config.update(site_company=obj)

    pt = named(PaperType, _("Service report"), template="service_report.weasy.html")
    yield pt

    for city in (eupen, stvith):
        partner = Company(name="Gemeindeverwaltung {}".format(city), city=city)
        yield partner
        yield SalesRule(partner=partner, paper_type=pt)

    ahmed= Worker(first_name="Ahmed", gender=dd.Genders.male, city=eupen)
    yield ahmed
    maria= Worker(first_name="Maria", gender=dd.Genders.female, city=eupen)
    yield maria

    kw = dd.str2kw('name', _("Employment office"))  # Arbeitsvermittler
    cct = ClientContactType(**kw)
    yield cct
    kw = dict(client_contact_type=cct, country=belgium, city=eupen)
    adg = Company(name=u"Arbeitsamt der D.G.", **kw)
    adg.save()
    yield adg
    bernard = Person.objects.get(name__exact="Bodard Bernard")
    adg_dir = Role(company=adg, person=bernard, type_id=1)
    yield adg_dir

    def cctype(name, **kw):
        return ClientContactType(**dd.str2kw('name', name, **kw))

    yield cctype(_("Landlord"))  # Vermieter
    yield cctype(_("Wealth manager"))  # Verwalter des persönlichen Vermögens
    yield cctype(_("Personal manager"))  # Verwalter des persönlichen Vermögens
    yield cctype(_("Delegated contact"))  # Delegierter Kontakt

    sales_on_services = named(
        Account, _("Sales on services"),
        # sheet_item=CommonItems.sales.get_object(),
        ref="7010")
    yield sales_on_services

    presence = named(ProductCat, _("Fees"))
    yield presence

    consuming = named(ProductCat, _("Consuming items"))
    yield consuming


    et_defaults =dict(force_guest_states=True, default_duration="0:15",
                      planner_column=PlannerColumns.external)

    et_defaults.update(**dd.str2kw('event_label', _("Deployment")))

    garden_et = named(EventType, _("Outside work"), **et_defaults)
    yield garden_et

    home_et = named(EventType, _("Inside work"), **et_defaults)
    yield home_et

    et_defaults.update(planner_column=PlannerColumns.internal)
    office_et = named(EventType, _("Office work"), **et_defaults)
    yield office_et

    worker = named(GuestRole, _("Worker"))
    yield worker
    yield named(GuestRole, _("Guest"))

    AREAS = Cycler(Area.objects.all())

    order_stories = []

    def team(name, et, gr, **order_options):
        kwargs = {}
        kwargs.setdefault('invoicing_area', AREAS.pop())
        kwargs.setdefault('event_type', et)
        kwargs.setdefault('guest_role', gr)
        obj = Room(**dd.str2kw('name', name, **kwargs))
        order_stories.append([obj, order_options])
        return obj

    order_options = {}
    order_options.update(max_events=3)
    yield team(_("Garden"), garden_et, worker, **order_options)
    order_options.update(max_events=1)
    yield team(_("Moves"), garden_et, worker, **order_options)
    order_options.update(max_events=2)
    yield team(_("Renovation"), home_et, worker, **order_options)
    order_options.update(max_events=10)
    yield team(_("Home help"), home_et, worker, **order_options)
    order_options.update(max_events=50)
    yield team(_("Home care"), home_et, worker, **order_options)
    order_options.update(max_events=1)
    yield team(_("Office"), office_et, worker, **order_options)

    def product(pt, name, unit, **kwargs):
        return Product(**dd.str2kw('name', name,
                       delivery_unit=DeliveryUnits.get_by_name(unit),
                       product_type=ProductTypes.get_by_name(pt), **kwargs))

    yield product('default', _("Ironing of a shirt"), 'piece')
    yield product('default', _("Ironing of a pair of trousers"), 'piece')
    yield product('default', _("Ironing of a skirt"), 'piece')
    yield product('default', _("Washing per Kg"), 'kg')

    for i, ic in enumerate(rt.models.presto.IncomeCategories.get_list_items()):
        work = named(
            Product, format_lazy("{} {}", _("Work by hour"), ic),
            sales_account=sales_on_services,
            sales_price=Decimal("3.75") * (i+1), cat=presence,
            product_type=ProductTypes.default)
        yield work
        yield PriceRule(event_type=garden_et, fee=work, pf_income=ic)
        yield PriceRule(event_type=home_et, fee=work, pf_income=ic)


    yield named(
        Product, _("Travel per Km"),
        sales_price=0.50, sales_account=sales_on_services, cat=consuming,
        product_type=ProductTypes.default)
    yield named(
        Product, _("Other consuming items"),
        sales_price=1.50, sales_account=sales_on_services, cat=consuming,
        product_type=ProductTypes.default)

    yield named(Product, _("Other"), sales_price=35)

    # yield create_user("ahmed", UserTypes.worker,
    #                   event_type=garden_et, partner=ahmed)
    # yield create_user("maria", UserTypes.worker, event_type=home_et, partner=maria)
    yield create_user("martha", UserTypes.secretary)


    invoice_recipient = None
    for n, p in enumerate(Partner.objects.all()):
        if n % 10 == 0:
            if not hasattr(p, 'salesrule'):
                yield SalesRule(
                    partner=p, invoice_recipient=invoice_recipient)
        else:
            invoice_recipient = p

    def person2client(p, **kw):
        c = mti.insert_child(p, Client)
        for k, v in kw.items():
            setattr(c, k, v)
        c.client_state = ClientStates.active
        c.save()
        return Client.objects.get(pk=p.pk)


    count = 0
    for person in Person.objects.exclude(gender=''):
        if not person.birth_date:  # not those from humanlinks
            if User.objects.filter(partner=person).count() == 0:
                if rt.models.contacts.Role.objects.filter(person=person).count() == 0:
                    birth_date = settings.SITE.demo_date(-170 * count - 16 * 365)
                    national_id = generate_ssin(birth_date, person.gender)

                    client = person2client(person,
                                           national_id=national_id,
                                           birth_date=birth_date)
                    # youngest client is 16; 170 days between each client

                    count += 1
                    if count % 2:
                        client.client_state = ClientStates.active
                    elif count % 5:
                        client.client_state = ClientStates.newcomer
                    else:
                        client.client_state = ClientStates.former

                    # Dorothée is three times in our database
                    if client.first_name == "Dorothée":
                        client.national_id = None
                        client.birth_date = ''

                    client.full_clean()
                    client.save()

    INCOMES = Cycler(rt.models.presto.IncomeCategories.get_list_items())
    for obj  in Client.objects.all():
        obj.pf_income = INCOMES.pop()
        yield obj

    # JOURNALS

    # rt.models.ledger.Journal.objects.get(ref="SLS").delete()
    # rt.models.ledger.Journal.objects.get(ref="SLC").delete()

    kw = dict(journal_group=JournalGroups.sales)
    MODEL = rt.models.sales.InvoicesByJournal
    # MODEL = rt.models.vat.InvoicesByJournal
    kw.update(ref="MAN", dc=CREDIT, trade_type="sales")
    # kw.update(printed_name=_("Mission"))
    kw.update(dd.str2kw('name', _("Manual invoices")))
    yield MODEL.create_journal(**kw)

    # create one orders journal for every team

    kw = dict(journal_group=JournalGroups.orders)
    MODEL = rt.models.orders.OrdersByJournal

    kw.update(dc=CREDIT, trade_type="sales")
    kw.update(printed_name=_("Order"))
    # for room in rt.models.cal.Room.objects.all():
    for story in order_stories:
        room = story[0]
        # kw.update(dd.str2kw('name', _("Orders")))
        kw.update(room=room)
        kw.update(ref=room.name)
        kw.update(name=room.name)
        obj = MODEL.create_journal(**kw)
        story.append(obj)
        yield obj


    CLIENTS = Cycler(Client.objects.all())
    # Client.objects.filter(client_state=ClientStates.coached))
    OFFSETS = Cycler(1, 0, 0, 1, 1, 1, 1, 2)
    START_TIMES = Cycler("8:00", "9:00", "11:00", "13:00", "14:00")
    DURATIONS = Cycler([Duration(x) for x in ("1:00", "0:30", "2:00", "3:00", "4:00")])
    WORKERS = Cycler(Worker.objects.all())
    ITEM_PRODUCTS = Cycler(Product.objects.filter(cat=consuming))
    USERS = Cycler(User.objects.exclude(user_type=""))
    EVERY_UNITS = Cycler([Recurrencies.get_by_value(x) for x in "ODWM"])

    num = 0
    # entry_date = datetime.date(dd.plugins.ledger.start_year, 1, 1)
    entry_date = dd.today(-70)
    for i in range(2):
        for story in order_stories:
            room, order_options, journal = story
            num += 1
            entry_date += ONE_DAY

            user = USERS.pop()
            st = START_TIMES.pop()
            et = str(st + DURATIONS.pop())
            # A Duration is not a valid type for a TimeField (Django says
            # "expected string or bytes-like object")
            # print(20190501, st, et)
            order_options.update(entry_date=entry_date)
            order_options.update(start_date=entry_date+datetime.timedelta(days=OFFSETS.pop()))
            order_options.update(start_time=st)
            order_options.update(end_time=et)
            order_options.update(project=CLIENTS.pop())
            order_options.update(every_unit=EVERY_UNITS.pop())
            order_options.update(user=user)
            # order_options.update(max_events=MAX_EVENTS.pop())
            obj = journal.create_voucher(**order_options)
            # if obj.every_unit = Recurrencies.D:
            #     obj.monday = True
            yield obj  # save a first time because we want to create related objects
            yield Enrolment(order=obj, worker=WORKERS.pop())
            if num % 5 == 0:
                yield Enrolment(order=obj, worker=WORKERS.pop())
            yield OrderItem(voucher=obj, product=ITEM_PRODUCTS.pop(), qty="20")
            # ar = rt.login(user)
            ar = BaseRequest(user=user)
            obj.register(ar)
            obj.update_auto_events(ar)
            # obj.full_clean()
            # obj.save()
            # print(20190501, obj.every_unit)
            yield obj  # save a second time after registering


    qs = rt.models.cal.Event.objects.filter(
        start_date__lt=dd.today(-10))
    for e in qs:
        if e.id % 5:
            e.state = EntryStates.took_place
        else:
            e.state = EntryStates.missed
        yield e
