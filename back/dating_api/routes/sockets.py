from .. import socketio
from flask import render_template

from flask_socketio import join_room, emit
@socketio.on('connect')
def on_connect():
    print("User Connected")
    emit('info', {'Info': "Vous êtes connecté."})

@socketio.on('join')
def on_join(data):
    print("Room joined")
    room = data['room']
    join_room(room)
    socketio.emit('info',  {'Info':'Vous avez rejoint la Room'}, room=room)
