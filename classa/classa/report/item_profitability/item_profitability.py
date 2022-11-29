# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns(filters)
	data = get_data(filters,columns)
	return columns, data

def get_columns(filters):
	if not filters.get("totals"):
		return [
			{
				"label": _("Invoice"),
				"fieldname": "name",
				"fieldtype": "Link",
				"options": "Sales Invoice",
				"width": 100
			},
			{
				"label": _("Date"),
				"fieldname": "date",
				"fieldtype": "Date",
				"width": 100
			},
			{
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 130
			},
			{
				"label": _("Address"),
				"fieldname": "customer_address",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Sales Person"),
				"fieldname": "sales_person",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Item"),
				"fieldname": "item_code",
				"fieldtype": "Link",
				"options": "Item",
				"width": 130
			},
			{
				"label": _("Item Name"),
				"fieldname": "item_name",
				"fieldtype": "Data",
				"width": 130
			},
			{
				"label": _("Unit"),
				"fieldname": "unit",
				"fieldtype": "Data",
				"width": 70
			},
			{
				"label": _("Box"),
				"fieldname": "box",
				"fieldtype": "Data",
				"width": 70
			},
			{
				"label": _("Carton"),
				"fieldname": "carton",
				"fieldtype": "Data",
				"width": 70
			},
			{
				"label": _("PLR"),
				"fieldname": "price_list_rate",
				"fieldtype": "Currency",
				"width": 70
			},
			{
				"label": _("Discount"),
				"fieldname": "discount_percentage",
				"fieldtype": "Currency",
				"width": 70
			},
			{
				"label": _("Tax"),
				"fieldname": "item_tax_template",
				"fieldtype": "Currency",
				"width": 70
			},
			{
				"label": _("Rate"),
				"fieldname": "rate",
				"fieldtype": "Currency",
				"width": 70
			},
			{
				"label": _("Selling Value"),
				"fieldname": "net_amount",
				"fieldtype": "Currency",
				"width": 70
			},
			{
				"label": _("Cost"),
				"fieldname": "cost",
				"fieldtype": "Currency",
				"width": 80
			},
			{
				"label": _("Profit"),
				"fieldname": "profit",
				"fieldtype": "Currency",
				"width": 80
			},
			{
				"label": _("Cost %"),
				"fieldname": "cost_percent",
				"fieldtype": "Float",
				"width": 80
			},
			{
				"label": _("Profit %"),
				"fieldname": "profit_percent",
				"fieldtype": "Float",
				"width": 80
			}
		]
	if filters.get("totals"):
		return [			
			{
				"label": _("Customer"),
				"fieldname": "customer",
				"fieldtype": "Link",
				"options": "Customer",
				"width": 130
			},
			{
				"label": _("Address"),
				"fieldname": "customer_address",
				"fieldtype": "Data",
				"width": 100
			},
			{
				"label": _("Unit"),
				"fieldname": "unit",
				"fieldtype": "Data",
				"width": 70
			},
			{
				"label": _("Box"),
				"fieldname": "box",
				"fieldtype": "Data",
				"width": 70
			},
			{
				"label": _("Carton"),
				"fieldname": "carton",
				"fieldtype": "Data",
				"width": 70
			},
			{
				"label": _("Selling Value"),
				"fieldname": "net_amount",
				"fieldtype": "Currency",
				"width": 120
			},
			{
				"label": _("Cost"),
				"fieldname": "cost",
				"fieldtype": "Currency",
				"width": 80
			},
			{
				"label": _("Profit"),
				"fieldname": "profit",
				"fieldtype": "Currency",
				"width": 80
			},
			{
				"label": _("Cost %"),
				"fieldname": "cost_percent",
				"fieldtype": "Float",
				"width": 80
			},
			{
				"label": _("Profit %"),
				"fieldname": "profit_percent",
				"fieldtype": "Float",
				"width": 80
			}
		]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("from_date"):
		conditions += " and a.posting_date between %(from_date)s and %(to_date)s"
	if filters.get("item_code"):
		conditions += " and b.item_code=%(item_code)s"
	if filters.get("customer"):
		conditions += " and a.customer=%(customer)s"
	if filters.get("item_group"):
		conditions += " and b.item_group=%(item_group)s"
	if filters.get("customer_group"):
		conditions += " and a.customer_group=%(customer_group)s"
	if filters.get("sales_person"):
		conditions += " and a.sales_person=%(sales_person)s"
	if not filters.get("totals"):
		item_results = frappe.db.sql("""Select
											a.name as name,
											a.customer as customer,
											a.posting_date as date,
											a.customer_address as customer_address,
											a.sales_person as sales_person,
											b.item_code as item_code,
											b.item_name as item_name,
											b.net_amount as net_amount,
											b.rate as rate,
											b.price_list_rate as price_list_rate,
											b.discount_percentage as discount_percentage,
											b.item_tax_template as item_tax_template,
											b.uom as uom,
											b.stock_qty as unit,
											(select conversion_factor from `tabUOM Conversion Detail` where uom = 'علبه' and parent = b.item_code) as box,
											(select conversion_factor from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = b.item_code) as carton,
											(select max(valuation_rate) from tabBin where item_code = b.item_code order by valuation_rate limit 1 ) as value
										from 
											`tabSales Invoice` a join `tabSales Invoice Item` b on a.name = b.parent
											where a.docstatus =1
											
											{conditions}
											
									""".format(conditions=conditions), filters, as_dict=1)


		result = []
		if item_results:
			for item_dict in item_results:
				data = {
					'name': item_dict.name,
					'date': item_dict.date,
					'sales_person': item_dict.sales_person,
					'customer': item_dict.customer,
					'customer_address': item_dict.customer_address,
					'item_code': item_dict.item_code,
					'item_name': item_dict.item_name,
					'uom': item_dict.uom,
					'discount_percentage': item_dict.discount_percentage,
					'unit': item_dict.unit,
					'box': round((item_dict.unit/ item_dict.box),2) if item_dict.box else 0,
					'carton':round((item_dict.unit/ item_dict.carton),2) if item_dict.carton else 0,
					'price_list_rate': item_dict.price_list_rate,
					'item_tax_template': item_dict.item_tax_template,
					'rate': item_dict.rate,
					'net_amount': item_dict.net_amount,
					'cost': round((item_dict.unit* item_dict.value),2),
					'profit': round((item_dict.net_amount - (item_dict.unit* item_dict.value)),2),
					'cost_percent':  round((((item_dict.unit* item_dict.value)/ item_dict.net_amount)*100),2) if item_dict.unit and item_dict.value and item_dict.net_amount else 0,
					'profit_percent': round((((item_dict.net_amount - (item_dict.unit* item_dict.value))/item_dict.net_amount)*100),2) if item_dict.net_amount and item_dict.unit and item_dict.value else 0,
				}
				result.append(data)

		return result
	if filters.get("totals"):
		if not filters.get("item_code"):
			frappe.throw("Please Select Item")
		else:
			
			item_results = frappe.db.sql("""Select distinct
												a.customer as customer,
												a.customer_address as customer_address
											from
												`tabSales Invoice` a join `tabSales Invoice Item` b on a.name = b.parent
											where
												a.docstatus =1
												
												{conditions}
												
										""".format(conditions=conditions), filters, as_dict=1)


			result = []
			if item_results:
				for item_dict in item_results:
					data = {
						'customer': item_dict.customer,
						'customer_address': item_dict.customer_address,
						'item_code': item_dict.item_code,
						'item_name': item_dict.item_name,
						'uom': item_dict.uom,
						'unit': item_dict.unit,
						
						#'net_amount': item_dict.net_amount
						#'cost': round((item_dict.unit* item_dict.value),2),
						#'profit': round((item_dict.net_amount - (item_dict.unit* item_dict.value)),2),
						#'cost_percent':  round((((item_dict.unit* item_dict.value)/ item_dict.net_amount)*100),2) if item_dict.unit and item_dict.value and item_dict.net_amount else 0,
						#'profit_percent': round((((item_dict.net_amount - (item_dict.unit* item_dict.value))/item_dict.net_amount)*100),2) if item_dict.net_amount and item_dict.unit and item_dict.value else 0,
					}
					details = frappe.db.sql(""" select 
												sum(b.stock_qty) as qty,
												(select conversion_factor from `tabUOM Conversion Detail` where uom = 'علبه' and parent ='{tt}') as box,
												(select conversion_factor from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = '{tt}') as carton,
												(select ROUND(avg(valuation_rate),2) from tabBin where item_code = '{tt}') as value
												from
												`tabSales Invoice` a join `tabSales Invoice Item` b on a.name = b.parent
											where
												a.docstatus =1 
												and a.customer = '{customer}'
												{conditions}
					""".format(conditions=conditions,customer=item_dict.customer,tt=filters.get('item_code')), filters, as_dict=1)
					result.append(data)
					for x in details:
						data['unit'] = x.qty
						data['box'] = round((x.qty/ x.box),2) if x.box else 0,
						data['carton']=round((x.qty/ x.carton),2) if x.carton else 0,

			return result