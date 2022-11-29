# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import cint


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"fieldname": "branch",
			"fieldtype": "Link",
			"label": _("Branch"),
			"options": "Branch",
			"width": 80
		},
		{
			"fieldname": "item",
			"fieldtype": "Link",
			"options": "Item",
			"label": "Item",
			"width": 60
		},
		{
			"fieldname": "item_name",
			"fieldtype": "Data",
			"label": _("Item Name"),
			"width": 200
		},
		{
			"fieldname": "item_group",
			"fieldtype": "Link",
			"label": _("Item Group"),
			"options": "Item Group",
			"width": 140
		},
		{
			"fieldname": "customer",
			"fieldtype": "Link",
			"label": _("Customer"),
			"options": "Customer",
			"width": 150
		},
		{
			"fieldname": "days_since_last_order",
			"fieldtype": "Int",
			"label": _("Days Since Last Invoice"),
			"width": 180
		},
		{
			"fieldname": "last_invoice",
			"fieldtype": "Link",
			"label": _("Last Invoice"),
			"options": "Sales Invoice",
			"width": 100
		},
		{
			"fieldname": "last_order_date",
			"fieldtype": "Date",
			"label": _("Last Invoice Date"),
			"width": 140
		},
		{
			"fieldname": "qty",
			"fieldtype": "Float",
			"label": _("Quantity"),
			"width": 80
		},
		{
			"fieldname": "sales_person",
			"fieldtype": "Data",
			"label": _("Sales Person"),
			"width": 180
		},
	]

	return columns


def get_data(filters):
	data = []
	items = get_items(filters)
	branches = get_branches(filters)
	sales_invoice_data = get_sales_details(filters)

	for branch in branches:
		for item in items:
			row = {
				"branch": branch.name,
				"item_group": item.item_group,
				"item": item.item_code,
				"item_name": item.item_name
			}

			if sales_invoice_data.get((branch.name,item.item_code)):
				item_obj = sales_invoice_data[(branch.name,item.item_code)]
				if item_obj.days_since_last_order > cint(filters['days']):
					row.update({
						"branch": item_obj.branch,
						"customer": item_obj.customer,
						"last_invoice": item_obj.name,
						"sales_person": item_obj.sales_person,
						"last_order_date": item_obj.last_order_date,
						"qty": item_obj.qty,
						"days_since_last_order": item_obj.days_since_last_order
					})
				else:
					continue

			data.append(row)

	return data


def get_sales_details(filters):
	data = []
	item_details_map = {}

	date_field = "s.transaction_date" if filters["based_on"] == "Sales Order" else "s.posting_date"
	branch_field = "s.branch," if filters["based_on"] == "Sales Invoice" else ""

	sales_data = frappe.db.sql("""
		select {branch_field} s.name, s.customer, s.sales_person, si.item_group, si.item_code, si.qty, {date_field} as last_order_date,
		DATEDIFF(CURDATE(), {date_field}) as days_since_last_order
		from `tab{doctype}` s, `tab{doctype} Item` si
		where s.name = si.parent and s.docstatus = 1
		order by days_since_last_order """ #nosec
		.format(date_field=date_field, branch_field=branch_field, doctype=filters['based_on']), as_dict=1)

	for d in sales_data:
		item_details_map.setdefault((d.branch,d.item_code), d)

	return item_details_map

def get_branches(filters):

	filter_dict = {}
	if filters.get("branch"):
		filter_dict.update({'name': filters['branch']})

	branches = frappe.get_all("Branch", fields=["name"], filters=filter_dict)

	return branches

def get_items(filters):
	filters_dict = {
		"disabled": 0,
		"is_stock_item": 1
	}

	if filters.get("item_group"):
		filters_dict.update({
			"item_group": filters["item_group"]
		})

	if filters.get("item"):
		filters_dict.update({
			"name": filters["item"]
		})

	items = frappe.get_all("Item", fields=["name", "item_group", "item_name", "item_code"], filters=filters_dict, order_by="name")

	return items
