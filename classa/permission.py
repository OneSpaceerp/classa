from __future__ import unicode_literals
import frappe
import erpnext
from frappe import auth
import datetime
import json, ast
from frappe.share import add

@frappe.whitelist()
def share_mr(doc, method=None):
    pass
    '''
    if doc.set_from_warehouse:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(from_warehouse=doc.set_from_warehouse),as_dict=1)
        read = 1
        write = 1
        submit = 1
        share = 1
        everyone = 0
        for x in users:
            add('Material Request', doc.name, x.user, read, write, submit, share, everyone)

    if doc.set_warehouse:
        users = frappe.db.sql(
        """ select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(
                from_warehouse=doc.set_warehouse), as_dict=1)
        read = 1
        write = 1
        submit = 1
        share = 1
        everyone = 0
        for x in users:
            add('Material Request', doc.name, x.user, read, write, submit, share, everyone)
    '''

@frappe.whitelist()
def share_se(doc, method=None):
    pass
    '''
    if doc.from_warehouse:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(from_warehouse=doc.from_warehouse),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Stock Entry', doc.name, x.user, read, write, submit, share, everyone)

    if doc.to_warehouse:
        users = frappe.db.sql(
            """ select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(
                from_warehouse=doc.to_warehouse), as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Stock Entry', doc.name, x.user, read, write, submit, share, everyone)
    '''

@frappe.whitelist()
def share_dn(doc, method=None):
    pass
    '''
    if doc.set_warehouse:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(from_warehouse=doc.set_warehouse),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Delivery Note', doc.name, x.user, read, write, submit, share, everyone)
    '''

@frappe.whitelist()
def share_so(doc, method=None):
    pass
    '''
    if doc.set_warehouse:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(from_warehouse=doc.set_warehouse),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Sales Order', doc.name, x.user, read, write, submit, share, everyone)
    '''

@frappe.whitelist()
def share_po(doc, method=None):
    pass
    '''
    if doc.set_warehouse:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(from_warehouse=doc.set_warehouse),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Purchase Order', doc.name, x.user, read, write, submit, share, everyone)
    '''

@frappe.whitelist()
def share_pr(doc, method=None):
    pass
    '''
    if doc.set_warehouse:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Warehouse' and share_name = '{from_warehouse}' """.format(from_warehouse=doc.set_warehouse),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Purchase Receipt', doc.name, x.user, read, write, submit, share, everyone)
    '''

@frappe.whitelist()
def share_sin(doc, method=None):
    pass
    '''
    if doc.customer_group:
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Customer Group' and share_name = '{customer_group}' """.format(customer_group=doc.customer_group),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Sales Invoice', doc.name, x.user, read, write, submit, share, everyone)
    '''
@frappe.whitelist()
def share_pe(doc, method=None):
    pass
    '''
    users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Account' and share_name = '{paid_to}' """.format(paid_to=doc.paid_to),as_dict=1)
    read = 1
    write = 1
    submit = 0
    share = 1
    everyone = 0
    if users:
        for x in users:
            add('Payment Entry', doc.name, x.user, read, write, submit, share, everyone)

    customer_group = frappe.db.get_value("Customer", doc.party, "customer_group")
    if doc.party_type == "Customer":
        users = frappe.db.sql(""" select user from `tabDocShare` where share_doctype = 'Customer Group' and share_name = '{customer_group}' """.format(customer_group=customer_group),as_dict=1)
        read = 1
        write = 1
        submit = 0
        share = 1
        everyone = 0
        for x in users:
            add('Payment Entry', doc.name, x.user, read, write, submit, share, everyone)
    '''

