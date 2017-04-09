$(document).ready(function(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('MESSAGE', function(msg) {
        var clear = document.createElement("div");
        var body = document.createElement("div");
        var message = document.createElement("p");
        var bubbleClass = 'from-me';

        $('#btn-input').val('');
        $('#btn-input2').val('');

        clear.setAttribute("class", "clear-chat");


        if (msg.position === 'left') {
            bubbleClass = 'from-them';
        }
        body.setAttribute("class", bubbleClass);
        message.innerHTML = msg.data;
        body.append(message);
        $(clear).appendTo('#chatbox, #chatbox2');
        $(body).appendTo('#chatbox, #chatbox2');
        $('#holder').scrollTop($('#holder')[0].scrollHeight);
        $('#holder2').scrollTop($('#holder2')[0].scrollHeight);

    });
    $('#btn-chat').click(function(event) {
        socket.emit('message', {data: $('#btn-input').val()});
        return false;
    });
    $('#btn-chat2').click(function(event) {
        socket.emit('broadcast', {data: $('#btn-input2').val()});
        return false;
    });
});


