import requests,json

PATH_TO_CREDITENTIALS = "./tools/mailgun_creditentials.json"

class send_mail_alert:

	def execute(self,data):
		with open(PATH_TO_CREDITENTIALS) as json_cred:
			dict_ = json.load(json_cred)
			request_url = 'https://api.mailgun.net/v3/{0}/messages'.format	(dict_['sandbox'])
			request = requests.post(request_url, auth=('api', dict_['key']), data={
		    		'from': 'Pluggi <crysteo@isen-lille.fr>',
				'to': dict_['recipient'],
				'subject': 'Help !',
				'text': 'Someone hit me !'
			})
