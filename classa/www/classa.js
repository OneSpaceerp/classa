async function submit() {
    let button = document.getElementById('submit-button');
    button.disabled = true;
    let form = document.querySelector('#customer-form');
    if (!form.checkValidity()) {
        form.reportValidity();
        button.disabled = false;
        return;
    }
    let contact = get_form_data();
    let appointment =  frappe.call({
        method: 'classa.www.classa.create_todo',
        args: {
            'contact': contact,
        },
        callback: (response)=>{
            if (response.message.status == "Unverified") {
                frappe.show_alert("Please check your email to confirm the appointment")
            } else {
                frappe.show_alert("Appointment Created Successfully");
            }
            setTimeout(()=>{
                let redirect_url = "/";
                if (window.appointment_settings.success_redirect_url){
                    redirect_url += window.appointment_settings.success_redirect_url;
                }
                window.location.href = redirect_url;},5000)
        },
        error: (err)=>{
            frappe.show_alert("Something went wrong please try again");
            button.disabled = false;
        }
    });
}

function get_form_data() {
    contact = {};
    let inputs = ['name', 'skype', 'number', 'notes', 'email'];
    //inputs.forEach((id) => contact[id] = document.getElementById(`customer_${id}`).value)
    return contact
}