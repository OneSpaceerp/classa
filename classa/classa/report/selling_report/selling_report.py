# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters, columns)
    return columns, data


def get_columns(filters):
    if filters.get('type') == "Large Groceries":
        return [
            {
                "label": _("Customer"),
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 200
            },
            {
                "label": _("Customer Address"),
                "fieldname": "address_display",
                "fieldtype": "Data",
                "width": 200
            },
            {
                "label": _("Branch"),
                "fieldname": "branch",
                "fieldtype": "Data",
                "width": 90
            },
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Territory Manager"),
                "fieldname": "territory_manager",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Sales Order"),
                "fieldname": "sales_order",
                "fieldtype": "Link",
                "options": "Sales Order",
                "width": 170
            },
            {
                "label": _("Order Status"),
                "fieldname": "order_status",
                "fieldtype": "Data",
                "width": 150
            },
            {
                "label": _("Order Date"),
                "fieldname": "order_date",
                "fieldtype": "Date",
                "width": 110
            },
            {
                "label": _("Order Total"),
                "fieldname": "order_total",
                "fieldtype": "Currency",
                "width": 110
            },
            {
                "label": _("Delivery Note"),
                "fieldname": "delivery_note",
                "fieldtype": "Link",
                "options": "Delivery Note",
                "width": 170
            },
            {
                "label": _("DN Status"),
                "fieldname": "dn_status",
                "fieldtype": "Data",
                "width": 150
            },
            {
                "label": _("DN Total"),
                "fieldname": "dn_total",
                "fieldtype": "Currency",
                "width": 110
            },
            {
                "label": _("Sales Invoice"),
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 120
            },
            {
                "label": _("Invoice Status"),
                "fieldname": "invoice_status",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Invoice Date"),
                "fieldname": "invoice_date",
                "fieldtype": "Date",
                "width": 110
            },
            {
                "label": _("Invoice Total"),
                "fieldname": "invoice_total",
                "fieldtype": "Currency",
                "width": 110
            }
        ]

    if filters.get('type') == "Chains":
        return [
            {
                "label": _("Customer"),
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 200
            },
            {
                "label": _("Customer Address"),
                "fieldname": "address_display",
                "fieldtype": "Data",
                "width": 200
            },
            {
                "label": _("Branch"),
                "fieldname": "branch",
                "fieldtype": "Data",
                "width": 90
            },
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Territory Manager"),
                "fieldname": "territory_manager",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Sales Order"),
                "fieldname": "sales_order",
                "fieldtype": "Link",
                "options": "Sales Order",
                "width": 170
            },
            {
                "label": _("Order Status"),
                "fieldname": "order_status",
                "fieldtype": "Data",
                "width": 150
            },
            {
                "label": _("Order Date"),
                "fieldname": "order_date",
                "fieldtype": "Date",
                "width": 110
            },
            {
                "label": _("Order Total"),
                "fieldname": "order_total",
                "fieldtype": "Currency",
                "width": 110
            },
            {
                "label": _("Delivery Note"),
                "fieldname": "delivery_note",
                "fieldtype": "Link",
                "options": "Delivery Note",
                "width": 170
            },
            {
                "label": _("DN Status"),
                "fieldname": "dn_status",
                "fieldtype": "Data",
                "width": 150
            },
           
            {
                "label": _("DN Total"),
                "fieldname": "dn_total",
                "fieldtype": "Currency",
                "width": 110
            },
            {
                "label": _("Sales Invoice"),
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 120
            },
            {
                "label": _("Invoice Status"),
                "fieldname": "invoice_status",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Invoice Date"),
                "fieldname": "invoice_date",
                "fieldtype": "Date",
                "width": 110
            },
            {
                "label": _("Invoice Total"),
                "fieldname": "invoice_total",
                "fieldtype": "Currency",
                "width": 110
            },
             {
                "label": _("Update Stock"),
                "fieldname": "update_stock",
                "fieldtype": "Integer",
                "width": 80
            },
             {
                "label": _("Warehouse"),
                "fieldname": "warehouse",
                "fieldtype": "Data",
                "width": 150
            }
        ]

    if filters.get('type') == "Retail":
        return [
            {
                "label": _("Customer"),
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 200
            },
            {
                "label": _("Customer Address"),
                "fieldname": "address_display",
                "fieldtype": "Data",
                "width": 200
            },
            {
                "label": _("Branch"),
                "fieldname": "branch",
                "fieldtype": "Data",
                "width": 90
            },
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Territory Manager"),
                "fieldname": "territory_manager",
                "fieldtype": "Data",
                "width": 180
            },
            {
                "label": _("Sales Invoice"),
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 120
            },
            {
                "label": _("Invoice Status"),
                "fieldname": "invoice_status",
                "fieldtype": "Data",
                "width": 120
            },
            {
                "label": _("Invoice Date"),
                "fieldname": "invoice_date",
                "fieldtype": "Date",
                "width": 110
            },
            {
                "label": _("Grand Total"),
                "fieldname": "grand_total",
                "fieldtype": "Currency",
                "width": 110
            }
        ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    
    result = []
    if filters.get('type') == "Retail":
        item_results = frappe.db.sql("""
                SELECT
                    `tabSales Invoice`.name as sales_invoice,
                    `tabSales Invoice`.status as invoice_status,
                    `tabSales Invoice`.posting_date as invoice_date,
                    `tabSales Invoice`.customer as customer,
                    `tabSales Invoice`.address_display as address_display,
                    `tabSales Invoice`.branch as branch,
                    `tabSales Invoice`.grand_total as grand_total ,
                    `tabSales Invoice`.sales_person as sales_person,
                    `tabSales Invoice`.territory as branch,
                    `tabSales Invoice`.territory_manager as territory_manager
                    from
                    `tabSales Invoice`
                    where
                    `tabSales Invoice`.customer_group in ("عملاء التجزئة","عملاء جمله","مجموعة التجزئة")
                    {conditions}
                """.format(conditions=conditions), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'sales_invoice': item_dict.sales_invoice,
                    'invoice_status': item_dict.invoice_status,
                    'invoice_date': item_dict.invoice_date,
                    'customer': item_dict.customer,
                    'address_display': item_dict.address_display,
                    'branch': item_dict.branch,
                    'sales_person': item_dict.sales_person,
                    'territory_manager': item_dict.territory_manager,
                    'grand_total': item_dict.grand_total
                }
                result.append(data)
        return result

    if filters.get('type') == "Chains":
        conditions = "and `tabSales Order`.transaction_date between %(from_date)s and %(to_date)s"
        item_results = frappe.db.sql("""
                SELECT                  
                    `tabSales Order`.name as sales_order,
                    `tabSales Order`.status as order_status,
                    `tabSales Order`.customer as customer,
                    `tabSales Order`.address_display as address_display,
                    `tabSales Order`.transaction_date as order_date,
                    `tabSales Order`.grand_total as order_total,
                    `tabSales Order`.sales_person as sales_person,
                    `tabSales Order`.territory as branch,
                    `tabSales Order`.territory_manager as territory_manager
                    from
                    `tabSales Order` 
                    where
                    `tabSales Order`.customer_group in  ("كبار عملاء السلاسل","القطاع الحكومي","بنزينات السلاسل","قسم هوريكا وتوريدات","مجموعة السلاسل")
                    {conditions}
                """.format(conditions=conditions), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'customer': item_dict.customer,
                    'address_display': item_dict.address_display,
                    'branch': item_dict.branch,
                    'sales_order': item_dict.sales_order,
                    'order_status': item_dict.order_status,
                    'order_date': item_dict.order_date,
                    'territory_manager':item_dict.territory_manager,
                    'sales_person':item_dict.sales_person,
                    'order_total': item_dict.order_total
                }
                sdelivery = frappe.db.sql(""" select name as delivery_note,
                                                        status as dn_status,
                                                        grand_total as dn_total
                                                        from `tabDelivery Note` where docstatus < 2 and is_return = 0 and sales_order = '{sales_order}'
                                                         """.format(sales_order=item_dict.sales_order),as_dict=1)
                for e in sdelivery:
                    data['delivery_note']=e.delivery_note
                    data['dn_status']=e.dn_status
                    data['dn_total']=e.dn_total
                    data['invoice_total']=e.invoice_total
                    sinvoice = frappe.db.sql(""" select name as sales_invoice,
                                                    posting_date as invoice_date,
                                                    status as invoice_status,
                                                    grand_total as invoice_total,
                                                    update_stock as update_stock,
                                                    set_warehouse as warehouse
                                                    from `tabSales Invoice` where delivery_note = '{dn}' and docstatus<2 and is_return = 0 """.format(dn=e.delivery_note),as_dict=1)
                    for d in sinvoice:
                        data['sales_invoice']=d.sales_invoice
                        data['invoice_status']=d.invoice_status
                        data['invoice_date']=d.invoice_date
                        data['invoice_total']=d.invoice_total



                result.append(data)
        return result


    if filters.get('type') == "Large Groceries":
        item_results = frappe.db.sql("""
                SELECT                  
                    `tabSales Order`.name as sales_order,
                    `tabSales Order`.status as order_status,
                    `tabSales Order`.customer as customer,
                    `tabSales Order`.address_display as address_display,
                    `tabSales Order`.transaction_date as order_date,
                    `tabSales Order`.grand_total as order_total,
                    `tabSales Order`.territory as branch,
                    `tabSales Order`.sales_person as sales_person,
                    `tabSales Order`.territory_manager as territory_manager
                    from
                    `tabSales Order` 
                    where
                    `tabSales Order`.customer_group = "كبار عملاء تجزئة"
                    {conditions}
                """.format(conditions=conditions), filters, as_dict=1)

        if item_results:
            for item_dict in item_results:
                data = {
                    'customer': item_dict.customer,
                    'address_display': item_dict.address_display,
                    'branch': item_dict.branch,
                    'sales_order': item_dict.sales_order,
                    'order_status': item_dict.order_status,
                    'order_date': item_dict.order_date,
                    'sales_person': item_dict.sales_person,
                    'territory_manager': item_dict.territory_manager,
                    'order_total': item_dict.order_total
                }
                sdelivery = frappe.db.sql(""" select name as delivery_note,
                                                        status as dn_status,
                                                        grand_total as dn_total
                                                        from `tabDelivery Note` where docstatus < 2 and is_return = 0 and sales_order = '{sales_order}'
                                                         """.format(sales_order=item_dict.sales_order),as_dict=1)
                for e in sdelivery:
                    data['delivery_note']=e.delivery_note
                    data['dn_status']=e.dn_status
                    data['dn_total']=e.dn_total
                    data['invoice_total']=e.invoice_total
                    sinvoice = frappe.db.sql(""" select name as sales_invoice,
                                                    posting_date as invoice_date,
                                                    status as invoice_status,
                                                    grand_total as invoice_total,
                                                    update_stock as update_stock,
                                                    set_warehouse as warehouse
                                                    from `tabSales Invoice` where delivery_note = '{dn}' and docstatus<2 and is_return = 0 """.format(dn=e.delivery_note),as_dict=1)
                    for d in sinvoice:
                        data['sales_invoice']=d.sales_invoice
                        data['invoice_status']=d.invoice_status
                        data['invoice_date']=d.invoice_date
                        data['invoice_total']=d.invoice_total



                result.append(data)
        return result

