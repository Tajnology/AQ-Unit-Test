import socketio

sio = socketio.Client()

@sio.event
def connect():
    print("I'm connected!")

sio.connect('http://172.30.0.1:5000')

print('my sid is', sio.sid)