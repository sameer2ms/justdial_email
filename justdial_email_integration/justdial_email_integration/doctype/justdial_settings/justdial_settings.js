// Copyright (c) 2023, New Indictrans Tech Pvt Ltd and contributors
// For license information, please see license.txt

frappe.ui.form.on('Justdial Settings', {
	// refresh: function(frm) {

	// }

	get_now: function(frm){
		console.log(" this is button click",frm)
		frappe.call({
            method: "justdial_email_integration.justdial_email_integration.doctype.justdial_settings.justdial_settings.jd_get_emails",
            callback: function(r) {
                // code snippet
                console.log(r.message)
                if(r.message) {
                   console.log(" this is success")
                }
                
            }
        })
	}
});
