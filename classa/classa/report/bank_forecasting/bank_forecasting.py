from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
import datetime
from frappe.utils import flt
from erpnext.accounts.utils import get_balance_on
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)

def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("الحساب البنكي"),
            "fieldname": "account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 250
        },
        {
            "label": _("أول المدة"),
            "fieldname": "opening",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("مدين"),
            "fieldname": "incoming",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("تحت التحصيل"),
            "fieldname": "receivable",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("دائن"),
            "fieldname": "outgoing",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("برسم الدفع"),
            "fieldname": "payable",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("الإجمالي"),
            "fieldname": "total",
            "fieldtype": "Currency",
            "width": 130
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    to_date = filters.get("to_date")
    from_date = filters.get("from_date")
    from_dateo = getdate(from_date) - datetime.timedelta(days=1)

    result = []
    item_results = frappe.db.sql("""
            SELECT
                `tabAccount`.name as account
            FROM
                `tabAccount`
            WHERE
                `tabAccount`.disabled = 0
                and `tabAccount`.is_group = 0
                and `tabAccount`.account_type = 'Bank'
                and `tabAccount`.name not in ("1331 - اوراق قبض مستلمة - CA", "1332 - اوراق قبض برسم التحصيل - CA", "1334 - اوراق قبض مندوبي البيع - CA", "1910 - حساب افتتاحي مؤقت - CA", "2140 - اوراق الدفع - CA")
            """, filters, as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'account': item_dict.account,
            }
            opening = get_balance_on(account=item_dict.account, date=getdate(from_dateo), party_type=None, party=None, company=None,
                             in_account_currency=True, cost_center=None, ignore_account_permission=False)
            data['opening'] = opening

            accounto = item_dict.account
            incoming = frappe.db.sql(""" select 
                                                ifnull(sum(`tabGL Entry`.debit), 0) as debit
                                           from 
                                                `tabGL Entry`
                                           where 
                                               `tabGL Entry`.is_cancelled = 0
                                               and `tabGL Entry`.account = '{accounto}'
                                               and `tabGL Entry`.posting_date between '{from_date}' and '{to_date}'
                                       """.format(accounto=accounto, from_date=from_date, to_date=to_date), as_dict=0)

            data['incoming'] = incoming[0][0]

            outgoing = frappe.db.sql(""" select 
                                                ifnull(sum(`tabGL Entry`.credit), 0) as credit
                                           from 
                                                `tabGL Entry`
                                           where 
                                               `tabGL Entry`.is_cancelled = 0
                                               and `tabGL Entry`.account = '{accounto}'
                                               and `tabGL Entry`.posting_date between '{from_date}' and '{to_date}'
                                       """.format(accounto=accounto, from_date=from_date, to_date=to_date), as_dict=0)

            data['outgoing'] = outgoing[0][0]

            receivable = frappe.db.sql(""" select 
                                                ifnull(sum(`tabPayment Entry`.paid_amount), 0) as paid_amount
                                           from 
                                                `tabPayment Entry`
                                           where
                                               `tabPayment Entry`.docstatus = 1
                                               and `tabPayment Entry`.payment_type = "Receive"
                                               and `tabPayment Entry`.mode_of_payment_type = "Cheque"
                                               and `tabPayment Entry`.cheque_status = "تحت التحصيل"
                                               and `tabPayment Entry`.account = '{accounto}'
                                               and `tabPayment Entry`.reference_date between '{from_date}' and '{to_date}'
                                       """.format(accounto=accounto, from_date=from_date, to_date=to_date),as_dict=0)

            data['receivable'] = receivable[0][0]

            payable = frappe.db.sql(""" select 
                                            ifnull(sum(`tabPayment Entry`.paid_amount), 0) as paid_amount
                                       from 
                                            `tabPayment Entry`
                                       where 
                                           `tabPayment Entry`.docstatus = 1
                                           and `tabPayment Entry`.payment_type = "Pay"
                                           and `tabPayment Entry`.mode_of_payment_type = "Cheque"
                                           and `tabPayment Entry`.cheque_status_pay = "حافظة شيكات برسم الدفع"
                                           and `tabPayment Entry`.account = '{accounto}'
                                           and `tabPayment Entry`.reference_date between '{from_date}' and '{to_date}'
                                   """.format(accounto=accounto, from_date=from_date, to_date=to_date), as_dict=0)

            data['payable'] = payable[0][0]

            data['total'] = opening + incoming[0][0] + receivable[0][0] - outgoing[0][0] - payable[0][0]

            result.append(data)
    return result

