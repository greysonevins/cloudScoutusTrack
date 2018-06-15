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
LASTDECIDED = "Washington v. United States"
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
		DECIDEDINX= next((index for index, dictItem in enumerate(caseDecisions) if LASTDECIDED == dictItem.decision), None)
		decidedList = []
		os.system('clear')

		if DECIDEDINX > 1:
			decidedList = caseDecisions[0:DECIDEDINX]



		if CASE != LASTDECIDED:

			if not decidedList:
				sendCaseEmail(caseDecisions[0])


			else:
				[sendCaseEmail(case) for case in decidedList]


		LASTDECIDED, CASE = caseDecisions[0].decision, caseDecisions[0].decision

	except Exception as e:
		print(e)
		logging.warn(e)
		sendEmail("Exception Raised on url track Court", e)
		pass


	t = threading.Timer(100, checkStatus)
	t.start()
	if STOP:
		print("stop search")
		logging.warn("Stop search")
		t.cancel()

def sendCaseEmail(case):
	global CASE, STOP
	caseinfo =  case.information + '\n \n' + case.url + \
						'\n Time Found: \n' + case.time
	print("DECIDED")
	headerCase = "Decision Made for {} Made".format(case.decision)
	logging.info(headerCase)
	logging.info(caseinfo)
	sendEmail(headerCase, caseinfo)
	if case == "Trump v. Hawaii":
					STOP = True

t = threading.Timer(100, checkStatus)
t.start()
