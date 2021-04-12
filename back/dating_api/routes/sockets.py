from .. import socketio
from flask import render_template

from flask_socketio import join_room, emit
@socketio.on('connect')
def on_connect():
    print("User Connected")
    emit('notification', {'Info': "Vous êtes connecté."})

@socketio.on('test')
def on_join(data):
    print("Room joined")
    room = data['room']
    join_room(room)
    emit('notification',  {'Info':'Vous avez rejoint la Room'})
