import requests,json

class setupWebhook(object):
	def __init__(self,
		*args):
		self.finalurl = None
		if args:
			if args[0].startswith("http") and "hooks" in args[0]:
				self.finalurl = args[0]
			elif len(args) == 3:	
				self.finalurl = "https://hooks.slack.com/services/{}/{}/{}".format(
					args[0],args[1],args[2])	
			else:
				raise ValueError("please pass correct parameter(s)")
		else: 
			raise ValueError("please pass (correct) parameter(s)")	


	def getColor(self,
		statuscode):
		arr_colors = {
		"success": "#66ff66",
		"info" : "#00ffcc",
		"warning" : "#ffff99",
		"danger" : "#ff4d4d"
		}
		try:
			return arr_colors[statuscode]
		except KeyError as e:
			raise KeyError("please provide proper status code")
		

	def sendNotification(self,
		notif_title=None,
		error_title=None,
		error=None,
		status_code="success"):

		if notif_title is None or error_title is None or error is None or "" in {notif_title,error_title,error}:
			raise ValueError("Did not get required parameters")	
		status_code = self.getColor(status_code)
		url=self.finalurl
		data={"attachments": [
		    {           
		        "color": status_code,
		        "title": notif_title,
		        "fields": [
		            {
		                "title": error_title,
		                "value": error,
		                "short": False
		            }
		        ]
		    }
		]}

		headers={"Content-Type":"application/json"}
		try:
		    requests.post(url = url,data = json.dumps(data),headers=headers,timeout=5)
		except requests.Timeout:
		    raise Exception()
		except requests.ConnectionError:
		    raise ConnectionError("Connection not established")
		return "Success!!"