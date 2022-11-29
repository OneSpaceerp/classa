// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Items Per Item Group Evaluation"] = {
	"filters": [
        {
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
			reqd: 1,
		},
		{
			fieldname: "price_list",
			label: __("Price List"),
			fieldtype: "Link",
			options: "Price List",
			reqd: 1,
		},
	]
}