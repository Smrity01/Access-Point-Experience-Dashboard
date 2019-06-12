from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

                                                
#import sys
#from importlib import reload
#sys.setdefaultencoding('utf8') 

lastUpdatedDate = "2013-01-26 18:10:11"
lastUpdatedDateNoCo = "2014-05-28 21:23:07"

class Youtube():
    
    def __init__(self):
        '''
        Objective       : Initialize youtube API developer key, service name and version
        Input Parameter : -
        Return          : -
        '''
        developerKey = "AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs"
        youtubeApiServiceName = "youtube"
        youtubeApiVersion = "v3"
        pafy.set_api_key("AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs")
        self.youtube = build(youtubeApiServiceName, youtubeApiVersion, developerKey = developerKey)

    def getFormatDateTime(self, dateTime):
        '''
        Objective       : Convert dateTime in format %YYYY-%MM-%DD %hh:%mm:%ss
        Input Parameter : DateTime - original dateTime in comment/reply data
        Return          : Formatted date-time
        '''
        dateTimeList = dateTime.split('T')
        formattedTime = dateTimeList[1].split('.')
        formattedDateTime = ""
        formattedDateTime = ''.join(dateTimeList[0]) + ' ' + ''.join(formattedTime[0])
        return formattedDateTime
    
    def sortCSV(self, fileName):
        '''
        Objective       : Sort CSV file data in reverse order on date-time column 
                            date time format is %Y-%m-%d %H:%M:%S
        Input Parameter : FileName - file to be sorted
        Return          : Sorted data
        '''
        try:
        	fd1 = open(fileName, "r")
        	data = csv.reader(fd1, delimiter=',')
        	sortedData = sorted(data, key = lambda row: datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S"),reverse=True)
        	#print(sortedData)
        	fd1.close()
        	return sortedData
        except IOError:
            return None
    
    def initLastUpdatedDate(self, fileName, fileNameNoCo):
        '''
        Objective       : Initialize date-time with most recent date-time in file
        Input Parameter : fileName - csv file with location
        				  fileNameNoCo - csv file without location
        Return          : -
        '''
        sortedData = self.sortCSV(fileName)
        if(sortedData): 
        	global lastUpdatedDate
        	firstRow = sortedData[0]
        	lastUpdatedDate = firstRow[7]
        	#print(lastUpdatedDate)

        sortedData = self.sortCSV(fileNameNoCo)
        if(sortedData): 
        	global lastUpdatedDateNoCo
        	firstRow = sortedData[0]
        	lastUpdatedDateNoCo = firstRow[7]
        	#print(lastUpdatedDate)
    
    def setLastUpdatedDate(self, newDate):
        '''
        Objective       : set last updated comment/reply date-time
        Input Parameter : newDate - new date-time
        Return          : -
        '''
        global lastUpdatedDate
        lastUpdatedDate = newDate
        
    def getLastUpdatedDate(self, newDate):
        '''
        Objective       : set last updated comment/reply date-time
        Input Parameter : newDate - new date-time
        Return          : Last updated Date 
        '''
        global lastUpdatedDateNoCo
        lastUpdatedDateNoCo = newDate
    
    def checkDate(self, oldDate, newDate):
        if oldDate < newDate:
            return False
        else:
            return True  
    def isAddedInCSV(self, row, flag):
        '''
        Objective       : Check if comment/reply row is already added in csv file
        Input Parameter : Row - contains comment/reply with related information
                          flag - 0 for csv file without country, 1 for with country
        Return          : False if date in row is greater than last updated date-time
        		            otherwise, True 
        '''
        if flag == 0:
        	global lastUpdatedDate
        	oldDate = datetime.strptime(lastUpdatedDate, "%Y-%m-%d %H:%M:%S")
        	newDate = datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S")
        	return self.checkDate(oldDate, newDate)

        if flag == 1:
        	global lastUpdatedDateNoCo
        	oldDate = datetime.strptime(lastUpdatedDateNoCo, "%Y-%m-%d %H:%M:%S")
        	newDate = datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S")
        	return self.checkDate(oldDate, newDate)

    def getVideoData(self, videoId):
        '''
        Objective       : Fetch comment threads on a youtube video
        Input Parameter : VideoID - Unique Id of video
        Return          : Required fields of fetched comments data
        '''
        url = "https://www.youtube.com/watch?v=" + videoId
        #Request for Metadata of the Video
        #videoData = pafy.new(url)
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
                try:
                    results = self.youtube.commentThreads().list(part = "snippet", maxResults = 100, videoId = videoId, textFormat = "plainText", pageToken = nextPageToken).execute()
                    totalResults = int(results["pageInfo"]["totalResults"])
                except HttpError:
                    halt = True
            if halt == False:
                count += totalResults
                for item in results["items"]:
                    comment = item["snippet"]["topLevelComment"]
                    author = comment["snippet"]["authorDisplayName"]
                    text = comment["snippet"]["textDisplay"]
                    idi = item['snippet']['topLevelComment']['id']
                    publishedAt = item['snippet']['topLevelComment']['snippet']['publishedAt']
                    updatedAt = item['snippet']['topLevelComment']['snippet']['updatedAt']
                    comments.append([author, text, idi, publishedAt, updatedAt])
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

    def getComments(self, videoIds):
        '''
        Objective       : Fetch all comments on multiple youtube videos
        Input Parameter : videoIDs - list of Unique Id of videos
        Return          : fetched comments data
        '''
        comments = []
        #get comments on each video
        try:
            for videoId in videoIds:
                comment = []
                comment = self.getVideoData(videoId)
                comments.extend(comment)
            return comments
        except IndexError:
            return None

    def getSentimentScores(self , sentence):
        '''
        Objective       : Find polarity of sentence
        Input Parameter : sentence - text on video (comment/reply)
        Return          : Polarity scores
        '''
        sidObj = SentimentIntensityAnalyzer()
        sentimentDictionary = sidObj.polarity_scores(sentence)
        return sentimentDictionary

    def getReplies(self, parentId):
        '''
        Objective       : Fetch all replies on a comment on a youtube video
        Input Parameter : parentID - Id for comment
        Return          : Fetched replies in any
        '''
        response = self.youtube.comments().list(part = 'snippet', parentId = parentId, textFormat="plainText").execute()
        return  response

    def writeRow(self, reviewData, flag):
        '''
        Objective       : create list by appending required attributes from reviewData,
        			        call writeToCSV to update file
        Input Parameter :   reviewData - comment/reply data
        				    flag -  0 -> reviewData contains comment data
        				 			1 -> reviewData contains reply data
        Return          : -
        '''

        if flag == 0:
            #for comment
            author = reviewData[0]
            text = reviewData[1]
            publishedAt = reviewData[3]
            updatedAt = reviewData[4]
        if flag == 1:
            #for reply
            author = reviewData["snippet"]["authorDisplayName"]
            text = reviewData["snippet"]["textDisplay"]
            publishedAt = reviewData['snippet']['publishedAt']
            updatedAt = reviewData['snippet']['updatedAt']        
        i = self.youtube.channels().list(part = 'snippet',forUsername=author).execute()
        if len(i['items']) > 0:
            row = []
            polarity = self.getSentimentScores(text.encode('unicode-escape').decode('utf-8'))
            row.append(text.encode('unicode-escape').decode('utf-8'))
            
            if('country' in i['items'][0]['snippet']):
                row.append(i['items'][0]['snippet']['country'])
            else:
                row.append(" ")
            
            row.append(author.encode('unicode-escape').decode('utf-8'))
            row.append(polarity['compound'])
            row.append(polarity['neg']*100)
            row.append(polarity['neu']*100)
            row.append(polarity['pos']*100)
            #PUBLISHED DATE & TIME
            row.append(self.getFormatDateTime(publishedAt))   
            #UPDATED DATE & TIME
            row.append(self.getFormatDateTime(updatedAt))   
            self.writeToCSV(row)

    def writeToCSV(self, row):
        '''
        Objective       : Write data in csv file after checking if it is not already added
        Input Parameter : row - list containing data to be inserted
        Return          : -
        '''
        if(row[1] != " "):
            #added date time check logic
            #print(self.isAddedInCSV(row))
            #print('\n')
            if(self.isAddedInCSV(row, 0)): 
                return None
            else:
                try: 
                    fd1 = open("review.csv", "a", newline='')
                    try:
                        writer1 = csv.writer(fd1, delimiter=',')
                        writer1.writerows([row])
                        #update the variable with date of newly added row
                        self.setLastUpdatedDate(row[7])
                    finally:
                        fd1.close()
                except IOError:
                    return None
        else:
            #to be added date time check logic 
            if(self.isAddedInCSV(row, 1)): 
                return None
            else:
                try:
                    fd2 = open("output.csv", "a", newline='')
                    try:
                        writer2 = csv.writer(fd2, delimiter=',')
                        writer2.writerows([row])
                        #update the variable with date of newly added row
                        self.setLastUpdatedDate(row[7])
                    finally:
                        fd2.close()
                except IOError:
                    return None
def main():
    '''
    Objective       : Main function / Driver Function
	Input Parameter : -
    Return          : -
    '''
    # creating object of Youtube Class
    yObject = Youtube()
    videoIds = ["GXGN4f6ma4k" , "RBXEIo37Q1w" , "P3fuh03n0mE" , "Jn0kFSXo9gY" , "_ybn9sC8xE0"]
    #row = ["Comment","Location","UserId","Compound","Negative","neutral","positive"]
    #writer2.writerows([row])
    yObject.initLastUpdatedDate("review.csv", "output.csv")
    
    comments = yObject.getComments(videoIds)
    for comment in comments:
        yObject.writeRow(comment, 0)
        replies = yObject.getReplies(comment[2])
        for reply in replies["items"]:
            #print(reply)
            yObject.writeRow(reply, 1)

if __name__ == "__main__":
    # calling main function
    main()
