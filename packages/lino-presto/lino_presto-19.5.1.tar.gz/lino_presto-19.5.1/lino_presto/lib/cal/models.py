# -*- coding: UTF-8 -*-
# Copyright 2013-2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from __future__ import unicode_literals

from builtins import str
import six

from django.utils.translation import ugettext_lazy as _
from lino.core.gfks import gfk2lookup

from lino_xl.lib.cal.models import *
from etgen.html import E

from lino.modlib.users.choicelists import UserTypes

from lino_xl.lib.courses.choicelists import EnrolmentStates
from lino_xl.lib.invoicing.mixins import InvoiceGenerator

# courses = dd.resolve_app('courses')

# must import this to activate these workflow definitions:
# 20160622 this is now done by workflows_module
# from . import workflows
# from lino_xl.lib.cal.workflows import voga


from lino.modlib.office.roles import OfficeUser


class Room(Room, Referrable):

    ref_max_length = 5

    class Meta(Room.Meta):
        abstract = dd.is_abstract_model(__name__, 'Room')
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")

    event_type = dd.ForeignKey('cal.EventType',blank=True, null=True)
    guest_role = dd.ForeignKey("cal.GuestRole", blank=True, null=True)
    invoicing_area = dd.ForeignKey('invoicing.Area', blank=True, null=True)


class RoomDetail(dd.DetailLayout):
    main = """
    ref name invoicing_area id
    event_type guest_role display_color
    company contact_person contact_role 
    cal.EntriesByRoom
    """


class Rooms(Rooms):
    column_names = "name event_type *"


# @dd.python_2_unicode_compatible
class Event(Event, InvoiceGenerator):

    class Meta(Event.Meta):
        abstract = dd.is_abstract_model(__name__, 'Event')
        
    # invoiceable_date_field = 'start_date'
    invoiceable_partner_field = 'project'

    def long_fmt(self, pv):
        t = []
        if self.start_time:
            t.append(str(self.start_time)[:5])
        if not pv.project and self.project:
            t.append(str(self.project))
            t.append(self.project.city.name)
        if not pv.room and self.room and self.room.ref:
            t.append(self.room.ref)
        if self.summary:
            t.append(self.summary)
        return " ".join(t)


    def short_fmt(self, pv):
        t = []
        if self.start_time:
            t.append(str(self.start_time)[:5])
        if not pv.room and self.room and self.room.ref:
            t.append(self.room.ref)
        return " ".join(t)

    def calendar_fmt(self, pv):
        ele = E.span(self.long_fmt(pv))
        if self.room:
            data_color = self.room.get_diplay_color()
        if self.room:
            dot  = E.span(u"\u00A0",CLASS="dot")
            # ele.attrib['style'] = "color: white;background-color: {};".format(data_color)
            dot.attrib['style'] = "background-color: {};".format(data_color)
            return E.div(*[dot,ele])
        else:
            return E.div(*[ele])


    def get_invoiceable_partner(self):
        ord = self.owner
        if isinstance(ord, rt.models.orders.Order):
            return ord.invoice_recipient or ord.project

    def get_invoiceable_product(self, max_date=None):
        par = self.get_invoiceable_partner()
        # par = self.project
        # if self.project_id is None:
        if par is None:
            return None
        return rt.models.products.Product.get_rule_fee(par, self.event_type)

    def get_invoiceable_qty(self):
        qty = self.get_duration()
        if qty is not None:
            return Duration(qty)
        if self.event_type_id:
            return self.event_type.default_duration or self.default_invoiceable_qty
        return self.default_invoiceable_qty

    def get_event_summary(self, ar):
        # Overrides lino_xl.lib.cal.Event.get_event_summary
        if self.owner is None:
            return self.summary
        else:
            return str(self.owner)

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        # pre-select all Event objects that potentially will generate
        # an invoice.

        qs = cls.objects.all()
        qs = qs.filter(state=EntryStates.took_place)
        if plan.area_id:
            qs = qs.filter(room__invoicing_area=plan.area)

        if plan.order is not None:
            qs = qs.filter(**gfk2lookup(cls.owner, plan.order))

        # dd.logger.info("20181113 c %s", qs)

        if partner is None:
            partner = plan.partner

        if partner is None:
            # only courses with a partner (because only these get invoiced
            # per course).
            qs = qs.filter(project__isnull=False)
        else:
            q1 = models.Q(
                project__salesrule__invoice_recipient__isnull=True,
                project=partner)
            q2 = models.Q(
                project__salesrule__invoice_recipient=partner)
            qs = qs.filter(models.Q(q1 | q2))

        # dd.logger.info("20190328 %s (%d rows)", qs.query, qs.count())
        return qs.order_by('id')

    # def __str__(self):
    #     if self.owner is None:
    #         if six.PY2:
    #             return super(Event, self).__unicode__()
    #         else:
    #             return super(Event, self).__str__()
    #         # a simple super() fails because of
    #         # python_2_unicode_compatible
    #     owner = self.owner._meta.verbose_name + " #" + str(self.owner.pk)
    #     return "%s %s" % (owner, self.summary)

    # def suggest_guests(self):
    #     # print "20130722 suggest_guests"
    #     for g in super(Event, self).suggest_guests():
    #         print("20190328 suggesting super {}".format(g))
    #         yield g
    #     order = self.owner
    #     if not isinstance(order, rt.models.orders.Order):
    #         # e.g. None or RecorrentEvent
    #         return
    #     Guest = settings.SITE.models.cal.Guest
    #     for obj in order.enrolments_by_order.all():
    #         if obj.worker:
    #             print("20190328 suggesting worker {}".format(obj.worker))
    #             yield Guest(event=self,
    #                         partner=obj.worker,
    #                         role=obj.guest_role)

    def get_invoice_items(self, info, invoice, ar):
        # dd.logger.info("20181116a %s", self)
        for i in super(Event, self).get_invoice_items(info, invoice, ar):
            # print(i.qty)
            yield i
            for oi in self.owner.items.all():
                kwargs = dict(
                    invoiceable=self,
                    product=oi.product,
                    qty=oi.qty)
                yield invoice.add_voucher_item(**kwargs)

dd.update_field(Event, 'description',format="plain")

class EventDetail(EventDetail):
    main = "general more"
    general = dd.Panel("""
    event_type summary user
    start end
    room priority access_class transparent #rset
    owner:30 project workflow_buttons:30
    cal.GuestsByEvent description 
    """, _("General"))

    more = dd.Panel("""
    id created:20 modified:20 state
    # outbox.MailsByController  notes.NotesByOwner
    invoicing.InvoicingsByGenerator
    """, _("More"))


class MyEntries(MyEntries):
    column_names = 'when_text summary room owner workflow_buttons *'



class GuestsByEvent(GuestsByEvent):
    column_names = 'partner role #workflow_buttons remark *'
