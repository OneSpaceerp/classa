// Copyright (c) 2016, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Selling Report"] = {
	"filters": [
		{
			"fieldname": "type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": ["Chains","Large Groceries","Retail"],
			"default": "Chains",
			"reqd": 1
		},
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today()),
			"reqd": 1
		},
	]
}
