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

lastUpdatedDate = ""

class Youtube():
    
    def __init__(self):
        developerKey = "AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs"
        youtubeApiServiceName = "youtube"
        youtubeApiVersion = "v3"
        pafy.set_api_key("AIzaSyC7YZD2osLIZ4GXFEMnoOdvQ6Hkr6mUcUs")
        self.youtube = build(youtubeApiServiceName, youtubeApiVersion, developerKey = developerKey)
    def getFormatDate(self, dateTime):
        dateTimeList = dateTime.split('T')
        return dateTimeList[0]
    def getFormatTime(self, dateTime):
        dateTimeList = dateTime.split('T')
        formattedTime = dateTimeList[1].split('.')
        return formattedTime[0]
    
    def sortCSV(self, fileName):
        fd1 = open(fileName, "r")
        data = csv.reader(fd1, delimiter=',')
        sortedData = sorted(data, key = lambda row: datetime.strptime(row[7], "%Y-%m-%d"),reverse=True)
        #print(sortedData)
        fd1.close()
        return sortedData
    
    def initLastUpdatedDate(self, fileName):
        global lastUpdatedDate
        sortedData = self.sortCSV(fileName)
        firstRow = sortedData[0]
        lastUpdatedDate = firstRow[7]
        #print(lastUpdatedDate)
    
    def setLastUpdatedDate(self, newDate):
        global lastUpdatedDate
        lastUpdatedDate = newDate
        
    def getLastUpdatedDate(self):
        global lastUpdatedDate
        return lastUpdatedDate
        
    def isAddedInCSV(self, row):
        global lastUpdatedDate
        newDate1 = datetime.strptime(lastUpdatedDate, "%Y-%m-%d")
        newDate2 = datetime.strptime(row[7], "%Y-%m-%d")
        if newDate1 < newDate2:
            return False
        else:
            return True

    def getVideoData(self, videoId):
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
                except HttpError as e:
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
        sidObj = SentimentIntensityAnalyzer()
        sentimentDictionary = sidObj.polarity_scores(sentence)
        return sentimentDictionary

    def getReplies(self, parentId):
        response = self.youtube.comments().list(part = 'snippet', parentId = parentId, textFormat="plainText").execute()
        return  response

    def writeRow(self, reviewData, flag):

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
            row.append(self.getFormatDate(publishedAt))
            row.append(self.getFormatTime(publishedAt))   
            #UPDATED DATE & TIME
            row.append(self.getFormatDate(updatedAt))
            row.append(self.getFormatTime(updatedAt))   
            self.writeToCSV(row)

    def writeToCSV(self, row):
        if(row[1] != " "):
            #added date time check logic
            print(self.isAddedInCSV(row))
            print('\n')
            if(self.isAddedInCSV(row)): 
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
            try:
                fd2 =  open("output.csv", "a", newline='')
                try:
                    writer2 = csv.writer(fd2, delimiter=',')
                    writer2.writerows([row])
                finally:
                    fd2.close()
            except IOError:
                return None

def main():
    # creating object of Youtube Class
    yObject = Youtube()
    videoIds = ["GXGN4f6ma4k" , "RBXEIo37Q1w" , "P3fuh03n0mE" , "Jn0kFSXo9gY" , "_ybn9sC8xE0"]
    #row = ["Comment","Location","UserId","Compound","Negative","neutral","positive"]
    #writer2.writerows([row])
    yObject.initLastUpdatedDate("review.csv")
    #print("\n lastUpdatedDate: ")
    #global lastUpdatedDate
    #print(lastUpdatedDate)
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

