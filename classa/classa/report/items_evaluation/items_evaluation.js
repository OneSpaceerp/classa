// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Items Evaluation"] = {
	"filters": [
		{
			fieldname: "item_code",
			label: __("Item Code"),
			fieldtype: "Link",
			options: "Item",
		},
		{
			fieldname: "item_group",
			label: __("Item Group"),
			fieldtype: "Link",
			options: "Item Group",
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname:"to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.get_today(),
		},
		{
			fieldname: "tax_type",
			label: __("Tax Type"),
			fieldtype: "Select",
			options: ["Commercial", "Taxable"],
		},
		{
			fieldname: "sales_invoice",
			label: __("Sales Invoice"),
			fieldtype: "Link",
			options: "Sales Invoice",
		},
        {
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "sales_person",
			label: __("Sales Person"),
			fieldtype: "Link",
			options: "Sales Person",
		},
        {
			fieldname: "territory",
			label: __("Territory"),
			fieldtype: "Link",
			options: "Territory",
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "is_return",
			label: __("Return"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_item",
			label: __("Group By Item"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_customer",
			label: __("Group By Customer"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_customer_group",
			label: __("Group By Customer Group"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_sales_person",
			label: __("Group By Sales Person"),
			fieldtype: "Check",
		},
		{
			fieldname: "group_by_branch",
			label: __("Group By Branch"),
			fieldtype: "Check",
		},
	]
}
