# Copyright (c) 2021, ERP Cloud Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, erpnext, json
from frappe.utils import cstr, flt, fmt_money, formatdate, getdate, nowdate, cint, get_link_to_form
from frappe import msgprint, _, scrub
from erpnext.controllers.accounts_controller import AccountsController
from dateutil.relativedelta import relativedelta
from erpnext.accounts.utils import get_balance_on, get_stock_accounts, get_stock_and_account_balance, \
	get_account_currency, check_if_stock_and_account_balance_synced
from erpnext.accounts.party import get_party_account
from erpnext.hr.doctype.expense_claim.expense_claim import update_reimbursed_amount
from erpnext.accounts.doctype.invoice_discounting.invoice_discounting \
	import get_party_account_based_on_invoice_discounting
from erpnext.accounts.deferred_revenue import get_deferred_booking_accounts
from frappe.model.document import Document
from six import string_types, iteritems



class CommissionPayment(Document):
	pass

	def validate(self):
		if self.total_achieved ==0:
			self.get_details()
		self.commission_calculations()
		self.get_rates()

	def on_submit(self):
		self.update_invoice_payment()
		self.make_jv()

	def on_cancel(self):
		self.cancel_invoice_payment()

	@frappe.whitelist()
	def get_details(self):
		if self.sales_chanel == "Chains":
			if self.pay_to =="Sales Person":
				invoices =frappe.db.sql(""" select name as name ,
											customer as customer,
											posting_date as posting_date,
											net_total as net_total,
											outstanding_amount as outstanding
											from `tabSales Invoice` 
											where 
											docstatus=1 
											and sales_person = %s
											and sales_person_paid =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Sales Invoice"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.net_total
					row.outstanding = comm.outstanding
					row.commissions = comm.commissions


			elif self.pay_to =="Sales Supervisor":
				invoices =frappe.db.sql(""" select name as name ,
											customer as customer,
											posting_date as posting_date,
											net_total as net_total,
											outstanding_amount as outstanding
											from `tabSales Invoice` 
											where 
											docstatus=1 
											and sales_supervisor = %s
											and sales_supervisor_paid =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Sales Invoice"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.net_total
					row.outstanding = comm.outstanding
					row.commissions = comm.commissions

			elif self.pay_to =="Territory Manager":
				invoices =frappe.db.sql(""" select name as name ,
											customer as customer,
											posting_date as posting_date,
											net_total as net_total,
											outstanding_amount as outstanding
											from `tabSales Invoice` 
											where 
											docstatus=1 
											and territory_manager = %s
											and territory_manager_paid =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Sales Invoice"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.net_total
					row.outstanding = comm.outstanding
					row.commissions = comm.commissions

			elif self.pay_to == "Sales Manager":
				invoices =frappe.db.sql(""" select name as name ,
											customer as customer,
											posting_date as posting_date,
											net_total as net_total,
											outstanding_amount as outstanding
											from `tabSales Invoice` 
											where 
											docstatus=1 
											and sales_manager = %s
											and sales_manager_paid_ = 0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Sales Invoice"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.net_total
					row.outstanding = comm.outstanding
					row.commissions = comm.commissions

		if self.sales_chanel == "Retail":
			if self.pay_to =="Sales Person":
				invoices =frappe.db.sql(""" select name as name ,
											party as customer,
											posting_date as posting_date,
											paid_amount as paid_amount
											from `tabPayment Entry` 
											where 
											docstatus=1 
											and sales_person = %s
											and sales_person_paid =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Payment Entry"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.paid_amount

			elif self.pay_to =="Sales Supervisor":
				invoices =frappe.db.sql(""" select name as name ,
											party as customer,
											posting_date as posting_date,
											paid_amount as paid_amount
											from `tabPayment Entry` 
											where 
											docstatus=1 
											and sales_supervisor = %s
											and sales_supervisor_paid =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Payment Entry"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.paid_amount

			elif self.pay_to =="Territory Manager":
				invoices =frappe.db.sql(""" select name as name ,
											party as customer,
											posting_date as posting_date,
											paid_amount as paid_amount
											from `tabPayment Entry` 
											where 
											docstatus=1 
											and territory_manager = %s
											and territory_manager_paid =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Payment Entry"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.paid_amount

			elif self.pay_to =="Sales Manager":
				invoices =frappe.db.sql(""" select name as name ,
											party as customer,
											posting_date as posting_date,
											paid_amount as paid_amount
											from `tabPayment Entry` 
											where 
											docstatus=1 
											and sales_manager = %s
											and sales_manager_paid_ =0
											""", self.employee,as_dict=True)
				for comm in invoices:
					row = self.append('commission_details', {})
					row.reference_type = "Payment Entry"
					row.reference_name = comm.name
					row.customer = comm.customer
					row.posting_date = comm.posting_date
					row.net_total = comm.paid_amount
	"""
	@frappe.whitelist()
	def get_commission_details(self):
		process = frappe.get_doc("Sales Person", self.employee)
		if process:
			if process.sales_person_targets:
				self.add_item_in_table(process.sales_person_targets, "sales_person_targets")

	@frappe.whitelist()
	def add_item_in_table(self, table_value, table_name):
		self.set(table_name, [])
		for item in table_value:
			po_item = self.append(table_name, {})
			po_item.tier = item.tier
			po_item.from_amt = item.from_amt
			po_item.to_amt = item.to_amt
			po_item.rate = item.rate
	"""
	def update_invoice_payment(self):
		if self.sales_chanel == "Chains":
			if self.pay_to == "Sales Person":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set sales_person_paid = 1 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales supervisor":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set sales_supervisor_paid = 1 where name = %s """,inv.reference_name)
			elif self.pay_to == "Territory Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set territory_manager_paid = 1 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set sales_manager_paid = 1 where name = %s """,inv.reference_name)
		elif self.sales_chanel == "Retail":
			if self.pay_to == "Sales Person":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set sales_person_paid = 1 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales supervisor":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set sales_supervisor_paid = 1 where name = %s """,inv.reference_name)
			elif self.pay_to == "Territory Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set territory_manager_paid = 1 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set sales_manager_paid = 1 where name = %s """,inv.reference_name)

	def cancel_invoice_payment(self):
		if self.sales_chanel == "Chains":
			if self.pay_to == "Sales Person":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set sales_person_paid = 0 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales supervisor":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set sales_supervisor_paid = 0 where name = %s """,inv.reference_name)
			elif self.pay_to == "Territory Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set territory_manager_paid = 0 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabSales Invoice` set sales_manager_paid = 0 where name = %s """,inv.reference_name)
		elif self.sales_chanel == "Retail":
			if self.pay_to == "Sales Person":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set sales_person_paid = 0 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales supervisor":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set sales_supervisor_paid = 0 where name = %s """,inv.reference_name)
			elif self.pay_to == "Territory Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set territory_manager_paid = 0 where name = %s """,inv.reference_name)
			elif self.pay_to == "Sales Manager":
				for inv in self.commission_details:
					frappe.db.sql("""  update `tabPayment Entry` set sales_manager_paid = 0 where name = %s """,inv.reference_name)

	@frappe.whitelist()
	def make_jv(self):
		company = frappe.db.get_value("Company", frappe.db.get_value("Global Defaults", None, "default_company"),"company_name")
		emplo = frappe.get_value('Sales Person', self.employee, "employee")
		accounts = [
			{
				"account": self.commission_account,
				"debit_in_account_currency": self.commission,
				"party_type": "Employee",
				"party": emplo,
				"cost_center": self.cost_center,
				"exchange_rate": "1"
			},
			{
				"account": self.accrual_account,
				"party_type": "Employee",
				"party": emplo,
				"credit_in_account_currency": self.commission,
				"cost_center": self.cost_center,
				"exchange_rate": "1"
			}
		]
		doc = frappe.get_doc({
			"doctype": "Journal Entry",
			"voucher_type": "Journal Entry",
			"company": company,
			"posting_date": self.from_date,
			"accounts": accounts,
			"cheque_no": self.name,
			"cheque_date": self.from_date,
			"reference_doctype": "Commission Payment",
			"reference_link": self.name,
			"user_remark": _('Accrual Journal Entry for Sales Commission for {0}').format(self.employee),
			"total_debit": self.commission,
			"total_credit": self.commission,
			"remark":  _('Accrual Journal Entry for Sales Commission for {0}').format(self.employee)
		})
		doc.insert()
		doc.submit()

	@frappe.whitelist()

	def get_rates(self):
		data_from_commission_scheduale = frappe.db.sql("""select total_target as total_target,
															tier_1_amount as tier_1_amount,
															tier_2_amount as tier_2_amount,
															tier_3_amount as tier_3_amount,
															tier_1_percent as tier_1_percent,
															tier_2_percent as tier_2_percent,
															tier_3_percent as tier_3_percent
															from `tabCommission Schedule`
															where parent = '{sales_person}'
															and month = '{month}'
															""".format(sales_person = self.employee,month=self.month),as_dict=1)
		for comm in data_from_commission_scheduale:
			self.total_target = comm.total_target
			self.tier_1_amount = comm.tier_1_amount
			self.tier_2_amount = comm.tier_2_amount
			self.tier_3_amount = comm.tier_3_amount
			self.tier_1_percent = comm.tier_1_percent
			self.tier_2_percent = comm.tier_2_percent
			self.tier_3_percent = comm.tier_3_percent




	@frappe.whitelist()
	def commission_calculations(self):
		if self.total_achieved:
			if self.total_achieved <= self.tier_1_amount:
				self.tier_1_commission = self.total_achieved * self.tier_1_percent / 100
				self.tier_2_commission = 0
				self.tier_3_commission = 0
			elif self.total_achieved > self.tier_1_amount and self.total_achieved <= self.tier_3_amount:
				self.tier_1_commission = self.tier_1_amount * self.tier_1_percent / 100
				self.tier_2_commission = (self.total_achieved - self.tier_1_amount) * self.tier_2_percent / 100
				self.tier_3_commission = 0
			elif self.total_achieved >= self.tier_3_amount :
				self.tier_1_commission = self.tier_1_amount * self.tier_1_percent / 100
				self.tier_2_commission = self.tier_2_amount * self.tier_2_percent / 100
				self.tier_3_commission = ( self.total_achieved - self.tier_1_amount - self.tier_2_amount )* self.tier_3_percent / 100
		self.total_payable_commission = self.tier_1_commission + self.tier_2_commission + self.tier_3_commission



		"""
		a = float(self.total_payable)
		b = 3
		for k in self.sales_person_targets:
			#while (b>0):
			if (b == 3) and a > 0 and a >= k.from_amt and a <= k.to_amt:
				k.commission_amount = a * k.rate / 100
				#a -= k.to_amt
			elif (b == 3) and a > 0 and a >= k.from_amt and a > k.to_amt:
				k.commission_amount = k.to_amt * k.rate / 100
				#a -= k.to_amt
			elif (b == 2) and a > 0 and a < k.to_amt and a <= k.to_amt:
				k.commission_amount = (a - k.from_amt) * k.rate / 100
				a -= k.to_amt
			elif (b == 2) and a > 0 and a >= k.from_amt and a > k.to_amt:
				k.commission_amount = (a - k.from_amt) * k.rate / 100
				a -= k.to_amt

			elif (b == 1) and a > 0:
				k.commission_amount = a * k.rate / 100
				a -= k.to_amt
			b -= 1
		"""
			#if a >= float(k.from_amt) and a <= float(k.to_amt):
			#	self.append("sales_person_targets", {
			#	"commission_amount": (a * float(k.rate)/100)
			#	})
