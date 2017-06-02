// Start the dropzone widget
window.onload = function() {
    Dropzone.options.drop = {
        maxFiles: 1,
        maxFilesize: 2, // MB
        acceptedFiles: "image/jpeg,image/png,image/gif"
    };
};

// When image is clicked open modal
$("#overlay").click(function() {
    console.log("clicked")
    $('#upload').modal('show');
});

$('#profile-form').submit(function( event ) {
    event.preventDefault();
    console.log("Entered")
    var name = $('#name');
    var password = $('#password');
    var retype = $('#retype');

    var nameVal = $('#name').val();
    var passwordVal = $('#password').val();
    var retypeVal = $('#retype').val();

    var error = $("#message");
    var missing = false;
    var passwordError = false;

    // password regex
    var reg = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/;

    // Remove the class so that it can be readded in case of errors
    name.removeClass("shake");
    password.removeClass("shake");
    retype.removeClass("shake");

    if (nameVal == '') {
        error.html("Name cannot be empty");
        name.addClass('shake');
        name.css('border-color', 'red');
        missing = true;
    }
    if (passwordVal == '') {
        error.html("Password field cannot be empty");
        password.addClass('shake');
        missing = true;
    } else if (passVal.length < 6 || passVal.length > 100) {
        // check password is between 6 and 100 characters
        error.html("Password must be more than 6 characters, contain at least 1 uppercase letter and 1 number");
        missing = true;
        passwordError = true;
    } else if (!reg.test(passVal)) {
        // Add regex validation to password
        password.addClass('shake');
        password.css('border-color', 'red');
        error.html("Password must contain at least 1 uppercase letter and 1 number");
        missing = true;
    } else if (retypeVal != passwordVal) { // check passwords match
        error.html("Passwords don't match");
        passwordError = true;
    }

    if (passwordError) {
        password.addClass('shake');
        password.css('border-color', 'red');
        retype.addClass('shake');
        retype.css('border-color', 'red');
    }

    if (missing) {
        $("#show-errors").show();
        return false;
    } else {
        return true;
    }
});
