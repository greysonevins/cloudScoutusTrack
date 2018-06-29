import tweepy
import os
import time
import pandas as pd
consumer_key = os.environ["SCOTUS_CONSUMER_KEY"]
consumer_secret = os.environ["SCOTUS_CONSUMER_SECRET"]
access_token = os.environ["SCOTUS_ACCESS_TOKEN"]
access_token_secret = os.environ["SCOTUS_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# test = tweets['ids'][0]
# var = api.friends(test)
# x =api.friends(tweets['ids'][0])
# print(x[0].verified)
# print(x[0])

# for friend in tweepy.Cursor(api.friends, test).items():
#     # Process the friend here
#     print(friend)

# def getUserFollowersVerified(idx):
#     listFollowersIDs, listFollowerNames = zip(*[[friend.id, friend.name] for friend in tweepy.Cursor(api.friends, id=idx, count=200).items() if friend.verified])
#     print(listFollowersIDs,listFollowerNames)
#     return listFollowersIDs, listFollowerNames

# # [print(friend.id) for friend in tweepy.Cursor(api.friends, tweets['ids'][0]).items() if friend.verified]
# # counter = 0
# # for friend in tweepy.Cursor(api.friends, tweets['ids'][0]).items():
# #     counter+=1
# #     print("here:{}".format(counter))
# #     if friend.verified:
# #         print(friend.id)
# #need to collect the followers of the twitter user
# #to get an average of more democrat or more republican
# #-1 or 1?
# setVerfied = set()
# setVerfiedNames = set()
# counter = 0
# userList = []
# for ids in tweets['ids']:
#     counter+=1
#     print("here:{}".format(counter))
#     verfiedIDs, verfiedNames = getUserFollowersVerified(ids)
#     user={"id": ids, "following": verfiedIDs}
#     userList.append(user)
#     [setVerfied.add(item) for item in verfiedIDs]
#     [setVerfiedNames.add(item) for item in verfiedNames]
#     print(setVerfiedNames)
# getUserFollowersVerified(tweets['ids'][0])

# verfiedIDs, verfiedNames = set(map(lambda friend: getUserFollowersVerified(friend), tweets['ids']))

COUNT = 0
IDX = 0
def getUserFollowersVerified(idx):
    global COUNT, IDX
    listFollowersIDs = []
    apisCalled = 0
    if idx != IDX:
        COUNT+=1
        IDX = idx
        time.sleep(62)
    if COUNT == 14:
        print("Count friends Lisr :{}".format(COUNT))
        # time.sleep(62)
        #time.sleep(900)
    try:
        for friend in tweepy.Cursor(api.friends_ids, id=idx, count=5000).items():
            listFollowersIDs.append(friend)
            if apisCalled%5000 ==0 and apisCalled != 0:
                time.sleep(62)
                print("here api 5000")
                COUNT+=1
            elif apisCalled==0:
                print("here api Called New")
                time.sleep(62)
                apisCalled += 1
    except Exception as e:
        print(e)
    return listFollowersIDs

# [print(friend.id) for friend in tweepy.Cursor(api.friends, tweets['ids'][0]).items() if friend.verified]
# counter = 0
# for friend in tweepy.Cursor(api.friends, tweets['ids'][0]).items():
#     counter+=1
#     print("here:{}".format(counter))
#     if friend.verified:
#         print(friend.id)
#need to collect the followers of the twitter user
#to get an average of more democrat or more republican
#-1 or 1?
COUNTV = 0

def getUserVerfied(setList):
    global COUNTV
    verified = []
    for user in setList:
        COUNTV+=1
        time.sleep(1.5)
        try:
            userV = api.get_user(user)
            if userV.verified:
                verified.append(user)
        except Exception as e:
            print(e)
            continue
        if COUNTV%900 == 0 and COUNTV != 0:
            print("Count :{}".format(COUNTV))
            print("Sleep for 900")
            COUNTV = 0
    return verified

def UserUpdate(userList, verified):
    finalSetList = set()
    for user in userList:
            user['following'] = [userFollow for userFollow in user['following'] if userFollow in verified]
            [finalSetList.add(user) for user in user['following']]

    return userList, finalSetList


def getListOfVerfied(ids):
    setVerfied = set()
    counter = 0
    userList = []
    for ids in ids:
        counter+=1
        print("here:{}".format(counter))
        verfiedIDs = getUserFollowersVerified(ids)
        user={"id": ids, "following": verfiedIDs}
        userList.append(user)
        [setVerfied.add(item) for item in verfiedIDs]
    return verfiedIDs, userList


def main():
    df = pd.read_csv("/home/greyson_nevins/ids.csv", header=-1)
    dfSample = df.sample(n=400, replace=True)
    ids = dfSample[1]
    setList, userList = getListOfVerfied(ids)
    verified = getUserVerfied(setList)
    userList, finalSetList = UserUpdate(userList,verified)
    userListDf = pd.DataFrame(userList)
    finalSetListDf = pd.DataFrame(finalSetList)
    userListDf.to_csv("user_list.csv")
    finalSetListDf.to_csv("final_verified.csv")

main()
