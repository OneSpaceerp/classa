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
            "label": _("أول المدة بالكرتونة"),
            "fieldname": "opening_carton",
            "fieldtype": "Float",
            "width": 130
        },
        {
            "label": _("PO بالكرتونة"),
            "fieldname": "po_carton",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("PINV بالكرتونة"),
            "fieldname": "pinv_carton",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("PINV1 بالكرتونة"),
            "fieldname": "pinv_carton1",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("PINV1 بونص"),
            "fieldname": "pinv_carton2",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("المشتريات %"),
            "fieldname": "p_percent",
            "fieldtype": "Percent",
            "width": 100
        },
        {
            "label": _("متوسط سعر الشراء"),
            "fieldname": "avg_rate",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("إجمالي المشتريات"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 130
        },
        {
            "label": _("SO بالكرتونة"),
            "fieldname": "so_carton",
            "fieldtype": "Float",
            "width": 100
        },
        {
            "label": _("SINV بالكرتونة"),
            "fieldname": "sinv_carton",
            "fieldtype": "Float",
            "width": 110
        },
        {
            "label": _("المبيعات %"),
            "fieldname": "s_percent",
            "fieldtype": "Percent",
            "width": 100
        },
        {
            "label": _("اخر المدة بالكرتونة"),
            "fieldname": "closing_carton",
            "fieldtype": "Float",
            "width": 130
        }
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    to_date = filters.get("to_date")
    from_date = filters.get("from_date")
    item_group = filters.get("item_group")

    result = []
    item_results = frappe.db.sql("""
            SELECT
                `tabItem`.item_code as item_code,
                `tabItem`.item_name as item_name,
                `tabItem`.item_group as item_group,
                (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabItem`.item_code) as carton_cf
            FROM
                `tabItem`
            WHERE
                `tabItem`.disabled = 0
                and `tabItem`.is_sales_item = 1
                and `tabItem`.item_group = '{item_group}'
            ORDER BY `tabItem`.item_code
            """.format(item_group=item_group), filters, as_dict=1)

    if item_results:
        for item_dict in item_results:
            data = {
                'item_code': item_dict.item_code,
                'item_name': item_dict.item_name,
            }
            warehouses = frappe.db.sql("""select name as name from `tabWarehouse` where disabled = 0 and warehouse_type = 'مخزون سلعي' """, as_dict=1)
            opening_qty = 0
            itemo = item_dict.item_code
            for x in warehouses:

                warehouseo = x.name
                opening = frappe.db.sql("""
                                            select
                                                 ifnull(qty_after_transaction, 0) as qty_after_transaction
                                            from `tabStock Ledger Entry` join `tabItem` on `tabStock Ledger Entry`.item_code = '{itemo}'
                                            where
                                                `tabStock Ledger Entry`.item_code = '{itemo}'
                                                 and `tabStock Ledger Entry`.posting_date <= '{from_date}'
                                                 and `tabStock Ledger Entry`.warehouse = '{warehouseo}'
                                                 and `tabStock Ledger Entry`.is_cancelled = 0
                                            ORDER BY `tabStock Ledger Entry`.posting_date DESC, `tabStock Ledger Entry`.posting_time DESC, `tabStock Ledger Entry`.creation DESC LIMIT 1
                                        """.format(itemo=itemo, from_date=from_date, warehouseo=warehouseo), as_dict=1)
                for y in opening:
                    opening_qty += y.qty_after_transaction
            data['opening_carton'] = opening_qty / item_dict.carton_cf if item_dict.carton_cf else opening_qty

            po = frappe.db.sql(""" select 
                                        ifnull(sum(`tabPurchase Order Item`.stock_qty), 0) as stock_qty
                                   from 
                                        `tabPurchase Order Item` join `tabPurchase Order` on `tabPurchase Order`.name = `tabPurchase Order Item`.parent
                                   where 
                                       `tabPurchase Order`.docstatus = 1
                                       and `tabPurchase Order Item`.item_code = '{itemo}'
                                       and `tabPurchase Order`.transaction_date between '{from_date}' and '{to_date}'
                               """.format(itemo=itemo, from_date=from_date, to_date=to_date), as_dict=0)

            data['po_carton'] = po[0][0] / item_dict.carton_cf if item_dict.carton_cf else po[0][0]

            pinv = frappe.db.sql(""" select 
                                        ifnull(sum(`tabPurchase Invoice Item`.stock_qty), 0) as stock_qty,
                                        ifnull(sum(`tabPurchase Invoice Item`.base_amount), 0) as amount
                                   from 
                                        `tabPurchase Invoice Item` join `tabPurchase Invoice` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                                   where 
                                       `tabPurchase Invoice`.docstatus = 1
                                       and `tabPurchase Invoice Item`.item_code = '{itemo}'
                                       and `tabPurchase Invoice`.posting_date between '{from_date}' and '{to_date}'
                               """.format(itemo=itemo, from_date=from_date, to_date=to_date), as_dict=0)
            pinv1 = frappe.db.sql(""" select 
                                        ifnull(sum(`tabPurchase Invoice Item`.stock_qty), 0) as stock_qty
                                   from 
                                        `tabPurchase Invoice Item` join `tabPurchase Invoice` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                                   where 
                                       `tabPurchase Invoice`.docstatus = 1
                                       and `tabPurchase Invoice Item`.stock_qty >0
                                       and `tabPurchase Invoice Item`.rate >0
                                       and `tabPurchase Invoice Item`.item_code = '{itemo}'
                                       and `tabPurchase Invoice`.posting_date between '{from_date}' and '{to_date}'
                               """.format(itemo=itemo, from_date=from_date, to_date=to_date), as_dict=0)
            pinv2 = frappe.db.sql(""" select 
                                        ifnull(sum(`tabPurchase Invoice Item`.stock_qty), 0) as stock_qty
                                   from 
                                        `tabPurchase Invoice Item` join `tabPurchase Invoice` on `tabPurchase Invoice`.name = `tabPurchase Invoice Item`.parent
                                   where 
                                       `tabPurchase Invoice`.docstatus = 1
                                       and `tabPurchase Invoice Item`.stock_qty >0
                                       and `tabPurchase Invoice Item`.rate =0
                                       and `tabPurchase Invoice Item`.item_code = '{itemo}'
                                       and `tabPurchase Invoice`.posting_date between '{from_date}' and '{to_date}'
                               """.format(itemo=itemo, from_date=from_date, to_date=to_date), as_dict=0)

            data['pinv_carton'] = pinv[0][0] / item_dict.carton_cf if item_dict.carton_cf else pinv[0][0]
            data['pinv_carton1'] = pinv1[0][0] / item_dict.carton_cf if item_dict.carton_cf else pinv1[0][0]
            data['pinv_carton2'] = pinv2[0][0] / item_dict.carton_cf if item_dict.carton_cf else pinv2[0][0]
            data['amount'] = pinv[0][1]
            data['avg_rate'] = pinv[0][1] * item_dict.carton_cf / pinv[0][0] if pinv[0][0] else 0

            so = frappe.db.sql(""" select 
                                                    ifnull(sum(`tabSales Order Item`.stock_qty), 0) as stock_qty
                                               from 
                                                    `tabSales Order Item` join `tabSales Order` on `tabSales Order`.name = `tabSales Order Item`.parent
                                               where 
                                                   `tabSales Order`.docstatus = 1
                                                   and `tabSales Order Item`.item_code = '{itemo}'
                                                   and `tabSales Order`.transaction_date between '{from_date}' and '{to_date}'
                                           """.format(itemo=itemo, from_date=from_date, to_date=to_date), as_dict=0)

            data['so_carton'] = so[0][0] / item_dict.carton_cf if item_dict.carton_cf else so[0][0]

            sinv = frappe.db.sql(""" select 
                                        ifnull(sum(`tabSales Invoice Item`.stock_qty), 0) as stock_qty
                                   from 
                                        `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                   where 
                                       `tabSales Invoice`.docstatus = 1
                                       and `tabSales Invoice Item`.item_code = '{itemo}'
                                       and `tabSales Invoice`.posting_date between '{from_date}' and '{to_date}'
                               """.format(itemo=itemo, from_date=from_date, to_date=to_date), as_dict=0)

            data['sinv_carton'] = sinv[0][0] / item_dict.carton_cf if item_dict.carton_cf else sinv[0][0]
            data['closing_carton'] = (opening_qty + pinv[0][0] - sinv[0][0]) / item_dict.carton_cf if item_dict.carton_cf else (opening_qty + pinv[0][0] - sinv[0][0])
            data['p_percent'] = 100 * (pinv[0][0] / po[0][0]) if po[0][0] else pinv[0][0]
            data['s_percent'] = 100 * (sinv[0][0] / so[0][0]) if so[0][0] else sinv[0][0]


            result.append(data)
    return result

