// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Stock Balances"] = {
	"filters": [
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		}
	]
}
