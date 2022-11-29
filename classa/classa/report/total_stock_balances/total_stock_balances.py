

# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns=get_columns()
	data=get_data(filters,columns)
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
			"label": _("قطعة"),
			"fieldname": "piece",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("علبة"),
			"fieldname": "box",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("كرتونة"),
			"fieldname": "carton",
			"fieldtype": "Float",
			"width": 100
		},
		{
			"label": _("Reserved Qty"),
			"fieldname": "reserved_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label": _("Ordered Qty"),
			"fieldname": "ordered_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label": _("Requested Qty"),
			"fieldname": "indented_qty",
			"fieldtype": "Float",
			"width": 120
		},
		{
			"label": _("Projected Qty"),
			"fieldname": "projected_qty",
			"fieldtype": "Float",
			"width": 120
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	#if filters.get("warehouse_type"):
	#	conditions += " and a.warehouse_type>=%(warehouse_type)s"

	item_results = frappe.db.sql("""select  
										 tabItem.item_code as item_code,
										 (select barcode from `tabItem Barcode` where parent = tabItem.item_code) as barcode,
										 tabItem.item_name as item_name,
										 tabItem.item_group as item_group,
										 (select IFNULL(sum(tabBin.actual_qty),0) from `tabBin` where tabBin.item_code = tabItem.item_code) as piece,
										 IFNULL(((select sum(tabBin.actual_qty) from `tabBin` where tabBin.item_code = tabItem.item_code)/(select conversion_factor from `tabUOM Conversion Detail` where uom = 'علبه' and parent = tabItem.item_code)),0) as box,
										 IFNULL(((select sum(tabBin.actual_qty) from `tabBin` where tabBin.item_code = tabItem.item_code)/(select conversion_factor from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = tabItem.item_code)),0) as carton,
										 (select IFNULL(sum(tabBin.reserved_qty),0) from `tabBin` where tabBin.item_code = tabItem.item_code) as reserved_qty,
										 (select IFNULL(sum(tabBin.ordered_qty),0) from `tabBin` where tabBin.item_code = tabItem.item_code) as ordered_qty,
										 (select IFNULL(sum(tabBin.indented_qty),0) from `tabBin` where tabBin.item_code = tabItem.item_code) as indented_qty,
										 (select IFNULL(sum(tabBin.projected_qty),0) from `tabBin` where tabBin.item_code = tabItem.item_code) as projected_qty
										from
										tabItem
										where
										tabItem.has_variants = 0
										{conditions}
								""".format(conditions=conditions), filters, as_dict=1)


	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'item_code': item_dict.item_code,
				'barcode': item_dict.barcode,
				'item_name': item_dict.item_name,
				'item_group': item_dict.item_group,
				'piece': item_dict.piece,
				'box': item_dict.box,
				'carton': item_dict.carton,
				'reserved_qty': item_dict.reserved_qty,
				'ordered_qty': item_dict.ordered_qty,
				'indented_qty': item_dict.indented_qty,
				'projected_qty': item_dict.projected_qty
			}
			result.append(data)

	return result

def get_price_map(price_list_names, buying=0, selling=0):
	price_map = {}

	if not price_list_names:
		return price_map

	rate_key = "Buying Rate" if buying else "Selling Rate"
	price_list_key = "Buying Price List" if buying else "Selling Price List"

	filters = {"name": ("in", price_list_names)}
	if buying:
		filters["buying"] = 1
	else:
		filters["selling"] = 1

	pricing_details = frappe.get_all("Item Price",
		fields = ["name", "price_list", "price_list_rate"], filters=filters)

	for d in pricing_details:
		name = d["name"]
		price_map[name] = {
			price_list_key :d["price_list"],
			rate_key :d["price_list_rate"]
		}

	return price_map


