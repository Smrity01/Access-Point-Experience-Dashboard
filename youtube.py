'''
Problems- 1.Unable to add the data to a csv file
2.Unable to retrieve location
3.Works for a single video id at a time

'''
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv 


#import sys
#from importlib import reload
#sys.setdefaultencoding('utf8') 

DEVELOPER_KEY = "AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"
pafy.set_api_key("AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs")

def add_data(vID,title,description,author, likes,dislikes,rating,category,comments):
	data = [vID,title,description,author,likes, dislikes,rating,category,comments]
	#with open("scraper.csv", "a") as fp:
		#wr = csv.writer(fp, dialect='excel')
		#wr.writerow(data)
	print(data) 
		

youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)

videoId = "GXGN4f6ma4k"
url = "https://www.youtube.com/watch?v=" + videoId
#Request fro Metadata of the Video
video = pafy.new(url)

#Request for Comments
results = youtube.commentThreads().list(
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
	  		results = youtube.commentThreads().list(
	  		  part="snippet",
	  		  maxResults=100,
	  		  videoId=videoId,
	  		  textFormat="plainText",
	  		  pageToken=nextPageToken
	  		).execute()
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

# Adding the full data to CSV
add_data(videoId,video.title,video.description,video.author,video.likes, video.dislikes,video.rating,video.category,comments)
