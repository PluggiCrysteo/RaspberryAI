import requests,json,vlc

PATH_TO_CREDITENTIALS = "./tools/mailgun_creditentials.json"
PATH_TO_ALERT = "/home/crysteo/content/DANGEEER.wav"

class gyro_alert:
    
        def __init__(self,fifo_callback):
            self.callback = fifo_callback

	def execute(self,data):
		with open(PATH_TO_CREDITENTIALS) as json_cred:
			dict_ = json.load(json_cred)
			request_url = 'https://api.mailgun.net/v3/{0}/messages'.format	(dict_['sandbox'])
			request = requests.post(request_url, auth=('api', dict_['key']), data={
		    		'from': 'Pluggi <crysteo@isen-lille.fr>',
				'to': dict_['recipient'],
				'subject': 'Help !',
				'text': 'Someone moved me !\nGyroscope alert.'
			})
                vlc.MediaPlayer(PATH_TO_ALERT).play()
