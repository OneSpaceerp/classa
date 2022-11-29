# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import flt
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
	filters = frappe._dict(filters or {})
	if filters.from_date > filters.to_date:
		frappe.throw(_("From Date cannot be greater than To Date"))

	columns = get_columns(filters)
	data = get_data(filters)

	chart_data = get_chart_data(data)

	return columns, data, None, chart_data

def get_columns(filters):
	return [
		{
			"label": _("Item Code"),
			"fieldtype": "Link",
			"fieldname": "item_code",
			"options": "Item",
			"width": 120
		},
		{
			"label": _("Customer"),
			"fieldtype": "Link",
			"fieldname": "customer",
			"options": "Customer",
			"width": 100
		},
		{
			"label": _("Customer Group"),
			"fieldtype": "Link",
			"fieldname": "customer_group",
			"options": "Customer Group",
			"width": 120
		},
		{
			"label": _("Territory"),
			"fieldtype": "Link",
			"fieldname": "territory",
			"options": "Territory",
			"width": 100
		},
		
		{
			"label": _("UOM"),
			"fieldtype": "Data",
			"fieldname": "uom",
			"width": 50
		},
		{
			"label": _("قطعه"),
			"fieldtype": "Float",
			"fieldname": "quantity",
			"width": 70
		},
		{
			"label": _("علبة"),
			"fieldtype": "Float",
			"fieldname": "quantity1",
			"width": 70
		},
		{
			"label": _("كرتوة"),
			"fieldtype": "Float",
			"fieldname": "quantity2",
			"width": 70
		},
		{
			"label": _("Rate"),
			"fieldname": "rate",
			"options": "Currency",
			"width": 120
		},
		{
			"label": _("Amount"),
			"fieldname": "amount",
			"options": "Currency",
			"width": 120
		},
		{
			"label": _("Value"),
			"fieldname": "value",
			"options": "Float",
			"width": 120
		},
		{
			"label": _("Total Value"),
			"fieldname": "total_value",
			"options": "Float",
			"width": 120
		},
		{
			"label": _("Net Profit"),
			"fieldname": "net_profit",
			"options": "Float",
			"width": 120
		},
		{
			"label": _("Sales Invoice"),
			"fieldtype": "Link",
			"fieldname": "sales_invoice",
			"options": "Sales Invoice",
			"width": 100
		},
		{
			"label": _("Transaction Date"),
			"fieldtype": "Date",
			"fieldname": "transaction_date",
			"width": 90
		},
		{
			"label": _("Item Name"),
			"fieldtype": "Data",
			"fieldname": "item_name",
			"width": 140
		},
		{
			"label": _("Item Group"),
			"fieldtype": "Link",
			"fieldname": "item_group",
			"options": "Item Group",
			"width": 120
		},
		
	]

def get_data(filters):

	data = []

	company_list = get_descendants_of("Company", filters.get("company"))
	company_list.append(filters.get("company"))

	customer_details = get_customer_details()
	item_details = get_item_details()
	sales_order_records = get_sales_order_details(company_list, filters)

	for record in sales_order_records:
		customer_record = customer_details.get(record.customer)
		item_record = item_details.get(record.item_code)
		row = {
			"item_code": record.item_code,
			"item_name": item_record.item_name,
			"item_group": item_record.item_group,
			"uom": record.uom,
			"description": record.description,
			"quantity": (record.stock_qty ),
			"quantity1": (record.stock_qty/record.box ) if record.box else 0,
			"quantity2": (record.stock_qty/record.carton )if record.carton else 0 ,
			"rate": round(record.base_rate, 2),
			"amount": record.base_amount,
			"value": round(record.value, 2),
			"total_value": round((record.stock_qty *record.value), 2),
			"net_profit": round(record.base_amount-(record.stock_qty *record.value), 2),
			"sales_invoice": record.name,
			"transaction_date": record.posting_date,
			"customer": record.customer,
			"customer_name": customer_record.customer_name,
			"customer_group": customer_record.customer_group,
			"territory": record.territory,
			"project": record.project,
			"delivered_quantity": flt(record.delivered_qty),
			"billed_amount": flt(record.billed_amt),
			"company": record.company
		}
		data.append(row)

	return data

def get_conditions(filters):
	conditions = ''
	if filters.get('item_group'):
		conditions += "AND so_item.item_group = %s" %frappe.db.escape(filters.item_group)

	if filters.get('from_date'):
		conditions += "AND so.posting_date >= '%s'" %filters.from_date

	if filters.get('to_date'):
		conditions += "AND so.posting_date <= '%s'" %filters.to_date

	if filters.get("item_code"):
		conditions += "AND so_item.item_code = %s" %frappe.db.escape(filters.item_code)

	if filters.get("customer"):
		conditions += "AND so.customer = %s" %frappe.db.escape(filters.customer)

	return conditions

def get_customer_details():
	details = frappe.get_all("Customer",
		fields=["name", "customer_name", "customer_group"])
	customer_details = {}
	for d in details:
		customer_details.setdefault(d.name, frappe._dict({
			"customer_name": d.customer_name,
			"customer_group": d.customer_group
		}))
	return customer_details

def get_item_details():
	details = frappe.db.get_all("Item",
		fields=["item_code", "item_name", "item_group"])
	item_details = {}
	for d in details:
		item_details.setdefault(d.item_code, frappe._dict({
			"item_name": d.item_name,
			"item_group": d.item_group
		}))
	return item_details

def get_sales_order_details(company_list, filters):
	conditions = get_conditions(filters)

	return frappe.db.sql("""
		SELECT
			so_item.item_code, so_item.description, so_item.stock_qty,
			so_item.uom, so_item.conversion_factor,
			 so_item.base_rate, so_item.base_amount,
			so.name, so.posting_date, so.customer,so.territory,
			so.project, so_item.delivered_qty,
			so.company,
			(select ROUND(max(valuation_rate),2) from tabBin where item_code = so_item.item_code) as value,
			(select conversion_factor from `tabUOM Conversion Detail` where uom = 'علبه' and parent = so_item.item_code) as box,
			(select conversion_factor from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = so_item.item_code) as carton
		FROM
			`tabSales Invoice` so, `tabSales Invoice Item` so_item
		WHERE
			so.name = so_item.parent
			AND so.company in ({0})
			AND so.docstatus = 1 {1}
			order by so.posting_date
	""".format(','.join(["%s"] * len(company_list)), conditions), tuple(company_list), as_dict=1)

def get_chart_data(data):
	item_wise_sales_map = {}
	labels, datapoints = [], []

	for row in data:
		item_key = row.get("item_code")

		if not item_key in item_wise_sales_map:
			item_wise_sales_map[item_key] = 0

		item_wise_sales_map[item_key] = flt(item_wise_sales_map[item_key]) + flt(row.get("amount"))

	item_wise_sales_map = { item: value for item, value in (sorted(item_wise_sales_map.items(), key = lambda i: i[1], reverse=True))}

	for key in item_wise_sales_map:
		labels.append(key)
		datapoints.append(item_wise_sales_map[key])

	return {
		"data" : {
			"labels" : labels[:30], # show max of 30 items in chart
			"datasets" : [
				{
					"name" : _(" Total Sales Amount"),
					"values" : datapoints[:30]
				}
			]
		},
		"type" : "bar"
	}
