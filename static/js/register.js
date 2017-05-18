$('#register').submit(function () {

    name = $("#name").val();
    email = $('#email').val();
    pass = $('#pass').val();
    retype = $('#retype').val();
    var missing = false;

    var holder = document.getElementById("messages");
    var error = document.createElement("li");

     // Empty all messages on button click
    $("#messages").empty();

    if (name == '') {
        $("#name").css('border-color', 'red');
        $("#name").effect('shake');
        missing = true;
    }
    if (email == '') {
        $('#email').css('border-color', 'red');
        $('#email').effect('shake');
        missing = true;
    }
    if (pass == '') {
        $('#pass').css('border-color', 'red');
        $('#pass').effect('shake');
        missing = true;
    }
    if (retype == '') {
        $('#retype').css('border-color', 'red');
        $('#retype').effect('shake');
        missing = true;
    }
    if (retype != pass) {
        error.setAttribute("value", "Passwords do not much")
        $('#pass').css('border-color', 'red');
        $('#retype').css('border-color', 'red');
        $('#pass').effect('shake');
        $('#retype').effect('shake');
        missing = true;
    }

    if (missing) {
        return false;
    } else {
        return true;
    }
});
