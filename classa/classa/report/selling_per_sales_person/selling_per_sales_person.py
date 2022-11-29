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
            "label": _("الكود"),
            "fieldname": "code",
            "fieldtype": "Integer",
            "width": 70
        },
        {
            "label": _("العميل"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 220
        },
        {
            "label": _("تسويات مدينة"),
            "fieldname": "tdebit",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": _("تسويات دائنة"),
            "fieldname": "tcredit",
            "fieldtype": "Currency",
            "width": 110
        },
        {
            "label": _("مدين"),
            "fieldname": "debit",
            "fieldtype": "Currency",
            "width": 100
        },

        {
            "label": _("دائن"),
            "fieldname": "credit",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("الرصيد"),
            "fieldname": "balance",
            "fieldtype": "Currency",
            "width": 100
        },
        {
            "label": _("اخر بيع"),
            "fieldname": "last_invoice_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("اخر تحصيل"),
            "fieldname": "last_payment_date",
            "fieldtype": "Date",
            "width": 110
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    sales_person = filters.get("sales_person")
    to_date = filters.get("to_date")
    from_date = filters.get("from_date")

    result = []

    customer_list = frappe.db.sql(
        """select
            (`tabCustomer`.name) as customer
            from `tabCustomer`
            where `tabCustomer`.sales_person = '{sales_person}'
            and `tabCustomer`.disabled = 0
        """.format(sales_person=sales_person), as_dict=1)

    for x in customer_list:
        data = {
            'customer': x.customer
        }
        item_results = frappe.db.sql("""
                    SELECT 
                        `tabCustomer`.code as code,

                        ifnull((select sum(debit) from `tabGL Entry` where party='{customer_list}' 
                        and is_cancelled = 0
                        and posting_date < '{from_date}'),0) as tdebit,

                        ifnull((select sum(credit) from `tabGL Entry` where party='{customer_list}' 
                        and is_cancelled = 0
                        and posting_date < '{from_date}'),0) as tcredit,

                        IFNULL((select sum(debit) from `tabGL Entry` where party='{customer_list}' 
                        and is_cancelled = 0
                        and posting_date between '{from_date}' and '{to_date}'),0) as debit,

                        IFNULL((select sum(credit) from `tabGL Entry` where party='{customer_list}' 
                        and is_cancelled = 0
                        and posting_date between '{from_date}' and '{to_date}'),0) as credit,

                        IFNULL((select `tabSales Invoice`.posting_date
                        from `tabSales Invoice`
                        where `tabSales Invoice`.docstatus = 1
                        and `tabSales Invoice`.customer = '{customer_list}'
                        and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
                        order by `tabSales Invoice`.posting_date desc LIMIT 1) ,"00-00-0000") as last_invoice_date,

                        IFNULL((select `tabPayment Entry`.posting_date
                        from `tabPayment Entry`
                        where `tabPayment Entry`.docstatus = 1
                        and `tabPayment Entry`.party = '{customer_list}'
                        and `tabPayment Entry`.posting_date between '{from_date}' and '{to_date}'
                        order by `tabPayment Entry`.posting_date desc LIMIT 1) ,"00-00-0000") as last_payment_date

                    FROM
                        `tabCustomer`
                    WHERE
                        `tabCustomer`.disabled = 0
                        and `tabCustomer`.name = '{customer_list}'


                    """.format(customer_list=x.customer, sales_person=sales_person, from_date=from_date,
                               to_date=to_date), filters, as_dict=1)

        for z in item_results:
            data['code'] = z.code
            data['tdebit'] = z.tdebit
            data['tcredit'] = z.tcredit
            data['debit'] = z.debit
            data['credit'] = z.credit
            data['balance'] = (z.tdebit - z.tcredit + z.debit - z.credit)
            data['last_invoice_date'] = z.last_invoice_date
            data['last_payment_date'] = z.last_payment_date

        result.append(data)
    return result

