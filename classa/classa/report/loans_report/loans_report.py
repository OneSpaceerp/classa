# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters,columns)
	return columns, data

def get_columns():
	return [
		{
			"label": _("Loan"),
			"fieldname": "loan",
			"fieldtype": "Link",
			"options": "Loan",
			"width": 120
		},
		{
			"label": _("Employee"),
			"fieldname": "employee",
			"fieldtype": "Link",
			"options": "Employee",
			"width": 130
		},
		{
			"label": _("Employee Name"),
			"fieldname": "employee_name",
			"fieldtype": "Data",
			"width": 200
		},
		{
			"label": _("Loan Type"),
			"fieldname": "loan_type",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Loan Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 130
		},
		{
			"label": _("Loan Amount"),
			"fieldname": "loan_amount",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Accrual Date"),
			"fieldname": "accrual_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": _("Accrual Amount"),
			"fieldname": "accrued_amount",
			"fieldtype": "Currency",
			"width": 120
		}
	]

def get_data(filters, columns):
	item_price_qty_data = []
	item_price_qty_data = get_item_price_qty_data(filters)
	return item_price_qty_data

def get_item_price_qty_data(filters):
	conditions = ""
	if filters.get("type"):
		conditions += " and `tabLoan`.loan_type=%(type)s"
	if filters.get("status"):
		conditions += " and `tabLoan`.status=%(status)s"

	from_date = filters.get("from_date")
	to_date = filters.get("to_date")

	item_results = frappe.db.sql("""Select
					`tabLoan`.name as loan,
					`tabLoan`.applicant as employee,
					`tabLoan`.applicant_name as employee_name,
					`tabLoan`.loan_type as loan_type,
					`tabLoan`.posting_date as date,
					`tabLoan`.status as status,
					`tabLoan`.loan_amount as loan_amount,
					`tabRepayment Schedule`.total_payment as accrued_amount,
					`tabRepayment Schedule`.payment_date as accrual_date
					
					From `tabLoan` join `tabRepayment Schedule` on `tabRepayment Schedule`.parent = `tabLoan`.name
					Where
					`tabLoan`.docstatus = 1
					and payment_date between '{from_date}' and '{to_date}' 
					{conditions}
								""".format(from_date=from_date,to_date=to_date,conditions=conditions), filters, as_dict=1)


	result = []
	if item_results:
		for item_dict in item_results:
			data = {
				'loan': item_dict.loan,
				'employee': item_dict.employee,
				'employee_name': item_dict.employee_name,
				'loan_type': item_dict.loan_type,
				'date': item_dict.date,
				'status': item_dict.status,
				'loan_amount': item_dict.loan_amount,
				'accrual_date': item_dict.accrual_date,
				'accrued_amount': item_dict.accrued_amount
			}
			result.append(data)

	return result




