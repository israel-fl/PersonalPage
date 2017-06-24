from flask_socketio import emit
from app import socketio

## SOCKETS ##

@socketio.on('message', namespace='/test')
def handle_message(message):
    emit('MESSAGE', {'data': message['data'], 'user': 'SAMMY', 'position': 'left'}, broadcast=True)


@socketio.on('broadcast', namespace='/test')
def test_message(message):
    emit('MESSAGE', {'data': message['data'], 'user': "visitor", 'position': 'right'}, broadcast=True)
