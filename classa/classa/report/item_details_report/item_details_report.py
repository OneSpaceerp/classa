

# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters,columns)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Item"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 65
		},
		{
			"label": _("Barcode"),
			"fieldname": "barcode",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 300
		},
		{
			"label": _("Item Group"),
			"fieldname": "item_group",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Price List"),
			"fieldname": "price_list",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": _("Price List Rate"),
			"fieldname": "price_list_rate",
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
	if filters.get("price_list"):
		conditions += " and `tabItem Price`.price_list=%(price_list)s"
	if filters.get("item_code"):
		conditions += " and `tabItem Price`.item_code=%(item_code)s"

	item_results = frappe.db.sql("""Select
										`tabItem Price`.item_code as item_code,
										(Select barcode From `tabItem Barcode` Where parent = `tabItem Price`.item_code) as barcode,
										`tabItem Price`.item_name as item_name,
										(Select tabItem.item_group From tabItem Where `tabItem Price`.item_code = tabItem.item_code) as item_group,
										`tabItem Price`.price_list as price_list,
										`tabItem Price`.price_list_rate as price_list_rate
										From `tabItem Price`
										Where
										`tabItem Price`.selling = 1
										{conditions}
										Order By `tabItem Price`.item_code
								""".format(conditions=conditions), filters, as_dict=1)


	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'item_code': item_dict.item_code,
				'barcode': item_dict.barcode,
				'item_name': item_dict.item_name,
				'item_group': item_dict.item_group,
				'price_list': item_dict.price_list,
				'price_list_rate': item_dict.price_list_rate
			}
			result.append(data)

	return result




