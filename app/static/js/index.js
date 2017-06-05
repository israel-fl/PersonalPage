$(document).ready(function() {
    var socket = io.connect('https://' + document.domain + ':' + location.port + '/test', { secure: true });
    socket.on('MESSAGE', function(msg) {
        var clear = document.createElement("div");
        var body = document.createElement("div");
        var message = document.createElement("p");
        var bubbleClass = 'from-me';
        $('#btn-input').val('');
        $('#btn-input2').val('');
        clear.setAttribute("class", "clear-chat");
        if (msg.position === 'left') { bubbleClass = 'from-them'; }
        body.setAttribute("class", bubbleClass);
        message.innerHTML = msg.data;
        body.append(message);
        $(clear).appendTo('#chatbox, #chatbox2');
        $(body).appendTo('#chatbox, #chatbox2');
        $('#holder').scrollTop($('#holder')[0].scrollHeight);
        $('#holder2').scrollTop($('#holder2')[0].scrollHeight);
    });
    $('#btn-chat').click(function(event) {
        socket.emit('message', { data: $('#btn-input').val() });
        return false;
    });
    $('#btn-chat2').click(function(event) {
        socket.emit('broadcast', { data: $('#btn-input2').val() });
        return false;
    });
});

$('#contactForm').submit(function( event ) {
            var name = $('#name');
            var email = $('#email');
            var message = $('#message');

            var nameVal = $('#name').val();
            var emailVal = $('#email').val();
            var messageVal = $('#message').val();

            var error = $("#message");
            var missing = false;

            // Remove the class so that it can be readded in case of errors
            title.removeClass("shake");
            comment.removeClass("shake");

            if (nameVal == '') {
                error.html("You must enter your name");
                title.addClass('shake');
                title.css('border-color', 'red');
                missing = true;
            }
            if (emailVal == '') {
                error.html("Please enter an email address");
                comment.addClass('shake');
                comment.css('border-color', 'red');
                missing = true;
            }
            if (messageVal == '') {
                error.html("Message cannot be empty");
                comment.addClass('shake');
                comment.css('border-color', 'red');
                missing = true;
            }

            if (missing) {
                $("#show-errors").show();
                return false;
            } else {
                return true;
            }
        });
