$('#login').submit(function () {

    var email = $('#email');
    var password = $('#password');

    var emailVal = $('#email').val();
    var passwordVal = $('#password').val();

    var error = $("#message");
    var missing = false;

    // Remove the class so that it can be readded in case of errors
    email.removeClass("shake");
    password.removeClass("shake");

    if (emailVal == '') {
        error.html("Email address cannot be empty");
        email.addClass('shake');
        email.css('border-color', 'red');
        missing = true;
    } else if (!emailVal.includes("@")) {
        error.html("Email address must include an @");
        email.addClass('shake');
        email.css('border-color', 'red');
        missing = true;
    }
    if (passwordVal == '') {
        error.html("Password field cannot be empty");
        password.addClass('shake');
        missing = true;
    }
    if (missing) {
        $("#show-errors").show();
        return false;
    } else {
        return true;
    }
});
