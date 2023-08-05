# -*- coding: UTF-8 -*-
# Copyright 2019 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)

from lino.api import _
from lino_xl.lib.sales.models import *

class InvoiceDetail(InvoiceDetail):

    # main = "general more ledger"

    right_panel = dd.Panel("""
    #total_base #total_vat
    
    printed
    workflow_buttons
    """)

    invoice_header = dd.Panel("""
    entry_date partner invoicing_min_date invoicing_max_date
    subject your_ref paper_type 
    payment_term due_date:20 total_incl 
    """, label=_("Header"))  # sales_remark

    general = dd.Panel("""
    invoice_header:60 right_panel:20
    ItemsByInvoice
    """, label=_("General"))

    more = dd.Panel("""
    id user language project #item_vat
    intro
    """, label=_("More"))

    ledger = dd.Panel("""
    vat_regime #voucher_date journal accounting_period number match 
    ledger.MovementsByVoucher
    """, label=_("Ledger"))



ItemsByInvoice.column_names = "product title unit_price qty total_incl invoiceable *"


# class InvoiceItem(InvoiceItem):
#     class Meta:
#         app_label = 'sales'
#         abstract = dd.is_abstract_model(__name__, 'InvoiceItem')
#         verbose_name = _("Product invoice item")
#         verbose_name_plural = _("Product invoice items")


class InvoiceItemDetail(InvoiceItemDetail):
    main = """
    seqno product discount
    unit_price qty total_base total_vat total_incl
    title
    invoiceable_type:15 invoiceable_id:15 invoiceable:50
    description
    """


VatProductInvoice.print_items_table = ItemsByInvoicePrintNoQtyColumn
dd.update_field(
    VatProductInvoice, 'subject', verbose_name=_("Our reference"))
dd.update_field(
    VatProductInvoice, 'total_incl', verbose_name=_("Total amount"))
dd.update_field(
    InvoiceItem, 'total_incl', verbose_name=_("Total amount"))


