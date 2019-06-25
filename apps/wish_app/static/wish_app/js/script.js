$(document).ready(function(){
    $('#email_input').keyup(function(){
        var data = $("#registration_form").serialize();
        $.ajax({
            method: "POST",
            url: "/email",
            data: data
        })
        .done(function(res){
            $('#error_message').html(res)
        })
    });
})

function validateForm(){
    var error = false;
    var error_message = "<ul class='messages'>";
    var first_name = document.forms["registration_form"]["first_name_input"].value;
    if (first_name == "" || first_name.length < 2){
        error_message += "<li> First name should be a minimum of 2 characters</li>"
        error = true; 
    }
    var last_name = document.forms["registration_form"]["last_name_input"].value;
    if (last_name == "" || last_name.length < 2){
        error_message += "<li> Last name should be a minimum of 2 characters</li>"
        error = true; 
    }
    var email = document.forms["registration_form"]["email_input"].value;
    if (email == ""){
        error_message += "<li> Email is required for registration</li>"
        error = true; 
    }
    var re = /[^@]+@[^@]+\.[^@]+/
    if (!email.match(re)){
        error_message += "<li> Email format is not valid</li>";
        error = true; 
    }
    var password = document.forms["registration_form"]["password_input"].value;
    if (password == "" || password.length < 8){
        error_message += "<li> Password should be a minimum of 8 characters</li>"
        error = true; 
    }
    var password_confirm = document.forms["registration_form"]["password_confirmation_input"].value;
    if (password_confirm == "" || password_confirm.length < 8 || password != password_confirm){
        error_message += "<li>Password does not match</li>"
        error = true; 
    }
    error_message += "</ul>";
    if (error) {
        document.getElementById("error_message").innerHTML = error_message;
        return false;
    } else{
        return true;
    }
}