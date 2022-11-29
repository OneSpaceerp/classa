from . import __version__ as app_version

app_name = "classa"
app_title = "Classa"
app_publisher = "ERPCloud.Systems"
app_description = "classa Customizations "
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@erpcloud.systems"
app_license = "MIT"



doc_events = {
"Quotation": {
	"onload": "classa.event_triggers.quot_onload",
	"before_validate": "classa.event_triggers.quot_before_validate",
	"validate": "classa.event_triggers.quot_validate",
	"on_submit": "classa.event_triggers.quot_on_submit",
	"on_cancel": "classa.event_triggers.quot_on_cancel",
	"on_update_after_submit": "classa.event_triggers.quot_on_update_after_submit",
	"before_save": "classa.event_triggers.quot_before_save",
	"before_cancel": "classa.event_triggers.quot_before_cancel",
	"on_update": "classa.event_triggers.quot_on_update",
},
	"Sales Invoice": {
	"after_insert": "classa.permission.share_sin",
	"onload": "classa.event_triggers.siv_onload",
	"before_validate": "classa.event_triggers.siv_before_validate",
	"validate": "classa.event_triggers.siv_validate",
	"on_submit": "classa.event_triggers.siv_on_submit",
	"on_cancel": "classa.event_triggers.siv_on_cancel",
	"on_update_after_submit": "classa.event_triggers.siv_on_update_after_submit",
	"before_save": "classa.event_triggers.siv_before_save",
	"before_cancel": "classa.event_triggers.siv_before_cancel",
	"on_update": "classa.event_triggers.siv_on_update",
},
	"Sales Order": {
		"after_insert": "classa.permission.share_so",
		"onload": "classa.event_triggers.so_onload",
		"before_validate": "classa.event_triggers.so_before_validate",
		"validate": "classa.event_triggers.so_validate",
		"on_submit": "classa.event_triggers.so_on_submit",
		"on_cancel": "classa.event_triggers.so_on_cancel",
		"on_update_after_submit": "classa.event_triggers.so_on_update_after_submit",
		"before_save": "classa.event_triggers.so_before_save",
		"before_cancel": "classa.event_triggers.so_before_cancel",
		"on_update": "classa.event_triggers.so_on_update",

},
	"Material Request": {
		"after_insert": "classa.permission.share_mr",
		"onload": "classa.event_triggers.mr_onload",
		"before_validate": "classa.event_triggers.mr_before_validate",
		"validate": "classa.event_triggers.mr_validate",
		"on_submit": "classa.event_triggers.mr_on_submit",
		"on_cancel": "classa.event_triggers.mr_on_cancel",
		"on_update_after_submit": "classa.event_triggers.mr_on_update_after_submit",
		"before_save": "classa.event_triggers.mr_before_save",
		"before_cancel": "classa.event_triggers.mr_before_cancel",
		"on_update": "classa.event_triggers.mr_on_update",
},
	"Stock Entry": {
		"after_insert": "classa.permission.share_se",
		"onload": "classa.event_triggers.ste_onload",
		"before_validate": "classa.event_triggers.ste_before_validate",
		"validate": "classa.event_triggers.ste_validate",
		"on_submit": "classa.event_triggers.ste_on_submit",
		"on_cancel": "classa.event_triggers.ste_on_cancel",
		"on_update_after_submit": "classa.event_triggers.ste_on_update_after_submit",
		"before_save": "classa.event_triggers.ste_before_save",
		"before_cancel": "classa.event_triggers.ste_before_cancel",
		"on_update": "classa.event_triggers.ste_on_update",
},
	"Delivery Note": {
		"after_insert": "classa.permission.share_dn",
		"onload": "classa.event_triggers.dn_onload",
		"before_validate": "classa.event_triggers.dn_before_validate",
		"validate": "classa.event_triggers.dn_validate",
		"on_submit": "classa.event_triggers.dn_on_submit",
		"on_cancel": "classa.event_triggers.dn_on_cancel",
		"on_update_after_submit": "classa.event_triggers.dn_on_update_after_submit",
		"before_save": "classa.event_triggers.dn_before_save",
		"before_cancel": "classa.event_triggers.dn_before_cancel",
		"on_update": "classa.event_triggers.dn_on_update",
},
	"Purchase Order": {
		"after_insert": "classa.permission.share_po",
		"onload": "classa.event_triggers.po_onload",
		"before_validate": "classa.event_triggers.po_before_validate",
		"validate": "classa.event_triggers.po_validate",
		"on_submit": "classa.event_triggers.po_on_submit",
		"on_cancel": "classa.event_triggers.po_on_cancel",
		"on_update_after_submit": "classa.event_triggers.po_on_update_after_submit",
		"before_save": "classa.event_triggers.po_before_save",
		"before_cancel": "classa.event_triggers.po_before_cancel",
		"on_update": "classa.event_triggers.po_on_update",
},
	"Purchase Receipt": {
		"after_insert": "classa.permission.share_pr",
		"onload": "classa.event_triggers.pr_onload",
		"before_validate": "classa.event_triggers.pr_before_validate",
		"validate": "classa.event_triggers.pr_validate",
		"on_submit": "classa.event_triggers.pr_on_submit",
		"on_cancel": "classa.event_triggers.pr_on_cancel",
		"on_update_after_submit": "classa.event_triggers.pr_on_update_after_submit",
		"before_save": "classa.event_triggers.pr_before_save",
		"before_cancel": "classa.event_triggers.pr_before_cancel",
		"on_update": "classa.event_triggers.pr_on_update",
},
	"Purchase Invoice": {
		"onload": "classa.event_triggers.piv_onload",
		"before_validate": "classa.event_triggers.piv_before_validate",
		"validate": "classa.event_triggers.piv_validate",
		"on_submit": "classa.event_triggers.piv_on_submit",
		"on_cancel": "classa.event_triggers.piv_on_cancel",
		"on_update_after_submit": "classa.event_triggers.piv_on_update_after_submit",
		"before_save": "classa.event_triggers.piv_before_save",
		"before_cancel": "classa.event_triggers.piv_before_cancel",
		"on_update": "classa.event_triggers.piv_on_update",
},
	"Payment Entry": {
		"before_insert": "classa.event_triggers.pe_before_insert",
		"after_insert": "classa.permission.share_pe",
		"onload": "classa.event_triggers.pe_onload",
		"before_validate": "classa.event_triggers.pe_before_validate",
		"validate": "classa.event_triggers.pe_validate",
		"on_submit": "classa.event_triggers.pe_on_submit",
		"on_cancel": "classa.event_triggers.pe_on_cancel",
		"on_update_after_submit": "classa.event_triggers.pe_on_update_after_submit",
		"before_save": "classa.event_triggers.pe_before_save",
		"before_cancel": "classa.event_triggers.pe_before_cancel",
		"on_update": "classa.event_triggers.pe_on_update",
},
	"Blanket Order": {
		"onload": "classa.event_triggers.blank_onload",
		"before_validate": "classa.event_triggers.blank_before_validate",
		"validate": "classa.event_triggers.blank_validate",
		"on_submit": "classa.event_triggers.blank_on_submit",
		"on_cancel": "classa.event_triggers.blank_on_cancel",
		"on_update_after_submit": "classa.event_triggers.blank_on_update_after_submit",
		"before_save": "classa.event_triggers.blank_before_save",
		"before_cancel": "classa.event_triggers.blank_before_cancel",
		"on_update": "classa.event_triggers.blank_on_update",
},
	"Expense Claim": {
		"onload": "classa.event_triggers.excl_onload",
		"before_validate": "classa.event_triggers.excl_before_validate",
		"validate": "classa.event_triggers.excl_validate",
		"on_submit": "classa.event_triggers.excl_on_submit",
		"on_cancel": "classa.event_triggers.excl_on_cancel",
		"on_update_after_submit": "classa.event_triggers.excl_on_update_after_submit",
		"before_save": "classa.event_triggers.excl_before_save",
		"before_cancel": "classa.event_triggers.excl_before_cancel",
		"on_update": "classa.event_triggers.excl_on_update",
},
"Employee Advance": {
		"onload": "classa.event_triggers.emad_onload",
		"before_validate": "classa.event_triggers.emad_before_validate",
		"validate": "classa.event_triggers.emad_validate",
		"on_submit": "classa.event_triggers.emad_on_submit",
		"on_cancel": "classa.event_triggers.emad_on_cancel",
		"on_update_after_submit": "classa.event_triggers.emad_on_update_after_submit",
		"before_save": "classa.event_triggers.emad_before_save",
		"before_cancel": "classa.event_triggers.emad_before_cancel",
		"on_update": "classa.event_triggers.emad_on_update",
},
"Loan": {
		"onload": "classa.event_triggers.loan_onload",
		"before_validate": "classa.event_triggers.loan_before_validate",
		"validate": "classa.event_triggers.loan_validate",
		"on_submit": "classa.event_triggers.loan_on_submit",
		"on_cancel": "classa.event_triggers.loan_on_cancel",
		"on_update_after_submit": "classa.event_triggers.loan_on_update_after_submit",
		"before_save": "classa.event_triggers.loan_before_save",
		"before_cancel": "classa.event_triggers.loan_before_cancel",
		"on_update": "classa.event_triggers.loan_on_update",
},
}

scheduler_events = {
	"all": [
		"classa.functions.all_event",
		"erpnext.stock.doctype.repost_item_valuation.repost_item_valuation.repost_entries"
	],
	"hourly": [
		"classa.functions.hourly_event"
	],
}



# Includes in <head>
# ------------------
# include js, css files in header of desk.html
# app_include_css = "/assets/classa/css/classa.css"
# app_include_js = "/assets/classa/js/classa.js"

# include js, css files in header of web template
# web_include_css = "/assets/classa/css/classa.css"
# web_include_js = "/assets/classa/js/classa.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "classa/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "classa.install.before_install"
# after_install = "classa.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "classa.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"classa.tasks.all"
# 	],
# 	"daily": [
# 		"classa.tasks.daily"
# 	],
# 	"hourly": [
# 		"classa.tasks.hourly"
# 	],
# 	"weekly": [
# 		"classa.tasks.weekly"
# 	]
# 	"monthly": [
# 		"classa.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "classa.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "classa.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "classa.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"classa.auth.validate"
# ]

