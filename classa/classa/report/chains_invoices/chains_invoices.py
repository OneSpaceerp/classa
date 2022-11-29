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
            "label": _("Sales Order"),
            "fieldname": "sales_order",
            "fieldtype": "Link",
            "options": "Sales Order",
            "width": 150
        },
        {
            "label": _("Date"),
            "fieldname": "transaction_date",
            "fieldtype": "Date",
            "width": 110
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Data",
            "width": 150
        },
		{
			"label": _("Customer Address"),
			"fieldname": "customer_address",
			"fieldtype": "data",
			"width": 150
		},
		{
            "label": _("Stock Entry"),
            "fieldname": "stock_entry",
            "fieldtype": "Link",
            "options": "Stock Entry",
            "width": 150
        },
		{
			"label": _("Stock Entry Status"),
			"fieldname": "st_status",
			"fieldtype": "data",
			"width": 150
		},
		{
			"label": _("From Warehouse"),
			"fieldname": "from_warehouse",
			"fieldtype": "data",
			"width": 150
		},
		{
			"label": _("Vehicle"),
			"fieldname": "to_warehouse",
			"fieldtype": "data",
			"width": 150
		},
        {
            "label": _("Sales Invoice"),
            "fieldname": "sales_invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 150
        },
		{
            "label": _("Sales Invoice Status"),
            "fieldname": "sales_invoice_status",
            "fieldtype": "data",
			"width": 150
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    conditions1 = ""

    if filters.get("customer"):
        conditions += "and `tabSales Order`.customer = %(customer)s"
    if filters.get("customer_group"):
        conditions += " and `tabSales Order`.customer_group = %(customer_group)s"
    if filters.get("warehouse"):
        conditions += " and `tabStock Entry`.from_warehouse = %(warehouse)s"
    if filters.get("branch"):
        conditions += "and `tabSales Order`.branch = %(branch)s"
    if filters.get("st_status") == "Draft":
        conditions += "and `tabStock Entry`.docstatus = 0"
    if filters.get("st_status") == "Submitted":
        conditions += "and `tabStock Entry`.docstatus = 1"
    if filters.get("si_status") == "Draft":
        conditions1 += "and `tabSales Invoice`.docstatus = 0"
    if filters.get("si_status") == "Submitted":
        conditions1 += "and `tabSales Invoice`.docstatus = 1"
    item_results = frappe.db.sql("""
        SELECT 
            `tabStock Entry`.name as stock_entry,
            `tabStock Entry`.from_warehouse as from_warehouse,
            `tabStock Entry`.to_warehouse as to_warehouse,
            `tabStock Entry`.docstatus as st_status,
            (select `tabSales Order`.name from `tabSales Order` where name = `tabStock Entry`.sales_order and `tabSales Order`.docstatus = 1) as sales_order,
            (select `tabSales Order`.transaction_date from `tabSales Order` where name = `tabStock Entry`.sales_order and `tabSales Order`.docstatus = 1) as transaction_date,
            (select `tabSales Order`.customer from `tabSales Order` where name = `tabStock Entry`.sales_order and `tabSales Order`.docstatus = 1) as customer,
            (select `tabSales Order`.customer_address from `tabSales Order` where name = `tabStock Entry`.sales_order and `tabSales Order`.docstatus = 1) as customer_address
        FROM
            `tabStock Entry` 
        WHERE
            `tabStock Entry`.docstatus != 2
            and `tabStock Entry`.sales_order is not null
            and  `tabStock Entry`.posting_date > "2022-03-22"
            {conditions}
    
        """.format(conditions=conditions), filters, as_dict=1)


    result = []
    if item_results:
        for item_dict in item_results:
            if item_dict.st_status == 1:
                stt = "Submitted"
            elif item_dict.st_status == 2:
                stt = "Cancelled"
            else:
                stt = "Draft"
            data = {
                'sales_order': item_dict.sales_order,
                'transaction_date': item_dict.transaction_date,
                'customer': item_dict.customer,
                'customer_address': item_dict.customer_address,
                'stock_entry': item_dict.stock_entry,
                'st_status': stt,
                'from_warehouse': item_dict.from_warehouse,
                'to_warehouse': item_dict.to_warehouse
            }
            item_result2 = frappe.db.sql(""" select 
                                                `tabSales Invoice`.name  as sales_invoice,
                                                `tabSales Invoice`.status as sales_invoice_status
                                            from `tabSales Invoice`
                                            where
                                                 stock_entry = '{ste}'
                                                  and `tabSales Invoice`.docstatus != 2 
                                                  {conditions1}""".format(conditions1=conditions1,ste=item_dict.stock_entry),as_dict=1)
            for v in item_result2:
                data["sales_invoice"] = v.sales_invoice
                data["sales_invoice_status"] = v.sales_invoice_status


            result.append(data)

    return result
    
