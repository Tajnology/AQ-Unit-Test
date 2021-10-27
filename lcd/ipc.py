import socketio
import eventlet

import main

def init(temperature : main.RefObj, target_image : main.RefObj):
    sio = socketio.Server()
    app = socketio.WSGIApp(sio)

    @sio.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio.on(main.RECEIVE_IMAGE_EVENT)
    def receive_image(sid, data):
        target_image.set(data['image'])

    @sio.on(main.RECEIVE_TEMPERATURE_EVENT)
    def receive_temperature(sid, data):
        temperature.set(data['temperature'])

    @sio.event
    def disconnect(sid):
        print('disconnect', sid)

    eventlet.wsgi.server(eventlet.listen(('localhost',main.LCD_PORT)),app)
