// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Inactive Items"] = {
	"filters": [
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
			reqd: 0,
		},
		{
			fieldname: "item",
			label: __("Item"),
			fieldtype: "Link",
			options: "Item"
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group"
		},
		{
			fieldname: "based_on",
			label: __("Based On"),
			fieldtype: "Select",
			options: "Sales Order\nSales Invoice",
			default: "Sales Invoice",
			read_only: 1,
			hidden: 1
		},
		{
			fieldname: "days",
			label: __("Days Since Last order"),
			fieldtype: "Select",
			options: [30, 60, 90],
			default: 30
		},
	]
};
