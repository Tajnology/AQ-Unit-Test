import socketio
import eventlet
import json

import main

sio_send_connected = False
sio_send = None

def init():
    sio_recv = socketio.Server()
    app = socketio.WSGIApp(sio_recv)

    clients = {}

    @sio_recv.event
    def connect(sid, environ, auth):
        print('connect', sid)
        clients[sid] = environ

    @sio_recv.on(main.TD_IMAGE_EVENT)
    def receive_td_image(sid,data):
        resdata = "data:image/jpeg;base64," + str(data['image'].decode("utf-8"))
        msg_gcs('streaming',{'image':resdata})

    @sio_recv.on(main.TD_TARGET_EVENT)
    def received_td_logtarget(sid,data):
        resimg = "data:image/jpeg;base64," + str(data['image'].decode("utf-8"))
        params = {'image':resimg,'label':data['label']}
        msg_gcs('target_detected',params)
    
    @sio_recv.on(main.AQ_DATA_EVENT)
    def receive_aq_data(sid, data):
        msg_gcs('oxidising_gases',data['ox_gas'])
        msg_gcs('reducing_gases',data['red_gas'])
        msg_gcs('nh3',data['amm_gas'])
        #msg_gcs('air',data['amm_gas']) # Remove after integration
        #msg_gcs('gas',data['ox_gas']) # Remove after integration
        msg_gcs('temperature',data['temperature'])
        msg_gcs('pressure',data['pressure'])
        msg_gcs('humidity',data['humidity'])
        msg_gcs('light',data['light'])
        
        # msg_gcs(main.AQ_DATA_EVENT,data) # Old

    @sio_recv.on(main.AQ_STATUS_EVENT)
    def receive_aq_status(sid,data):
        msg_gcs(main.AQ_STATUS_EVENT,{'is_heating':data['heating']})

    @sio_recv.on(main.INIT_GCS_CLIENT_EVENT)
    def init_client(sid, data):
        print("Initialise Client")
        global sio_send
        sio_send = socketio.Client()
        
        @sio_send.event
        def connect():
            print("GCS Server connected")
            global sio_send_connected
            sio_send_connected = True
            msg_gcs('checkClient','raspberry')

        @sio_send.event
        def disconnect():
            print("GCS Server disconnected")
            global sio_send_connected
            sio_send_connected = False

        url = 'http://' + clients[sid]['REMOTE_ADDR'] + ':' + data['port']
        print(url)
        sio_send.connect(url)
    
    @sio_recv.event
    def disconnect(sid):
        print('disconnect', sid)

    eventlet.wsgi.server(eventlet.listen(('0.0.0.0',main.TRANSMISSION_PORT)), app)

def msg_gcs(key, value):
    if(not sio_send_connected):
        return
    else:
        sio_send.emit(key,value)
    
