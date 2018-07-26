import os
import tweepy
import threading
import json
import csv
from emailDecision import sendEmail

Collected = 0

def startStream():
	consumer_key = os.environ["NA_CONSUMER_KEY"]
	consumer_secret = os.environ["NA_CONSUMER_SECRET"]
	access_token = os.environ["NA_ACCESS_TOKEN"]
	access_token_secret = os.environ["NA_ACCESS_TOKEN_SECRET"]

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)

	api = tweepy.API(auth)
	TRACKED_WORDS=[
			"#scotus",
			"#notoriousrbg",
			"#RBG",
			"Anthony Kennedy",
			"Clarence Thomas",
			"Ruth Bader Ginsburg",
			"Stephen Breyer",
			"Samuel Alito",
			"Sonia Sotomayor",
			"Elena Kagan",
			"Neil Gorsuch",
			"John Roberts",
			"Justice Kennedy",
			"Justice Thomas",
			"Justice Ginsburg",
			"Justice Breyer",
			"Justice Alito",
			"Justice Sotomayor",
			"Justice Kagan",
			"Justice Gorsuch",
			"Justice Roberts",
			"Justice Scalia",
			"SCOTUS",
			"#Kennedy",
			"#Thomas",
			"#Ginsburg",
			"#Breyer",
			"#Alito",
			"#Sotomayor",
			"#Kagan",
			"#Gorsuch",
			"#Roberts",
			"#AnthonyKennedy",
			"#ClarenceThomas",
			"#RuthBaderGinsburg",
			"#StephenBreyer",
			"#SamuelAlito",
			"#SoniaSotomayor",
			"#ElenaKagan",
			"#NeilGorsuch",
			"#JohnRoberts",
			"Trump v. Hawaii",
			"travel ban",
			"#MuslimBan"
			]
	class MyStreamListener(tweepy.StreamListener):
			def on_data(self, data):
				global Collected
				fname = "statuesStream.txt"
				if os.path.isfile(fname):
					with open("statuesStream.txt", "a") as myfile:
						myfile.write(data + "\n")
						Collected+=1
						if Collected%1000 == 0:
							msg = "Collected {} tweets so far".format(Collected)
							print(msg)
							sendEmail(msg, msg)
				else:
					with open("statuesStream.txt", "w") as myfile:
						myfile.write(data + "\n")
						sendEmail("Twitter Stream Started", "Started")
						print("start")
						Collected+=1
				return True

				def on_disconnect(self, notice):
					sendEmail("Error with Twitter Disconnect", notice)
					print(notice)
					return
				def on_warning(self, notice):
					sendEmail("Warning Triggered", notice)
					print(notice)
					return
				def on_error(self, status_code):
					sendEmail("Error with Twitter Stream", status_code)
					print(status_code)
					if status_code == 420:
						return False
				def on_exception(self, exception):
					sendEmail("Error with Twitter Exception Thrown", exception)
					print(exception)
					return

	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	myStream.filter(track=TRACKED_WORDS, languages=['esdfsxxxn'],stall_warnings=True, async=True)

def main():
	startStream()

if __name__ == "__main__":
	main()


