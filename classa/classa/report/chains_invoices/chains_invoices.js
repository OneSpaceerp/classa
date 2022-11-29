// Copyright (c) 2022, ERPCloud.Systems and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Chains Invoices"] = {
	"filters": [
		/*
		{
			fieldname: "report_based",
			label: __("Report Base"),
			fieldtype: "Select",
			options: ["", "Sales Invoice", "Stock Entry"],
			reqd:1,
			on_change: function() {
				let type = frappe.query_report.get_filter_value('report_based');
				frappe.query_report.toggle_filter_display('st_status', type === 'Stock Entry');
				frappe.query_report.toggle_filter_display('si_status', type === 'Sales Invoice');
				frappe.query_report.set_filter_value('st_status', '');
				frappe.query_report.set_filter_value('si_status', '');
				frappe.query_report.refresh();
			}
		},
		*/
		{
			fieldname: "customer",
			label: __("Customer"),
			fieldtype: "Link",
			options: "Customer",
		},
		{
			fieldname: "customer_group",
			label: __("Customer Group"),
			fieldtype: "Link",
			options: "Customer Group",
		},
		{
			fieldname: "warehouse",
			label: __("Warehouse"),
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			fieldname: "branch",
			label: __("Branch"),
			fieldtype: "Link",
			options: "Branch",
		},
		{
			fieldname: "st_status",
			label: __("Stock Entry Status"),
			fieldtype: "Select",
			options: ["", "Draft", "Submitted"],
		},
		{
			fieldname: "si_status",
			label: __("Sales Invoice Status"),
			fieldtype: "Select",
			options: ["", "Draft", "Submitted"],
		}

	]
};
