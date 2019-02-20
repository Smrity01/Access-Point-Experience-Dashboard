#!/usr/bin/env python
# coding: utf-8

# In[3]:


'''
Problems- 
- Works for a single video id at a time

'''
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv 


#import sys
#from importlib import reload
#sys.setdefaultencoding('utf8') 

class Youtube():
	def __init__(self):
		developerKey = "AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs"
		youtubeApiServiceName = "youtube"
		youtubeApiVersion = "v3"
		pafy.set_api_key("AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs")
		self.youtube = build(youtubeApiServiceName, youtubeApiVersion, developerKey = developerKey)
	def getVideoData(self, videoId):
		url = "https://www.youtube.com/watch?v=" + videoId
		#Request fro Metadata of the Video
		videoData = pafy.new(url)
		#Request for Comments
		results = self.youtube.commentThreads().list(
		    part="snippet",
		    maxResults=100,
		    videoId=videoId,
		    textFormat="plainText"
		  ).execute()
		totalResults = 0
		totalResults = int(results["pageInfo"]["totalResults"])
		count = 0
		nextPageToken = ''
		comments = []
		further = True
		first = True
		while further:
			halt = False
			if first == False:
				print (".")
				try:
					results = self.youtube.commentThreads().list(part = "snippet", maxResults = 100, videoId = videoId, textFormat = "plainText", pageToken = nextPageToken).execute()
					totalResults = int(results["pageInfo"]["totalResults"])
				except HttpError as e:
					halt = True
			if halt == False:
				count += totalResults
				for item in results["items"]:
					comment = item["snippet"]["topLevelComment"]
					author = comment["snippet"]["authorDisplayName"]
					text = comment["snippet"]["textDisplay"]
					comments.append([author,text])
			if totalResults < 100:
				further = False
				first = False
			else:
				further = True
				first = False
				try:
					nextPageToken = results["nextPageToken"]
				except KeyError as e:
					further = False
		return comments
	def getUserData(self, comments):
		hi = []
		for comment in comments:
			hi.append(self.youtube.channels().list(part = 'snippet',forUsername=comment[0]).execute())
			print(comment[0],'\n',comment[1])
		for i in hi:
			if len(i['items']) > 0:
				if('country' in i['items'][0]['snippet']):
					print(i['items'][0]['snippet']['country'],'\n\n')
'''
print (yObject.youtube.channels().list(part = 'snippet',forUsername='kentuckyrangerpro').execute())
#print(comments)
for item in results['items']:
	#print(type(item))
	print(item['items']['kind'])
	# ,"\n",item['snippet']['authorDisplayName']) 
#print(results[items])
'''    
# Adding the full data to CSV
#print(videoId,video.title,video.description,video.author,video.likes, video.dislikes,video.rating,video.category,comments)

def main():
    videoIds = ["GXGN4f6ma4k" , "RBXEIo37Q1w" , "P3fuh03n0mE" , "Jn0kFSXo9gY" , "_ybn9sC8xE0" , "FbjYxaTe1M0"]
    yObject = Youtube()
    comments = [yObject.getVideoData(videoId) for videoId in videoIds]
    for comment in comments:
        yObject.getUserData(comment)

if __name__ == "__main__":
    # calling main function
    main()


# In[ ]:




