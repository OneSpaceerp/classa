# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("الفاتورة"),
            "fieldname": "sales_invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120
        },
        {
            "label": _("التاريخ"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("اسم العميل"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 220
        },
        {
            "label": _("مندوب المبيعات"),
            "fieldname": "sales_person",
            "fieldtype": "Link",
            "options": "Sales Person",
            "width": 220
        },
        {
            "label": _("المبيعات"),
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("المرتجعات"),
            "fieldname": "returns_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("الخصومات"),
            "fieldname": "discount_amount",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("التحصيلات"),
            "fieldname": "payment_entries",
            "fieldtype": "Currency",
            "width": 150
        },
        {
            "label": _("المتبقي"),
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 150
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    if filters.get("sales_person"):
        conditions += " and `tabSales Invoice`.sales_person=%(sales_person)s"
    if filters.get("from_date"):
        conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"

    result = []
    item_results = frappe.db.sql("""
            SELECT 
                `tabSales Invoice`.name as sales_invoice,
                `tabSales Invoice`.posting_date as posting_date,
                `tabSales Invoice`.sales_person as sales_person,
                `tabSales Invoice`.outstanding_amount as outstanding_amount,
                `tabSales Invoice`.customer as customer,
                
                if ((Select sum(`tabSales Invoice Item`.discount_amount) from `tabSales Invoice Item` 
                where `tabSales Invoice Item`.parent = `tabSales Invoice`.name) > 0, 
                (Select sum(`tabSales Invoice Item`.discount_amount) from `tabSales Invoice Item` 
                where `tabSales Invoice Item`.parent = `tabSales Invoice`.name) ,0) as discount_amount,
                
                if (`tabSales Invoice`.is_return = 0, `tabSales Invoice`.grand_total, 0) as grand_total,
                if (`tabSales Invoice`.is_return = 1, -1*(`tabSales Invoice`.grand_total), 0) as returns_amount
                
            FROM
                `tabSales Invoice`
            WHERE
                `tabSales Invoice`.docstatus = 1
                {conditions}

            ORDER BY `tabSales Invoice`.posting_date desc
            """.format(conditions=conditions), filters, as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'sales_person': item_dict.sales_person,
                'sales_invoice': item_dict.sales_invoice,
                'outstanding_amount': item_dict.outstanding_amount,
                'customer': item_dict.customer,
                'grand_total': item_dict.grand_total,
                'returns_amount': item_dict.returns_amount,
                'discount_amount': item_dict.discount_amount,
                'posting_date': item_dict.posting_date,
                'payment_entries': item_dict.grand_total - item_dict.outstanding_amount,
            }
            result.append(data)
    return result

