// Copyright (c) 2021, ERPCloud.Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Share And Unshare Doctypes', {
    get_shared_addresses: function(frm) {
            cur_frm.clear_table("shared_table");
			frappe.call({
				doc: frm.doc,
				method: "get_shared_addresses",
				    callback: function(r) {
                    refresh_field("shared_table");
                    cur_frm.save('Save');
                }
			});
	}
})

frappe.ui.form.on('Share And Unshare Doctypes', {
    get_shared_customers: function(frm) {
            cur_frm.clear_table("shared_table_2");
			frappe.call({
				doc: frm.doc,
				method: "get_shared_customers",
				    callback: function(r) {
                    refresh_field("shared_table_2");
                    cur_frm.save('Save');
                }
			});
	}
})

frappe.ui.form.on('Share And Unshare Doctypes', {
    get_customer_addresses: function(frm) {
            cur_frm.clear_table("shared_table");
			frappe.call({
				doc: frm.doc,
				method: "get_customer_addresses",
				    callback: function(r) {
                    refresh_field("shared_table");
                    cur_frm.save('Save');
                }
			});
	}
})
