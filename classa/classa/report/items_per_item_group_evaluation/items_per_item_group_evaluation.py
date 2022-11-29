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
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 70
        },
        {
            "label": _("اسم الصنف"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 300
        },
		{
			"label": _("متوسط سعر التكلفة"),
			"fieldname": "avg_valuation_rate",
			"fieldtype": "Currency",
			"width": 135
		},
		{
			"label": _("سعر قائمة الأسعار"),
			"fieldname": "price_list_rate",
			"fieldtype": "Currency",
			"width": 130
		},
        {
            "label": _("قيمة الربحية"),
            "fieldname": "profit_rate",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("نسبة الربحية"),
            "fieldname": "profit_percent",
            "fieldtype": "Percent",
            "width": 130
        }
    ]

def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    item_group = filters.get("item_group")
    price_list = filters.get("price_list")

    result = []
    item_results = frappe.db.sql("""
            SELECT
                `tabItem`.item_code as item_code,
                `tabItem`.item_name as item_name,
                
                IFNULL((select avg(valuation_rate) from `tabBin` join `tabWarehouse` on `tabBin`.warehouse = `tabWarehouse`.name
                where `tabWarehouse`.warehouse_type = "مخزون سلعي" and `tabBin`.item_code = `tabItem`.item_code), 0) as avg_valuation_rate,
                
                IFNULL((select price_list_rate from `tabItem Price` 
                where price_list = '{price_list}' and item_code = `tabItem`.item_code), 0) as price_list_rate

            FROM
                `tabItem`
            WHERE
                `tabItem`.disabled = 0
                and `tabItem`.is_sales_item = 1
                and `tabItem`.item_group = '{item_group}'
            ORDER BY `tabItem`.item_code
            """.format(item_group=item_group, price_list=price_list), filters, as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
                'avg_valuation_rate': item_dict.avg_valuation_rate,
                'price_list_rate': item_dict.price_list_rate,
                'profit_rate': item_dict.price_list_rate - item_dict.avg_valuation_rate,
                'profit_percent': 100 * (item_dict.price_list_rate - item_dict.avg_valuation_rate)/item_dict.price_list_rate if item_dict.price_list_rate else 0,
            }
            result.append(data)
    return result
