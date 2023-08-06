class SlackNotif(object):

	def __init__(self,channel,token):
		self.channel = channel
		self.token = token

	def sendNotification(err=None):
		token = self.token
		url_base ="https://hooks.slack.com/services/T04K0GJSL/BGMEFFQ6M/" 
		url=str(url_base)+str(token)
		data={"attachments": [
		    {           
		        "color": "#36a64f",
		        "title": "Smallsuite is down :scream:",
		        "fields": [
		            {
		                "title": "Sample Notif",
		                "value": err,
		                "short": False
		            }
		        ]
		    }
		]}
		headers={"Content-Type":"application/json"}
		r = requests.post(url = url,data = json.dumps(data),headers=headers)
		return True
