from __future__ import unicode_literals

import frappe

def get_context(context):
	context.mode_of_payment = frappe.db.get_list('Mode of Payment')
	pass
