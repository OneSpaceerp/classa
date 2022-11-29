# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import msgprint, _
from frappe.utils import flt


def execute(filters=None):
    columns, data = [], []
    columns = get_columns(filters)
    data = get_data(filters, columns)
    return columns, data


def get_columns(filters):
    if filters.get('group_by_item'):
        return [
            {
                "label": _("Item"),
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "width": 70
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
                "width": 160
            },
            {
                "label": _("قطعة"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("م.ت الكرتونة"),
                "fieldname": "carton_cf",
                "fieldtype": "Float",
                "width": 100
            },
            {
                "label": _("كرتونة"),
                "fieldname": "carton_qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("Average Rate"),
                "fieldname": "rate",
                "fieldtype": "Currency",
                "width": 120
            },
            {
                "label": _("Amount"),
                "fieldname": "amount",
                "fieldtype": "Currency",
                "width": 120
            }
        ]
    if filters.get('group_by_customer'):
        return [
            {
                "label": _("Customer"),
                "fieldname": "customer",
                "fieldtype": "Link",
                "options": "Customer",
                "width": 130
            },
            {
                "label": _("Code"),
                "fieldname": "code",
                "fieldtype": "Data",
                "width": 70
            },
            {
                "label": _("Customer Group"),
                "fieldname": "customer_group",
                "fieldtype": "Data",
                "width": 130
            },
            {
                "label": _("قطعة"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("كرتونة"),
                "fieldname": "carton",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("Amount"),
                "fieldname": "amount",
                "fieldtype": "Currency",
                "width": 120
            }
        ]
    if filters.get('group_by_customer_group'):
        return [
            {
                "label": _("Customer Group"),
                "fieldname": "customer_group",
                "fieldtype": "Link",
                "options": "Customer Group",
                "width": 130
            },
            {
                "label": _("قطعة"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("كرتونة"),
                "fieldname": "carton",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("Amount"),
                "fieldname": "amount",
                "fieldtype": "Currency",
                "width": 120
            }
        ]
    if filters.get('group_by_sales_person'):
        return [
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Link",
                "options": "Sales Person",
                "width": 130
            },
            {
                "label": _("قطعة"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("كرتونة"),
                "fieldname": "carton",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("Amount"),
                "fieldname": "amount",
                "fieldtype": "Currency",
                "width": 120
            }
        ]
    if filters.get('group_by_branch'):
        return [
            {
                "label": _("Branch"),
                "fieldname": "branch",
                "fieldtype": "Link",
                "options": "Branch",
                "width": 130
            },
            {
                "label": _("قطعة"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("كرتونة"),
                "fieldname": "carton",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("Amount"),
                "fieldname": "amount",
                "fieldtype": "Currency",
                "width": 120
            }
        ]
    else:
        return [
            {
                "label": _("Item"),
                "fieldname": "item_code",
                "fieldtype": "Link",
                "options": "Item",
                "width": 70
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
                "width": 160
            },
            {
                "label": _("قطعة"),
                "fieldname": "stock_qty",
                "fieldtype": "Float",
                "width": 90
            },
            {
                "label": _("Conversion Factor"),
                "fieldname": "conversion_factor",
                "fieldtype": "float",
                "width": 140
            },
            {
                "label": _("كرتونة"),
                "fieldname": "qty",
                "fieldtype": "Float",
                "width": 80
            },
            {
                "label": _("Price List Rate"),
                "fieldname": "price_list_rate",
                "fieldtype": "Currency",
                "width": 120
            },
            {
                "label": _("Discount"),
                "fieldname": "discount_percentage",
                "fieldtype": "Percent",
                "width": 90
            },
            {
                "label": _("Rate"),
                "fieldname": "rate",
                "fieldtype": "Currency",
                "width": 100
            },
            {
                "label": _("Amount"),
                "fieldname": "amount",
                "fieldtype": "Currency",
                "width": 110
            },
            {
                "label": _("Date"),
                "fieldname": "posting_date",
                "fieldtype": "Date",
                "width": 110
            },
            {
                "label": _("Invoice No"),
                "fieldname": "sales_invoice",
                "fieldtype": "Link",
                "options": "Sales Invoice",
                "width": 110
            },
            {
                "label": _("Tax Type"),
                "fieldname": "tax_type",
                "fieldtype": "Data",
                "width": 110
            },
            {
                "label": _("Customer"),
                "fieldname": "customer",
                "fieldtype": "Data",
                "width": 210
            },
            {
                "label": _("Customer Code"),
                "fieldname": "customer_code",
                "fieldtype": "Data",
                "width": 140
            },
            {
                "label": _("Customer Address"),
                "fieldname": "customer_address",
                "fieldtype": "Data",
                "width": 230
            },
            {
                "label": _("Territory"),
                "fieldname": "territory",
                "fieldtype": "Data",
                "width": 110
            },
            {
                "label": _("Branch"),
                "fieldname": "branch",
                "fieldtype": "Data",
                "width": 110
            },
            {
                "label": _("Sales Person"),
                "fieldname": "sales_person",
                "fieldtype": "Data",
                "width": 180
            }
        ]

    


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    

    if filters.get('group_by_item'):
        conditions = ""
        if filters.get("item_code"):
            conditions += "and `tabSales Invoice Item`.item_code = %(item_code)s"
        if filters.get("item_group"):
            conditions += "and `tabSales Invoice Item`.item_group = %(item_group)s"
        if filters.get("from_date"):
            conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
        if filters.get("to_date"):
            conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
        if filters.get("customer"):
            conditions += "and `tabSales Invoice`.customer = %(customer)s"
        if filters.get("territory"):
            conditions += "and `tabSales Invoice`.territory = %(territory)s"
        if filters.get("branch"):
            conditions += "and `tabSales Invoice`.branch = %(branch)s"
        if filters.get("sales_person"):
            conditions += "and `tabSales Invoice`.sales_person = %(sales_person)s"
        if filters.get("sales_invoice"):
            conditions += "and `tabSales Invoice`.name = %(sales_invoice)s"
        if filters.get("tax_type"):
            conditions += "and `tabSales Invoice`.tax_type = %(tax_type)s"
        if filters.get("is_return"):
            conditions += "and `tabSales Invoice`.is_return = %(is_return)s and `tabSales Invoice Item`.stock_qty < 0"
        else:
            conditions += "and `tabSales Invoice Item`.stock_qty > 0"
        item_results2 = frappe.db.sql("""
                    SELECT distinct
                        `tabSales Invoice Item`.item_code as item_code,
                        `tabSales Invoice Item`.item_name as item_name,
                        `tabSales Invoice Item`.stock_uom as stock_uom,
                        `tabSales Invoice Item`.item_group as item_group,
                        `tabSales Invoice Item`.barcode as barcode,
                        (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabSales Invoice Item`.item_code) as carton_cf
    
                    FROM
                        `tabSales Invoice Item` join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                    WHERE
                        `tabSales Invoice`.docstatus = 1
                        {conditions}           
    
                    Group BY `tabSales Invoice Item`.item_code
                    """.format(conditions=conditions), filters, as_dict=1)

        result2 = []
        if item_results2:
            for item_dict in item_results2:
                data = {
                    'item_code': item_dict.item_code,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'barcode': item_dict.barcode,
                    'carton_cf': item_dict.carton_cf,

                }
                details = frappe.db.sql("""
                        SELECT 
    
                            sum(`tabSales Invoice Item`.stock_qty) as qty,
                            sum(`tabSales Invoice Item`.amount) as amount
    
                        FROM
                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                        WHERE 
                            `tabSales Invoice Item`.item_code = '{name}'
                            and `tabSales Invoice`.docstatus = 1
                            {conditions}
                        """.format(name=item_dict.item_code, conditions=conditions), filters, as_dict=1)

                details1 = frappe.db.sql("""
                                        SELECT 

                                            avg(`tabSales Invoice Item`.rate) as rate

                                        FROM
                                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        WHERE 
                                            `tabSales Invoice Item`.item_code = '{name}'
                                            and `tabSales Invoice Item`.conversion_factor = 1
                                            and `tabSales Invoice`.docstatus = 1
                                        """.format(name=item_dict.item_code), as_dict=1)

                for x in details:
                    data['qty'] = x.qty
                    data['carton_qty'] = (x.qty / item_dict.carton_cf) if item_dict.carton_cf else x.qty
                    data['amount'] = x.amount

                for z in details1:
                    data['rate'] = z.rate

                result2.append(data)
        return result2

    

    if filters.get('group_by_customer'):
        conditions = ""
        main_conditions = ""
        if filters.get("item_code"):
            conditions += "and `tabSales Invoice Item`.item_code = %(item_code)s"
        if filters.get("item_group"):
            conditions += "and `tabSales Invoice Item`.item_group = %(item_group)s"
        if filters.get("from_date"):
            main_conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
            conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
        if filters.get("to_date"):
            main_conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
            conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
        if filters.get("customer"):
            main_conditions += "and `tabSales Invoice`.customer = %(customer)s"
        if filters.get("territory"):
            main_conditions += "and `tabSales Invoice`.territory = %(territory)s"
        if filters.get("branch"):
            main_conditions += "and `tabSales Invoice`.branch = %(branch)s"
        if filters.get("sales_person"):
            main_conditions += "and `tabSales Invoice`.sales_person = %(sales_person)s"
        if filters.get("sales_invoice"):
            main_conditions += "and `tabSales Invoice`.name = %(sales_invoice)s"
        if filters.get("tax_type"):
            main_conditions += "and `tabSales Invoice`.tax_type = %(tax_type)s"
        if filters.get("is_return"):
            main_conditions += "and `tabSales Invoice`.is_return = 1"
        else:
            main_conditions += "and `tabSales Invoice`.is_return = 0"
        item_results2 = frappe.db.sql("""
                    SELECT distinct
                        `tabSales Invoice`.customer as customer,
                        `tabSales Invoice`.customer_group as customer_group,
                        (select code from `tabCustomer` where name = `tabSales Invoice`.customer) as code
                    FROM
                        `tabSales Invoice`
                    WHERE
                        `tabSales Invoice`.docstatus = 1
                     {conditions}
                    Group BY `tabSales Invoice`.customer
                    """.format(conditions=main_conditions), filters, as_dict=1)

        result2 = []
        if item_results2:
            for item_dict in item_results2:
                data = {
                    'customer': item_dict.customer,
                    'customer_group': item_dict.customer_group,
                    'item_group': item_dict.item_group,
                    'code': item_dict.code

                }
                details = frappe.db.sql("""
                        SELECT 
                            sum(`tabSales Invoice Item`.stock_qty) as qty,
                             (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabSales Invoice Item`.item_code) as carton_cf,
                            sum(`tabSales Invoice Item`.amount) as amount
                        FROM
                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                        WHERE 
                            `tabSales Invoice`.customer = '{customer}'
                            and `tabSales Invoice`.docstatus = 1
                            {conditions} {main_conditions}
                        """.format(customer=item_dict.customer, conditions=conditions,main_conditions=main_conditions), filters, as_dict=1)

                details1 = frappe.db.sql("""
                                        SELECT 

                                            avg(`tabSales Invoice Item`.rate) as rate

                                        FROM
                                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        WHERE 
                                            `tabSales Invoice`.customer = '{customer}'
                                            and `tabSales Invoice Item`.conversion_factor = 1
                                            and `tabSales Invoice`.docstatus = 1
                                        """.format(customer=item_dict.customer), as_dict=1)

                for x in details:
                    data['qty'] = x.qty
                    data['carton'] = (x.qty / x.carton_cf) if x.carton_cf else x.qty
                    data['amount'] = x.amount

                for z in details1:
                    data['rate'] = z.rate

                result2.append(data)
        return result2




    if filters.get('group_by_customer_group'):
        conditions = ""
        main_conditions = ""
        if filters.get("item_code"):
            conditions += "and `tabSales Invoice Item`.item_code = %(item_code)s"
        if filters.get("item_group"):
            conditions += "and `tabSales Invoice Item`.item_group = %(item_group)s"
        if filters.get("from_date"):
            main_conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
            conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
        if filters.get("to_date"):
            main_conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
            conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
        if filters.get("customer"):
            main_conditions += "and `tabSales Invoice`.customer = %(customer)s"
        if filters.get("territory"):
            main_conditions += "and `tabSales Invoice`.territory = %(territory)s"
        if filters.get("branch"):
            main_conditions += "and `tabSales Invoice`.branch = %(branch)s"
        if filters.get("sales_person"):
            main_conditions += "and `tabSales Invoice`.sales_person = %(sales_person)s"
        if filters.get("sales_invoice"):
            main_conditions += "and `tabSales Invoice`.name = %(sales_invoice)s"
        if filters.get("tax_type"):
            main_conditions += "and `tabSales Invoice`.tax_type = %(tax_type)s"
        if filters.get("is_return"):
            main_conditions += "and `tabSales Invoice`.is_return = 1"
        else:
            main_conditions += "and `tabSales Invoice`.is_return = 0"
        item_results2 = frappe.db.sql("""
                    SELECT distinct
                        `tabSales Invoice`.customer_group as customer_group
                       
                    FROM
                        `tabSales Invoice`
                    WHERE
                        `tabSales Invoice`.docstatus = 1
                     {conditions}
                    Group BY `tabSales Invoice`.customer_group
                    """.format(conditions=main_conditions), filters, as_dict=1)

        result2 = []
        if item_results2:
            for item_dict in item_results2:
                data = {
                    'customer_group': item_dict.customer_group,
                    'code': item_dict.code

                }
                details = frappe.db.sql("""
                        SELECT 
                            sum(`tabSales Invoice Item`.stock_qty) as qty,
                            (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabSales Invoice Item`.item_code) as carton_cf,
                            sum(`tabSales Invoice Item`.amount) as amount
                        FROM
                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                        WHERE 
                            `tabSales Invoice`.customer_group = '{customer_group}'
                            and `tabSales Invoice`.docstatus = 1
                            {conditions} {main_conditions}
                        """.format(customer_group=item_dict.customer_group, conditions=conditions,main_conditions=main_conditions), filters, as_dict=1)

                details1 = frappe.db.sql("""
                                        SELECT 

                                            avg(`tabSales Invoice Item`.rate) as rate

                                        FROM
                                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        WHERE 
                                            `tabSales Invoice`.customer_group = '{customer_group}'
                                            and `tabSales Invoice Item`.conversion_factor = 1
                                            and `tabSales Invoice`.docstatus = 1
                                        """.format(customer_group=item_dict.customer_group), as_dict=1)

                for x in details:
                    data['qty'] = x.qty
                    data['carton'] = (x.qty / item_dict.carton_cf) if item_dict.carton_cf else x.qty
                    data['amount'] = x.amount

                for z in details1:
                    data['rate'] = z.rate

                result2.append(data)
        return result2



    if filters.get('group_by_sales_person'):
        conditions = ""
        main_conditions = ""
        if filters.get("item_code"):
            conditions += "and `tabSales Invoice Item`.item_code = %(item_code)s"
        if filters.get("item_group"):
            conditions += "and `tabSales Invoice Item`.item_group = %(item_group)s"
        if filters.get("from_date"):
            main_conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
            conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
        if filters.get("to_date"):
            main_conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
            conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
        if filters.get("customer"):
            main_conditions += "and `tabSales Invoice`.customer = %(customer)s"
        if filters.get("territory"):
            main_conditions += "and `tabSales Invoice`.territory = %(territory)s"
        if filters.get("branch"):
            main_conditions += "and `tabSales Invoice`.branch = %(branch)s"
        if filters.get("sales_person"):
            main_conditions += "and `tabSales Invoice`.sales_person = %(sales_person)s"
        if filters.get("sales_invoice"):
            main_conditions += "and `tabSales Invoice`.name = %(sales_invoice)s"
        if filters.get("tax_type"):
            main_conditions += "and `tabSales Invoice`.tax_type = %(tax_type)s"
        if filters.get("is_return"):
            main_conditions += "and `tabSales Invoice`.is_return = 1"
        else:
            main_conditions += "and `tabSales Invoice`.is_return = 0"
        item_results2 = frappe.db.sql("""
                    SELECT distinct
                        `tabSales Invoice`.sales_person as sales_person
                       
                    FROM
                        `tabSales Invoice`
                    WHERE
                        `tabSales Invoice`.docstatus = 1
                     {conditions}
                    Group BY `tabSales Invoice`.sales_person
                    """.format(conditions=main_conditions), filters, as_dict=1)

        result2 = []
        if item_results2:
            for item_dict in item_results2:
                data = {
                    'sales_person': item_dict.sales_person,
                    'code': item_dict.code

                }
                details = frappe.db.sql("""
                        SELECT 
                            sum(`tabSales Invoice Item`.stock_qty) as qty,
                            (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabSales Invoice Item`.item_code) as carton_cf,
                            sum(`tabSales Invoice Item`.amount) as amount
                        FROM
                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                        WHERE 
                            `tabSales Invoice`.sales_person = '{sales_person}'
                            and `tabSales Invoice`.docstatus = 1
                            {conditions} {main_conditions}
                        """.format(sales_person=item_dict.sales_person, conditions=conditions,main_conditions=main_conditions), filters, as_dict=1)

                details1 = frappe.db.sql("""
                                        SELECT 

                                            avg(`tabSales Invoice Item`.rate) as rate

                                        FROM
                                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        WHERE 
                                            `tabSales Invoice`.sales_person = '{sales_person}'
                                            and `tabSales Invoice Item`.conversion_factor = 1
                                            and `tabSales Invoice`.docstatus = 1
                                        """.format(sales_person=item_dict.sales_person), as_dict=1)

                for x in details:
                    data['qty'] = x.qty
                    data['carton'] = (x.qty / item_dict.carton_cf) if item_dict.carton_cf else x.qty
                    data['amount'] = x.amount

                for z in details1:
                    data['rate'] = z.rate

                result2.append(data)
        return result2


    if filters.get('group_by_branch'):
        conditions = ""
        main_conditions = ""
        if filters.get("item_code"):
            conditions += "and `tabSales Invoice Item`.item_code = %(item_code)s"
        if filters.get("item_group"):
            conditions += "and `tabSales Invoice Item`.item_group = %(item_group)s"
        if filters.get("from_date"):
            main_conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
            conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
        if filters.get("to_date"):
            main_conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
            conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
        if filters.get("customer"):
            main_conditions += "and `tabSales Invoice`.customer = %(customer)s"
        if filters.get("territory"):
            main_conditions += "and `tabSales Invoice`.territory = %(territory)s"
        if filters.get("branch"):
            main_conditions += "and `tabSales Invoice`.branch = %(branch)s"
        if filters.get("sales_person"):
            main_conditions += "and `tabSales Invoice`.sales_person = %(sales_person)s"
        if filters.get("sales_invoice"):
            main_conditions += "and `tabSales Invoice`.name = %(sales_invoice)s"
        if filters.get("tax_type"):
            main_conditions += "and `tabSales Invoice`.tax_type = %(tax_type)s"
        if filters.get("is_return"):
            main_conditions += "and `tabSales Invoice`.is_return = 1"
        else:
            main_conditions += "and `tabSales Invoice`.is_return = 0"
        item_results2 = frappe.db.sql("""
                    SELECT distinct
                        `tabSales Invoice`.branch as branch
                       
                    FROM
                        `tabSales Invoice`
                    WHERE
                        `tabSales Invoice`.docstatus = 1
                     {conditions}
                    Group BY `tabSales Invoice`.branch
                    """.format(conditions=main_conditions), filters, as_dict=1)

        result2 = []
        if item_results2:
            for item_dict in item_results2:
                data = {
                    'branch': item_dict.branch,
                    'code': item_dict.code

                }
                details = frappe.db.sql("""
                        SELECT 
                            sum(`tabSales Invoice Item`.stock_qty) as qty,
                            (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabSales Invoice Item`.item_code) as carton_cf,
                            sum(`tabSales Invoice Item`.amount) as amount
                        FROM
                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                        WHERE 
                            `tabSales Invoice`.branch = '{branch}'
                            and `tabSales Invoice`.docstatus = 1
                            {conditions} {main_conditions}
                        """.format(branch=item_dict.branch, conditions=conditions,main_conditions=main_conditions), filters, as_dict=1)

                details1 = frappe.db.sql("""
                                        SELECT 

                                            avg(`tabSales Invoice Item`.rate) as rate

                                        FROM
                                            `tabSales Invoice Item`  join `tabSales Invoice` on `tabSales Invoice`.name = `tabSales Invoice Item`.parent
                                        WHERE 
                                            `tabSales Invoice`.branch = '{branch}'
                                            and `tabSales Invoice Item`.conversion_factor = 1
                                            and `tabSales Invoice`.docstatus = 1
                                        """.format(branch=item_dict.branch), as_dict=1)

                for x in details:
                    data['qty'] = x.qty
                    data['carton'] = (x.qty / item_dict.carton_cf) if item_dict.carton_cf else x.qty
                    data['amount'] = x.amount

                for z in details1:
                    data['rate'] = z.rate

                result2.append(data)
        return result2




    else:
        conditions = ""
        if filters.get("item_code"):
            conditions += "and `tabSales Invoice Item`.item_code = %(item_code)s"
        if filters.get("item_group"):
            conditions += "and `tabSales Invoice Item`.item_group = %(item_group)s"
        if filters.get("from_date"):
            conditions += " and `tabSales Invoice`.posting_date>=%(from_date)s"
        if filters.get("to_date"):
            conditions += " and `tabSales Invoice`.posting_date<=%(to_date)s"
        if filters.get("customer"):
            conditions += "and `tabSales Invoice`.customer = %(customer)s"
        if filters.get("territory"):
            conditions += "and `tabSales Invoice`.territory = %(territory)s"
        if filters.get("branch"):
            conditions += "and `tabSales Invoice`.branch = %(branch)s"
        if filters.get("sales_person"):
            conditions += "and `tabSales Invoice`.sales_person = %(sales_person)s"
        if filters.get("sales_invoice"):
            conditions += "and `tabSales Invoice`.name = %(sales_invoice)s"
        if filters.get("tax_type"):
            conditions += "and `tabSales Invoice`.tax_type = %(tax_type)s"
        if filters.get("is_return"):
            conditions += "and `tabSales Invoice`.is_return = %(is_return)s and `tabSales Invoice Item`.stock_qty < 0"
        else:
            conditions += "and `tabSales Invoice Item`.stock_qty > 0"
        item_results = frappe.db.sql("""
            SELECT 
                `tabSales Invoice Item`.item_code as item_code,
                `tabSales Invoice Item`.item_name as item_name,
                `tabSales Invoice Item`.item_group as item_group,
                `tabSales Invoice Item`.barcode as barcode,
                `tabSales Invoice Item`.stock_uom as stock_uom,
                (select ifnull(conversion_factor, 1) from `tabUOM Conversion Detail` where uom = 'كرتونه' and parent = `tabSales Invoice Item`.item_code) as conversion_factor,
                `tabSales Invoice Item`.stock_qty as stock_qty,
                `tabSales Invoice Item`.uom as uom,
                `tabSales Invoice Item`.price_list_rate as price_list_rate,
                `tabSales Invoice Item`.discount_percentage as discount_percentage,
                `tabSales Invoice Item`.rate as rate,
                `tabSales Invoice Item`.amount as amount,
                `tabSales Invoice`.posting_date as posting_date,
                `tabSales Invoice`.name as sales_invoice,
                `tabSales Invoice`.tax_type as tax_type,
                `tabSales Invoice`.customer as customer,
                `tabSales Invoice`.customer_address as customer_address,
                `tabSales Invoice`.branch as branch,
                `tabSales Invoice`.territory as territory,
                `tabSales Invoice`.sales_person as sales_person,
                (Select `tabCustomer`.code from `tabCustomer` where `tabCustomer`.name = `tabSales Invoice`.customer) as customer_code
                
            FROM
                `tabSales Invoice` join `tabSales Invoice Item` on `tabSales Invoice Item`.parent = `tabSales Invoice`.name
            WHERE
                `tabSales Invoice`.docstatus = 1
                {conditions}
            ORDER BY
                `tabSales Invoice`.posting_date desc
            """.format(conditions=conditions), filters, as_dict=1)

        result = []

        if item_results:
            for item_dict in item_results:
                data = {
                    'item_code': item_dict.item_code,
                    'item_name': item_dict.item_name,
                    'item_group': item_dict.item_group,
                    'barcode': item_dict.barcode,
                    'qty': (item_dict.stock_qty / item_dict.conversion_factor) if item_dict.conversion_factor else item_dict.stock_qty,
                    'stock_uom': item_dict.stock_uom,
                    'conversion_factor': item_dict.conversion_factor,
                    'stock_qty': item_dict.stock_qty,
                    'uom': item_dict.uom,
                    'discount_percentage': item_dict.discount_percentage,
                    'price_list_rate': item_dict.price_list_rate,
                    'rate': item_dict.rate,
                    'amount': item_dict.amount,
                    'posting_date': item_dict.posting_date,
                    'sales_invoice': item_dict.sales_invoice,
                    'customer': item_dict.customer,
                    'customer_address': item_dict.customer_address,
                    'customer_code': item_dict.customer_code,
                    'territory': item_dict.territory,
                    'branch': item_dict.branch,
                    'sales_person': item_dict.sales_person,
                    'tax_type': item_dict.tax_type,
                }
                result.append(data)
        return result

    

