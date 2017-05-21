$('#register').submit(function () {

    var name = $("#name");
    var username = $("#username");
    var email = $('#email');
    var pass = $('#password');
    var retype = $('#retype');

    var nameVal = $("#name").val();
    var usernameVal = $("#username").val();
    var emailVal = $('#email').val();
    var passVal = $('#password').val();
    var retypeVal = $('#retype').val();

    // Remove the class so that it can be readded in case of errors
    name.removeClass("shake");
    username.removeClass("shake");
    email.removeClass("shake");
    pass.removeClass("shake");
    retype.removeClass("shake");

    var error = $("#message");

    var missing = false;
    var passwordError = false;

    // Check the name is between 4 and 40 characters
    if (nameVal.length < 4 || nameVal.length > 40) {
        error.html("Name can only be between 4 and 40 characters");
        name.addClass('shake');
        name.css('border-color', 'red');
        missing = true;
    }
    // check username is between 4 and 25
    if (usernameVal.length < 4 || usernameVal.length > 25) {
        error.html("Username can only be between 4 and 25 characters");
        username.addClass('shake');
        username.css('border-color', 'red');
        missing = true;
    }
    // check email contains @ and its betwen 6 and 50 characters
    if (emailVal.length < 6 || emailVal.length > 50 || !emailVal.includes("@")) {
        error.html("Email address invalid");
        email.addClass('shake');
        email.css('border-color', 'red');
        missing = true;
    }
    // check password is between 6 and 100 characters
    if (passVal.length < 6 || passVal.length > 100) {
        error.html("Password must be more than 6 characters, contain at least 1 uppercase letter and 1 number");
        missing = true;
        passwordError = true;
    } else if (retypeVal != passVal){  // check passwords match
        error.html("Passwords don't match");
        passwordError = true;
    }
    if (passwordError) {
        pass.addClass('shake');
        pass.css('border-color', 'red');
        retype.addClass('shake');
        retype.css('border-color', 'red');
    }
    // Add regex validation to password
    var reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;
    if (!reg.test(passVal)) {
        pass.addClass('shake');
        pass.css('border-color', 'red');
        error.html("Password must contain at least 1 uppercase letter and 1 number");
        $("#show-errors").show();
        return false;
    }

    if (missing) {
        $("#show-errors").show();
        return false;
    } else {
        return true;
    }
});
