import requests

class move_cam:
        def __init__(self,fifo_callback):
            self.callback = fifo_callback

        def execute(self,data):
            payload = { 'loginuse': 'admin', 'loginpas' :'', 'command' : data[1], 'onestep' : '0' }
            requests.get('http://192.168.0.100/decoder_control.cgi',params=payload)
