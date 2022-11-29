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
            "fieldname": "customer_code",
            "fieldtype": "Data",
            "width": 70
        },
        {
            "label": _("العميل"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 200
        },
        {
            "label": _("مجموعة العميل"),
            "fieldname": "customer_group",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("المندوب"),
            "fieldname": "sales_person",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("المنطقة"),
            "fieldname": "territory",
            "fieldtype": "Data",
            "width": 80
        },
        {
            "label": _("عدد الفواتير"),
            "fieldname": "no_of_invoices",
            "fieldtype": "Int",
            "width": 130
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    sales_person = filters.get("sales_person")
    price_list = filters.get("price_list")

    result = []
    customer_list = frappe.db.sql(
        """select
            (`tabSales Invoice`.customer) as customer
            from `tabSales Invoice`
            where `tabSales Invoice`sales_person = '{sales_person}'
            and `tabSales Invoice`.docstatus = 1
        """.format(sales_person=sales_person), as_dict=1)
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
                'profit_percent': 100 * (
                            item_dict.price_list_rate - item_dict.avg_valuation_rate) / item_dict.price_list_rate if item_dict.price_list_rate else 0,
            }
            result.append(data)
    return result
