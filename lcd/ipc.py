import socketio
import eventlet

import main

def init(temperature : main.RefObj, cpu : main.RefObj):
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio.on(main.RECEIVE_AQ_DATA)
    def receive_temperature(sid, data):
        temperature.set(data['temperature'])
        cpu.set(data['cpu'])

    @sio.event
    def disconnect(sid):
        print('disconnect', sid)

    eventlet.wsgi.server(eventlet.listen(('localhost',main.LCD_PORT)),app)
