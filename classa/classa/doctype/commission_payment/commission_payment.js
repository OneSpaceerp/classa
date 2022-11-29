// Copyright (c) 2021, ERP Cloud Systems and contributors
// For license information, please see license.txt

frappe.ui.form.on('Commission Payment',  'validate',  function(frm, cdt, cdn) {
   // if(frm.doc.__islocal ? 0 : 1){
        var dw = locals[cdt][cdn];
        var total = 0;
        frm.doc.commission_details.forEach(function(dw) { total += dw.net_total; });
        frm.set_value("total_achieved", total);
        refresh_field("total_achieved");
   // }

});
/*
frappe.ui.form.on('Commission Payment', {


///copy tables from process_difination

employee: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "get_commission_details",
				callback: function(r) {
					refresh_field("sales_person_targets");
				}
			});

	}

})

frappe.ui.form.on("Commission Payment", "validate", function(frm, cdt, cdn) {
	$.each(frm.doc.sales_person_targets || [], function(i, d) {
	    if(cur_frm.doc.total_payable >= d.from_amt && cur_frm.doc.total_payable <= d.to_amt ){
	        frm.set_value("tier", d.tier);
	        frm.set_value("commission_rate", d.rate);
	        var total_comm = cur_frm.doc.total_payable * d.rate/100
	        frm.set_value("commission",total_comm);
            refresh_field("tier");
            refresh_field("rate");
            refresh_field("commission");
	    }

	});
});
*/