// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Cash Payments Report"] = {
	"filters": [
		{
			fieldname: "mode_of_payment",
			label: __("Mode Of Payment"),
			fieldtype: "Link",
			options: "Mode of Payment",
			reqd: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today()
		},
	]
}
