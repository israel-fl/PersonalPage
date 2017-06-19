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

function onGoogleSignin(googleUser) {
    var profile = googleUser.getBasicProfile();
    console.log('ID: ' + profile.getId()); // Do not send to your backend! Use an ID token instead.
    console.log('Name: ' + profile.getName());
    console.log('Image URL: ' + profile.getImageUrl());
    console.log('Email: ' + profile.getEmail()); // This is null if the 'email' scope is not present.
    $("#google-id").val(profile.getId());
    $("#social-email").val(profile.getEmail());
    $("#social-name").val(profile.getName());
    $("#social-image").val(profile.getImageUrl());
    console.log("submitting");
    // Submit the form now that the values are set
    $( "#social-form" ).submit();
}

// This function is called when someone finishes with the Login
// Button.  See the onlogin handler attached to it in the sample
// code below.
function onFBSignin() {
    FB.getLoginStatus(function(response) {
        if (response.status === 'connected') {
            // Logged into your app and Facebook.
            console.log("connected");
            FB.api('/me', { fields: 'name, email' }, function(response) {
                console.log(response.email);
                console.log(response.name);
                console.log(response.id);
                $("#fb-id").val(response.id);
                $("#social-email").val(response.email);
                $("#social-name").val(response.name);
                // Make the next api call when the previous one has finished
                FB.api('/me/?fields=picture', function(response) {
                    $("#social-image").val(response.picture.data.url);
                    // Submit the form when all calls have finished
                    $( "#social-form" ).submit();
                });
            });

        } else {
          // The person is not logged into your app or we are unable to tell.
            console.log(response.status);
        }
    });
}
