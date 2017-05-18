$('#login').submit(function () {

    email = $("#email").val();
    password = $('#pass').val();
    var missing = false;

    // Empty all messages on button click
    $("#messages").empty();

    if (email == '') {
        $('#email').css('border-color', 'red');
        missing = true;
    }
    if (password == '') {
        $('#pass').css('border-color', 'red');
        missing = true;
    }
    // Prevent form submission if missing fields
    if (missing) {
        $("#login").effect('shake');
        return false;
    } else {
        return true;
    }
});
