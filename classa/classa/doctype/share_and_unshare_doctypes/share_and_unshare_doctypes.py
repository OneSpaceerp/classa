# Copyright (c) 2021, ERPCloud.Systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import auth
import datetime
import json, ast
from frappe.model.document import Document


class ShareAndUnshareDoctypes(Document):
	@frappe.whitelist()
	def on_submit(self):
		for x in self.shared_table:
			if self.action == "Share Address" or self.action == "Share Customers & Addresses":
				new_doc = frappe.new_doc('DocShare')
				new_doc.user = self.user
				new_doc.share_doctype = "Address"
				new_doc.share_name = x.address
				new_doc.read = 1
				new_doc.write = 0
				new_doc.share = 0
				new_doc.everyone = 0
				new_doc.insert()

			if self.action == "Unshare Address" or self.action == "Unshare Customers & Addresses":
				old_doc = frappe.db.get_list('DocShare', filters=[{'share_name': ['=', x.address]}, {'user': ['=', self.user]}], fields=['name'])
				for y in old_doc:
					frappe.delete_doc("DocShare", y.name)


		for y in self.shared_table_2:
			if self.action == "Share Customer" or self.action == "Share Customers & Addresses":
				new_doc = frappe.new_doc('DocShare')
				new_doc.user = self.user
				new_doc.share_doctype = "Customer"
				new_doc.share_name = y.customer
				new_doc.read = 1
				new_doc.write = 0
				new_doc.share = 0
				new_doc.everyone = 0
				new_doc.insert()

			if self.action == "Unshare Customer" or self.action == "Unshare Customers & Addresses":
				old_doc = frappe.db.get_list('DocShare', filters=[{'share_name': ['=', y.customer]}, {'user': ['=', self.user]}], fields=['name'])
				for y in old_doc:
					frappe.delete_doc("DocShare", y.name)

		if self.action == "Migrate Shared Customers & Addresses":
			shared_cust = frappe.db.sql(""" select share_name, name from `tabDocShare` where `tabDocShare`.share_doctype = 'Customer' and `tabDocShare`.user = '{user}'
		 							 """.format(user=self.user), as_dict=1)

			for q in shared_cust:
				new_doc2 = frappe.new_doc('DocShare')
				new_doc2.user = self.user2
				new_doc2.share_doctype = "Customer"
				new_doc2.share_name = q.share_name
				new_doc2.read = 1
				new_doc2.write = 0
				new_doc2.share = 0
				new_doc2.everyone = 0
				new_doc2.insert()

				frappe.delete_doc("DocShare", q.name)

			shared_add = frappe.db.sql(""" select share_name, name from `tabDocShare` where `tabDocShare`.share_doctype = 'Address' and `tabDocShare`.user = '{user}'
									 """.format(user=self.user), as_dict=1)

			for w in shared_add:
				new_doc2 = frappe.new_doc('DocShare')
				new_doc2.user = self.user2
				new_doc2.share_doctype = "Address"
				new_doc2.share_name = w.share_name
				new_doc2.read = 1
				new_doc2.write = 0
				new_doc2.share = 0
				new_doc2.everyone = 0
				new_doc2.insert()

				frappe.delete_doc("DocShare", w.name)

	@frappe.whitelist()
	def on_cancel(self):
		for x in self.shared_table:
			if self.action == "Share Address" or self.action == "Share Customers & Addresses":
				old_doc = frappe.db.get_list('DocShare', filters=[{'share_name': ['=', x.address]}, {'user': ['=', self.user]}], fields=['name'])
				for y in old_doc:
					frappe.delete_doc("DocShare", y.name)

			if self.action == "Unshare Address" or self.action == "Unshare Customers & Addresses":
				new_doc = frappe.new_doc('DocShare')
				new_doc.user = self.user
				new_doc.share_doctype = "Address"
				new_doc.share_name = x.address
				new_doc.read = 1
				new_doc.write = 0
				new_doc.share = 0
				new_doc.everyone = 0
				new_doc.insert()

		for w in self.shared_table or self.action == "Unshare Customers & Addresses":
			if self.action == "Share Customer" or self.action == "Share Customers & Addresses":
				old_doc = frappe.db.get_list('DocShare', filters=[{'share_name': ['=', w.customer]}, {'user': ['=', self.user]}], fields=['name'])
				for z in old_doc:
					frappe.delete_doc("DocShare", z.name)

			if self.action == "Unshare Customer":
				new_doc = frappe.new_doc('DocShare')
				new_doc.user = self.user
				new_doc.share_doctype = "Customer"
				new_doc.share_name = w.customer
				new_doc.read = 1
				new_doc.write = 0
				new_doc.share = 0
				new_doc.everyone = 0
				new_doc.insert()

	@frappe.whitelist()
	def get_shared_addresses(self):
		if self.action == "Unshare Address" or self.action == "Unshare Customers & Addresses":
			shared_names = frappe.db.sql(""" select share_name from `tabDocShare` where `tabDocShare`.share_doctype = 'Address' and `tabDocShare`.user = '{user}'
			 							 """.format(user=self.user), as_dict=1)

			for x in shared_names:
				y = self.append("shared_table", {})
				y.address = x.share_name

	@frappe.whitelist()
	def get_shared_customers(self):
		if self.action == "Unshare Customer" or self.action == "Unshare Customers & Addresses":
			shared_names = frappe.db.sql(""" select share_name from `tabDocShare` where `tabDocShare`.share_doctype = 'Customer' and `tabDocShare`.user = '{user}'
			 							 """.format(user=self.user), as_dict=1)

			for x in shared_names:
				y = self.append("shared_table_2", {})
				y.customer = x.share_name

	@frappe.whitelist()
	def get_customer_addresses(self):
		if self.action == "Share Customers & Addresses" or self.action == "Unshare Customers & Addresses":
			for d in self.shared_table_2:
				addresses = frappe.db.get_list('Dynamic Link', filters={'link_name': d.customer},
											   fields=['parent'])
				for c in addresses:
					y = self.append("shared_table", {})
					y.address = c.parent
