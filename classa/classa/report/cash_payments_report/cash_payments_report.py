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
            "label": _("Voucher Type"),
            "fieldname": "voucher_type",
            "fieldtype": "Data",
            "width": 160
        },
        {
            "label": _("Voucher No"),
            "fieldname": "voucher_no",
            "fieldtype": "Dynamic Link",
            "options": "voucher_type",
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Type"),
            "fieldname": "payment_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Party Type"),
            "fieldname": "party_type",
            "fieldtype": "Data",
            "width": 140
        },
        {
            "label": _("Party"),
            "fieldname": "party",
            "fieldtype": "Data",
            "width": 230
        },
        {
            "label": _("Debit"),
            "fieldname": "debit",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Credit"),
            "fieldname": "credit",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": _("Balance"),
            "fieldname": "balance",
            "fieldtype": "Currency",
            "width": 120
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions1 = ""
    conditions2 = ""
    conditions3 = ""

    if filters.get("from_date"):
        conditions1 += " and `tabPayment Entry`.posting_date>=%(from_date)s"
        conditions2 += " and `tabLoan Disbursement`.posting_date>=%(from_date)s"
        conditions3 += " and `tabPayment Entry`.posting_date>=%(from_date)s"
    if filters.get("to_date"):
        conditions1 += " and `tabPayment Entry`.posting_date<=%(to_date)s"
        conditions2 += " and `tabLoan Disbursement`.posting_date<=%(to_date)s"
        conditions3 += " and `tabPayment Entry`.posting_date<=%(to_date)s"
    if filters.get("mode_of_payment"):
        conditions1 += "and `tabPayment Entry`.mode_of_payment = %(mode_of_payment)s "
        conditions2 += "and `tabLoan`.mode_of_payment = %(mode_of_payment)s "
        conditions3 += "and `tabPayment Entry`.mode_of_payment_2 = %(mode_of_payment)s "

    item_results1 = frappe.db.sql("""
        SELECT 
            `tabPayment Entry`.name as voucher_no,
            `tabPayment Entry`.posting_date as posting_date,
            IF(`tabPayment Entry`.payment_type != "Internal Transfer", `tabPayment Entry`.payment_type, "Internal Transfer To") as payment_type,            
            IF(`tabPayment Entry`.payment_type != "Internal Transfer", `tabPayment Entry`.party_type, "Mode of Payment") as party_type,
            IF(`tabPayment Entry`.payment_type != "Internal Transfer", `tabPayment Entry`.party_name, `tabPayment Entry`.mode_of_payment_2) as party,
            IF(`tabPayment Entry`.payment_type = "Receive", `tabPayment Entry`.paid_amount, 0) as debit,
            IF(`tabPayment Entry`.payment_type in ("Internal Transfer", "Pay"), `tabPayment Entry`.paid_amount, 0) as credit      
        FROM
            `tabPayment Entry`
        WHERE
            `tabPayment Entry`.docstatus = 1
            {conditions1}
        ORDER BY
            `tabPayment Entry`.posting_date desc
        """.format(conditions1=conditions1), filters, as_dict=1)

    item_results2 = frappe.db.sql("""
        SELECT 
            `tabLoan Disbursement`.name as voucher_no,
            `tabLoan Disbursement`.posting_date as posting_date,
            `tabLoan`.loan_type as payment_type,
            `tabLoan`.applicant_type as party_type,
            `tabLoan`.applicant_name as party,
            `tabLoan Disbursement`.disbursed_amount as credit
        FROM
            `tabLoan Disbursement` join `tabLoan` on `tabLoan`.name = `tabLoan Disbursement`.against_loan
        WHERE
            `tabLoan Disbursement`.docstatus = 1
            and `tabLoan`.loan_type = "عجز مناديب"
            {conditions2}
        ORDER BY
            `tabLoan Disbursement`.posting_date desc
        """.format(conditions2=conditions2), filters, as_dict=1)

    item_results3 = frappe.db.sql("""
            SELECT 
                `tabPayment Entry`.name as voucher_no,
                `tabPayment Entry`.posting_date as posting_date,
                `tabPayment Entry`.mode_of_payment as party,
                `tabPayment Entry`.paid_amount as debit
            FROM
                `tabPayment Entry`
            WHERE
                `tabPayment Entry`.docstatus = 1
                and `tabPayment Entry`.payment_type = "Internal Transfer"
                {conditions3}
            ORDER BY
                `tabPayment Entry`.posting_date desc
            """.format(conditions3=conditions3), filters, as_dict=1)


    result = []
    if item_results1:
        for item_dict in item_results1:
            data = {
                'voucher_type': "Payment Entry",
                'voucher_no': item_dict.voucher_no,
                'posting_date': item_dict.posting_date,
                'party_type': item_dict.party_type,
                'party': item_dict.party,
                'debit': item_dict.debit,
                'credit': item_dict.credit,
                'payment_type': item_dict.payment_type,
                'balance': item_dict.debit - item_dict.credit,
            }
            result.append(data)

    if item_results2:
        for item_dict in item_results2:
            data = {
                'voucher_type': "Loan Disbursement",
                'voucher_no': item_dict.voucher_no,
                'posting_date': item_dict.posting_date,
                'party_type': item_dict.party_type,
                'party': item_dict.party,
                'debit': 0,
                'credit': item_dict.credit,
                'payment_type': item_dict.payment_type,
                'balance': - 1 * item_dict.credit,
            }
            result.append(data)

    if item_results3:
        for item_dict in item_results3:
            data = {
                'voucher_type': "Payment Entry",
                'voucher_no': item_dict.voucher_no,
                'posting_date': item_dict.posting_date,
                'party_type': "Mode of Payment",
                'party': item_dict.party,
                'debit': item_dict.debit,
                'credit': 0,
                'payment_type': "Internal Transfer From",
                'balance': item_dict.debit,
            }
            result.append(data)

    return result
