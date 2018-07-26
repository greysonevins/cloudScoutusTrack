import pandas as pd
import json
import itertools
from datetime import datetime
import time
timeStart = datetime.now()
listFiles = ["statuesStream.txt", "statuesStream0.txt", "statuesStream1.txt",
              "statuesStream2.txt", "statuesStream3.txt", "statuesStream4.txt",
              "statuesStream5.txt", "statuesStream6.txt", "statuesStream7.txt",
              "statuesStream8.txt", "statuesStream9.txt", "statuesStream10.txt",
              "statuesStream11.txt", "statuesStream12.txt", "statuesStream13.txt",
              "statuesStream14.txt", "statuesStream15.txt", "statuesStream16.txt",
              "statuesStream17.txt", "statuesStream18.txt","statuesStream19.txt",
              "statuesStream20.txt"]

def getTweets(filename):
    file = open(filename, "r")
    for line in file:
        try:
            tweet= json.loads(line)
            tweet2 = {
                "text": "",
                "ids" : "",
                "created_at":  "",
                "tweet_id" : "",
                "following_count": "",
                "followers_count": "",
                "screen_name"    :"",
                "is_retweet"    : "",
                "reply_to"      : "",
                "verfied_user"  : ""

            }
            if tweet['text']:
                if "extended_tweet" in tweet:
                    tweet2["text"] = tweet["extended_tweet"]["full_text"]
                else:
                    tweet2["text"] = tweet["text"]
                tweet2["tweet_id"] = tweet["id"]
                tweet2["ids"] = tweet["user"]["id"]
                tweet2["created_at"] = tweet["created_at"]
                tweet2["following_count"] = tweet["user"]["friends_count"]
                tweet2["followers_count"] = tweet["user"]["followers_count"]
                tweet2["screen_name"] = tweet["user"]["screen_name"]
                tweet2["is_retweet"] = "retweeted_status" in tweet
                tweet2["reply_to"] = tweet["in_reply_to_screen_name"] != None
                tweet2["verfied_user"] = tweet["user"]["verified"]

                yield tweet2
        except Exception:
            continue

tweets = []
for files in listFiles:
    print("Starting file # {}".format(len(tweets)+1))
    tweets.append((getTweets(files)))
    time.sleep(3)
    print("Finsihing file # {}".format(len(tweets)+1))

list_of_menuitems = [item for item in tweets]
chain = itertools.chain(*list_of_menuitems)
print("Turning to DataFrame")

tweetsDF = pd.DataFrame(list(chain))
print("Turning to DataFram to CSV")
tweetsDF.to_csv("twitterData.csv")
timeEnd = datetime.now()
timeTotal = timeStart - timeEnd
print("Total Time {}".format(timeTotal.total_seconds()))
