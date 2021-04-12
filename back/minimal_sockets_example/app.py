from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

@app.route("/test", methods=["GET"])
def test_test():
    print("Test")
    return render_template('test.html')

@socketio.on('connect')
def test_connect():
    print("YihaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaAA")
    emit('notification',  {'data':'Lets dance'})

@socketio.on('message')
def test_message(event_name, data):
    print(f"FAIL: received {event_name} as a MESSAGE: {data}")
    emit('notification',  {'data':'Lets dance'})

@socketio.on("my event")
def test_event(data):
    print("BOOM", data)
    emit('notification',  {'data':'event received'})

if __name__ == '__main__':
    socketio.run(app, debug=True)