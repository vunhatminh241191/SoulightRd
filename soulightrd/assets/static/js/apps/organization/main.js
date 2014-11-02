jQuery(document).ready(function($){
    $('#signup_form').validate({
        rules:{
            'name':{
                required: true,
                minlength: 2,
                pattern: /^[A-Z]{2}[0-9]{5}$/
            },
            'description': {
                required: true,
                minlength: 20,
                maxlength: 500
            },
            'phone': {
                pattern: /^[0-9]$/,
                minlength: 10,
                maxlength: 12,
            },
            'email':{
                pattern: /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i
            }
        },
        messages:{
            'name':{
                minlength: "Please make your organization name longer than 2 characters",
                pattern: "The organization name can only consist of alphabetical and number"
            },
            'description': {
                minlength: "Can you tell us more about your organization",
                maxlength: "Please descripting briefly"
            },
            'phone': {
                pattern: "Phone field only accepts integer number from 1 to 9",
                minlength: "Please give us a right phone number",
                maxlength: "Please give us a right phone number",                     
            },
            'email': {
                pattern: "Please give us a right email"
            }
        },
        submitHandler: function (form) { // for demo
            alert('valid form submitted'); // for demo
            return false; // for demo
        }

    });
});