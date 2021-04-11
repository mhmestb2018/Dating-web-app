from .. import socketio

from flask_socketio import join_room, emit
@socketio.on('join')
def on_join(data):
    emit('notification',  {'data':'Lets dance'})
    #room = data['room']
    #join_room(room)
    #emit('notification', {'Info': "Vous êtes connecté."})
