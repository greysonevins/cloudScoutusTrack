import os
import bs4
import threading
import requests
import re
from emailDecision import sendEmail
from datetime import datetime
import twitterStream
import google.cloud.logging
client = google.cloud.logging.Client().from_service_account_json(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

client.setup_logging()

import logging

URL = "https://www.supremecourt.gov/opinions/slipopinion/17"

CASE = ""
t = None
SENT = False
DECIDED = False
LASTDECIDED = ""
STOP = False

class DecisionInfo:
	def __init__(self, data):
		caseInfo = {
			"decision":  "No Title",
			"information": "No information",
			"url": "No URL",
			"time": str(datetime.now())

		}
		try:

			caseInfo["decision"] = data.text
		except:
			pass

		try:
			caseInfo["url"] = "https://www.supremecourt.gov/" + data["href"]
		except:
			pass

		try:
			caseInfo["information"] = data["title"].encode('ascii', 'ignore').decode('ascii')
		except:
			pass


		for key, value in caseInfo.items():
			setattr(self, key, value)



def checkStatus():
	global DECIDED, SENT, LASTDECIDED, STOP, t, CASE
	try:
		res = requests.get(URL)

		caseSoup = bs4.BeautifulSoup(res.text,'html.parser')


		caseDecisions = [DecisionInfo(a) for a in caseSoup.findAll('a', href=re.compile(r'^/opinions/17pdf?'))]

		LASTDECIDED, case = caseDecisions[0].decision, caseDecisions[0]
		os.system('clear')

		if CASE != LASTDECIDED:
			caseinfo =  case.information + '\n \n' + case.url + \
								'\n Time Found: \n' + case.time
			print("DECIDED")
			CASE = LASTDECIDED
			headerCase = "Decision Made for {} Made".format(CASE)
			logging.info(headerCase)
			logging.info(caseinfo)
			sendEmail(headerCase, caseinfo)
			if case == "Trump v. Hawaii":
                        	STOP = True


	except Exception as e:
		print(e)
		sendEmail("Exception Raised on url track Court", e)
		pass


	t = threading.Timer(100, checkStatus)
	t.start()
	if STOP:
		print("stop search")
		t.cancel()

t = threading.Timer(100, checkStatus)
t.start()
