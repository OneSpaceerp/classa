import frappe
def get_context(context):
    context.users = frappe.get_list("User", fields=["first_name", "last_name"])
    context.mode_of_payments = frappe.get_list("Mode of Payment", fields=['name'])

@frappe.whitelist(allow_guest=True)
def create_todo(contact):
	todo = frappe.new_doc('ToDo')
	todo.description =contact.get('description', None)
	todo.insert()
	return todo