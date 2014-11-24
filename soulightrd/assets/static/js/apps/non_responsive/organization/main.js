/* CLICK CANCEL BUTTON */
$(function() {
    $("#button-id-cancel").click(function() {
        window.location.href = "/";
    })
})
/*****************/

/* FORM VALIDATION */
$(document).ready(function($){
    $('#create_organization_form').validate({
        errorPlacement: function(error, element) {
            $( element ).closest('.controls').prepend(error);
        },
        rules:{
            'name':{
                required: true,
                minlength: 2,
            },
            'description': {
                required: true,
                minlength: 20,
                maxlength: 500
            },
            'phone': {
                required: true,
                intlphone: true,
            },
            'email':{
                required: true,
                pattern: /^\b[A-Z0-9._%-]+@[A-Z0-9.-]+\.[A-Z]{2,4}\b$/i
            },
            'address': {
                required: true
            },
            'website': {
                required: false
            },
            'city': {
                required: true
            }
        },
        messages:{
            'name':{
                required: "Please enter your organization",
                minlength: "Please make your organization name longer than 2 characters",
                pattern: "The organization name can only consist of alphabetical and number"
            },
            'description': {
                required: "Please descripting your organization",
                minlength: "Can you tell us more about your organization",
                maxlength: "Please descripting briefly"
            },
            'phone': {
                required: "Please give us your organization phone number to contact",              
            },
            'email': {
                required: "Please give us your organization email",
                pattern: "Please give us a right email"
            },
            'address': {
                required: "Please give us your organization address"
            },
            'website': {
                required: "Please give us your organization website"
            }
        },
    });
});
/********************/