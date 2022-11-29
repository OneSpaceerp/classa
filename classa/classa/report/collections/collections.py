# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Link",
            "options": "Payment Entry",
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Customer"),
            "fieldname": "party_name",
            "fieldtype": "Data",
            "width": 300
        },
		{
			"label": _("Mode Of Payment"),
			"fieldname": "mode_of_payment",
			"fieldtype": "Data",
			"width": 230
		},
        {
            "label": _("Amount"),
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "width": 120
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""

    if filters.get("customer"):
        conditions += "and `tabPayment Entry`.party = %(customer)s"
    if filters.get("from_date"):
        conditions += " and `tabPayment Entry`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions += " and `tabPayment Entry`.posting_date<=%(to_date)s"
    if filters.get("mode_of_payment"):
        conditions += "and `tabPayment Entry`.mode_of_payment = %(mode_of_payment)s"
    if filters.get("mode_of_payment_type"):
        conditions += "and `tabPayment Entry`.mode_of_payment_type = %(mode_of_payment_type)s"

    item_results = frappe.db.sql("""
        SELECT 
            `tabPayment Entry`.name as voucher_no,
            `tabPayment Entry`.posting_date as posting_date,
            `tabPayment Entry`.party_name as party_name,
            `tabPayment Entry`.mode_of_payment as mode_of_payment,
            `tabPayment Entry`.paid_amount as paid_amount      
        FROM
            `tabPayment Entry`
        WHERE
            `tabPayment Entry`.docstatus = 1
            and `tabPayment Entry`.payment_type = "Receive"
            and `tabPayment Entry`.cheque_status != "مردود"
            and `tabPayment Entry`.party_type = "Customer"
            and `tabPayment Entry`.party != "عميل مسحوبات عاملين"
            and `tabPayment Entry`.mode_of_payment != "مشتريات عاملين"
            {conditions}
        ORDER BY
            `tabPayment Entry`.posting_date desc
        """.format(conditions=conditions), filters, as_dict=1)


    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'voucher_no': item_dict.voucher_no,
                'posting_date': item_dict.posting_date,
                'party_name': item_dict.party_name,
                'mode_of_payment': item_dict.mode_of_payment,
                'paid_amount': item_dict.paid_amount,
            }
            result.append(data)

    return result
