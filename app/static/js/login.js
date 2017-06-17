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

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
    data = {"user_id": profile.getId(),
            "email": profile.getEmail(),
            "name": profile.getName(),
            "image_url": profile.getImageUrl()
        }
    $.ajax({
        url : "AJAX_POST_URL",
        type: "POST",
        data : data,
        success: function(data, textStatus, jqXHR) {
            //data - response from server
        },
        error: function (jqXHR, textStatus, errorThrown) {

        }
    }
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function checkLoginState() {
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response);
    });
}
