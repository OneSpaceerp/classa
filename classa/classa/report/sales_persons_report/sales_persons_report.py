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
			"label": _("مندوب المبيعات"),
			"fieldname": "sales_person",
			"fieldtype": "Link",
			"options": "Sales Person",
			"width": 220
		},
		{
			"label": _("المبيعات"),
			"fieldname": "total_sales_amount",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("المرتجعات"),
			"fieldname": "total_returns_amount",
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
			"width": 160
		},
		{
			"label": _("عدد الفواتير"),
			"fieldname": "no_sales_invoices",
			"fieldtype": "Integer",
			"width": 110
		},
		{
			"label": _("عدد العملاء"),
			"fieldname": "no_customers",
			"fieldtype": "Integer",
			"width": 110
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data


def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("sales_person"):
		conditions += " and `tabSales Person`.name=%(sales_person)s"

	to_date = filters.get("to_date")
	from_date = filters.get("from_date")

	result = []
	item_results = frappe.db.sql("""
			SELECT 
				`tabSales Person`.name as sales_person,
				`tabSales Person`.employee as code,
								
				IFNULL((select count(name) 
				from `tabSales Invoice`
				where `tabSales Invoice`.docstatus = 1
				and `tabSales Invoice`.is_return = 0
				and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
				and `tabSales Invoice`.sales_person = `tabSales Person`.name),0) as no_sales_invoices,
				
				IFNULL((select sum(paid_amount) 
				from `tabPayment Entry`
				where `tabPayment Entry`.docstatus = 1
				and `tabPayment Entry`.payment_type = "Receive"
				and `tabPayment Entry`.posting_date between '{from_date}' and '{to_date}'
				and `tabPayment Entry`.sales_person = `tabSales Person`.name),0) as payment_entries,
				
				IFNULL((select sum(grand_total) 
				from `tabSales Invoice`
				where `tabSales Invoice`.docstatus = 1
				and `tabSales Invoice`.is_return = 0
				and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
				and `tabSales Invoice`.sales_person = `tabSales Person`.name),0) as total_sales_amount,
				
				IFNULL((select sum(`tabSales Invoice Item`.discount_percentage * `tabSales Invoice Item`.price_list_rate / 100) 
				from `tabSales Invoice Item` join `tabSales Invoice` 
				on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
				where `tabSales Invoice`.docstatus = 1
				and `tabSales Invoice`.is_return = 0
				and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
				and `tabSales Invoice`.sales_person = `tabSales Person`.name),0) as discount_amount,
				
				
				IFNULL(-1*(select sum(grand_total) 
				from `tabSales Invoice`
				where `tabSales Invoice`.docstatus = 1
				and `tabSales Invoice`.is_return = 1
				and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
				and `tabSales Invoice`.sales_person = `tabSales Person`.name),0) as total_returns_amount

			FROM
				`tabSales Person`
			WHERE
				`tabSales Person`.is_group = 0
				and `tabSales Person`.enabled = 1
				{conditions}

			ORDER BY (select sum(grand_total) 
				from `tabSales Invoice`
				where `tabSales Invoice`.docstatus = 1
				and `tabSales Invoice`.is_return = 0
				and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
				and `tabSales Invoice`.sales_person = `tabSales Person`.name) desc
			""".format(conditions=conditions, from_date=from_date, to_date=to_date), filters, as_dict=1)

	if item_results:
		for item_dict in item_results:
			data = {
				'sales_person': item_dict.sales_person,
				'code': item_dict.code,
				'no_sales_invoices': item_dict.no_sales_invoices,
				'payment_entries': item_dict.payment_entries,
				'total_sales_amount': item_dict.total_sales_amount,
				'total_taxes_amount': item_dict.total_taxes_amount,
				'total_returns_amount': item_dict.total_returns_amount,
				'discount_amount': item_dict.discount_amount
			}

			customer_count = frappe.db.sql(
							"""select distinct
								(`tabSales Invoice`.customer) as customer
								from `tabSales Invoice`
								where `tabSales Invoice`.docstatus=1
								and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
								and `tabSales Invoice`.sales_person = '{sales_person}'
							""".format(sales_person=item_dict.sales_person, from_date=from_date, to_date=to_date), as_dict=1)
			num = 0
			for s in customer_count:
				num += 1
			data['no_customers'] = num

			result.append(data)
	return result

