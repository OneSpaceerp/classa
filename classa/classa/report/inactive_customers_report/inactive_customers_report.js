// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Inactive Customers Report"] = {
	"filters": [
		{
			fieldname: "days_since_last_invoice",
			label: __("Days Since Last Invoice"),
			fieldtype: "Int",
			reqd: 1,
		},
        {
			fieldname: "sales_person",
			label: __("Sales Person"),
			fieldtype: "Link",
			options: "Sales Person",
		},
        {
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
		},
	]
}