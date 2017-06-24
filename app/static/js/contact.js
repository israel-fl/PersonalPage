function verifyCaptcha() {
    var grecaptcha = $("#g-recaptcha-response").val();
    if (grecaptcha.length == 0){
        alert("Please fill the captcha first!");
        return false;
    } else {
        return true;
    }
}

$('#contactForm').submit(function( event ) {
    var name = $('#name');
    var email = $('#email');
    var message = $('#content');
    var nameVal = $('#name').val();
    var emailVal = $('#email').val();
    var messageVal = $('#content').val();
    var error = $("#message");
    var missing = false;
    // Remove the class so that it can be readded in case of errors
    name.removeClass("shake");
    email.removeClass("shake");
    message.removeClass("shake");
    if (nameVal == '') {
        error.html("You must enter your name");
        name.addClass('shake');
        name.css('border-color', 'red');
        missing = true;
    }
    if (emailVal == '') {
        error.html("Please enter an email address");
        email.addClass('shake');
        email.css('border-color', 'red');
        missing = true;
    }
    if (messageVal == '') {
        error.html("Message cannot be empty");
        message.addClass('shake');
        message.css('border-color', 'red');
        missing = true;
    }
    if (missing) {
        $("#show-errors").show();
        return false;
    } else {
        return true;
    }
});
