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
            "label": _("Item"),
            "fieldname": "item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 60
        },
        {
            "label": _("Barcode"),
            "fieldname": "barcode",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 270
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Data",
            "width": 120
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
            "label": _("معامل تحويل العلبة"),
            "fieldname": "box_conversion",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("كرتونة"),
            "fieldname": "carton",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("معامل تحويل الكرتونة"),
            "fieldname": "carton_conversion",
            "fieldtype": "Float",
            "width": 150
        },
        {
            "label": _("Reserved Qty"),
            "fieldname": "reserved_qty",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Warehouse"),
            "fieldname": "warehouse",
            "fieldtype": "Data",
            "width": 180
        },
        {
            "label": _("Type"),
            "fieldname": "type",
            "fieldtype": "Data",
            "width": 120
        },
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""

    if filters.get("warehouse"):
        conditions += " and `tabBin`.warehouse=%(warehouse)s"

    item_results = frappe.db.sql("""
        select
            tabBin.item_code as item,
            (select barcode from `tabItem Barcode` where parent = tabBin.item_code) as barcode,
            tabItem.item_name as item_name,
            tabItem.item_group as item_group,
            ifnull(tabBin.actual_qty,0) as piece,
            ifnull((tabBin.actual_qty /(select conversion_factor from `tabUOM Conversion Detail` where uom = 'علبه' and parent = tabBin.item_code)),0) as box,
            ifnull((select conversion_factor from `tabUOM Conversion Detail` where uom = 'علبه' and parent = tabBin.item_code),0) as box_conversion,
            ifnull((tabBin.actual_qty /(select conversion_factor from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = tabBin.item_code)),0) as carton,
            ifnull((select conversion_factor from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = tabBin.item_code),0) as carton_conversion,
            ifnull(tabBin.reserved_qty,0) as reserved_qty,
            tabBin.warehouse as warehouse,
            (select warehouse_type from tabWarehouse where tabWarehouse.name = tabBin.warehouse ) as type
        from
            tabBin
            inner join tabItem on tabBin.item_code = tabItem.item_code
        where
            tabItem.has_variants = 0
            and tabBin.actual_qty !=0
            {conditions}
        """.format(conditions=conditions), filters, as_dict=1)



    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'item': item_dict.item,
                'barcode': item_dict.barcode,
                'item_name': item_dict.item_name,
                'item_group': item_dict.item_group,
                'piece': item_dict.piece,
                'box': item_dict.box,
                'box_conversion': item_dict.box_conversion,
                'carton': item_dict.carton,
                'carton_conversion': item_dict.carton_conversion,
                'reserved_qty': item_dict.reserved_qty,
                'warehouse': item_dict.warehouse,
                'type': item_dict.type,
            }
            result.append(data)

    return result



