import socketio
import eventlet
import json

import main

sio_send_connected = False
sio_send = None

def init():
    sio_recv = socketio.Server()
    app = socketio.WSGIApp(sio_recv)

    @sio_recv.event
    def connect(sid, environ, auth):
        print('connect', sid)

    @sio_recv.on(main.AQ_DATA_EVENT)
    def receive_aq_data(sid, data):
        print('Transmission program received data')
        print(data)
        
        # msg_gcs(main.AQ_DATA_EVENT,data) # Old

    @sio_recv.event
    def disconnect(sid):
        print('disconnect', sid)

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0',main.TRANSMISSION_PORT)), app)
    
