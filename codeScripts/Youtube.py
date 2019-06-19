from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import pafy
import csv
import sys
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from FileHandling import TextHandling

                                                
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
        developerKey = "Your Developer Key"
        youtubeApiServiceName = "youtube"
        youtubeApiVersion = "v3"
        pafy.set_api_key(developerKey)
        try:
            self.youtube = build(youtubeApiServiceName, youtubeApiVersion, developerKey = developerKey)
        except Exception as error:
            print(error)
            
    def getFormatDateTime(self, dateTime):
        '''
        Objective       : Convert dateTime in format %YYYY-%MM-%DD %hh:%mm:%ss
        Input Parameter : dateTime - original dateTime in comment/reply data
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
        Input Parameter : fileName - file to be sorted
        Return          : Sorted data
        '''
        try:
            fd1 = open(fileName, "r")
            data = csv.reader(fd1, delimiter=',')
            next(data)
            sortedData = sorted(data, key = lambda row: datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S"),reverse=True)
            #print(sortedData)
            fd1.close()
            return sortedData
        except Exception as error:
            print(error)
            return None
    
    def getLastUpdatedDate(self):
        '''
        Objective       : Initialize date-time with most recent date-time in file
        Input Parameter : fileName - csv file with location
        				  fileNameNoCo - csv file without location
        Return          : -
        '''
        DateTimeFileName = "youtubeDateTime.txt"
        #File which store time of latest fetched and stored tweet
        DateTimeFileDescriptor = TextHandling(DateTimeFileName)
        global lastUpdatedDate
        lastUpdatedDate = DateTimeFileDescriptor.read()
        print("\nLast UpdatedDate: ",lastUpdatedDate)
        DateTimeFileName = "youtubeDateTimeNoCo.txt"
        #File which store time of latest fetched and stored tweet
        DateTimeFileDescriptor = TextHandling(DateTimeFileName)
        global lastUpdatedDateNoCo
        lastUpdatedDateNoCo = DateTimeFileDescriptor.read()
        print('\n last updated no co', lastUpdatedDateNoCo)
        
    def setLastUpdatedDate(self):
        '''
        Objective       : Initialize date-time with most recent date-time in file
        Input Parameter : fileName - csv file with location
        				  fileNameNoCo - csv file without location
        Return          : -
        '''
        sortedData = self.sortCSV("output.csv")
        if(sortedData):
            firstRow = sortedData[0]
            DateTimeFileName = "youtubeDateTime.txt"
            #File which store time of latest fetched and stored tweet
            DateTimeFileDescriptor = TextHandling(DateTimeFileName)
            DateTimeFileDescriptor.write(firstRow[7])
            #print(lastUpdatedDateNoCo)

        sortedData = self.sortCSV("review.csv")
        if(sortedData): 
            firstRow = sortedData[0]
            DateTimeFileName = "youtubeDateTimeNoCo.txt"
            #File which store time of latest fetched and stored tweet
            DateTimeFileDescriptor = TextHandling(DateTimeFileName)
            DateTimeFileDescriptor.write(firstRow[7])
            #print(lastUpdatedDate)
            
    def checkDate(self, oldDate, newDate):
        '''
        Objective       : check date-time
        Input Parameter : oldDate - date
                          newDatw - date
        Return          : False if oldDate < newDate else True
        '''
        if oldDate < newDate:
            return False
        else:
            return True  
    
    def isAddedInCSV(self, row, flag):
        '''
        Objective       : Check if comment/reply row is already added in csv file
        Input Parameter : Row - contains comment/reply with related information
                          flag - 0 for csv file with country, 1 for no country
        Return          : False if date in row is greater than last updated date-time
                            otherwise, True 
        '''
        if flag == 0:
            global lastUpdatedDate
            oldDate = datetime.strptime(lastUpdatedDate, "%Y-%m-%d %H:%M:%S")
            newDate = datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S")
            #print("\nCheckDate: ",self.checkDate(oldDate, newDate))
            return self.checkDate(oldDate, newDate)

        if flag == 1:
            global lastUpdatedDateNoCo
            oldDate = datetime.strptime(lastUpdatedDateNoCo, "%Y-%m-%d %H:%M:%S")
            newDate = datetime.strptime(row[7], "%Y-%m-%d %H:%M:%S")
            #print("\nCheckDate: ",self.checkDate(oldDate, newDate))
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
                except Exception as error:
                    print(error)
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
                except Exception as error:
                    print(error)
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
        except Exception as error:
            print(error)
            return None

    def getSentimentScores(self , sentence):
        '''
        Objective       : Find polarity of sentence
        Input Parameter : sentence - text on video (comment/reply)
        Return          : Polarity scores
        '''
        try:
            sidObj = SentimentIntensityAnalyzer()
            sentimentDictionary = sidObj.polarity_scores(sentence)
            return sentimentDictionary
        except Exception as error:
            print(error)

    def getReplies(self, parentId):
        '''
        Objective       : Fetch all replies on a comment on a youtube video
        Input Parameter : parentID - Id for comment
        Return          : Fetched replies in any
        '''
        try:
            response = self.youtube.comments().list(part = 'snippet', parentId = parentId, textFormat="plainText").execute()
            return  response
        except Exception as error:
            print(error)
        

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
            try:
                author = reviewData["snippet"]["authorDisplayName"]
                text = reviewData["snippet"]["textDisplay"]
                publishedAt = reviewData['snippet']['publishedAt']
                updatedAt = reviewData['snippet']['updatedAt']
            except Exception as error:
                print
        row = []
        polarity = self.getSentimentScores(text)
        print(polarity)
        row.append(text.encode('unicode-escape').decode('utf-8'))
            
        try:
            i = self.youtube.channels().list(part = 'snippet',forUsername=author).execute()
            if len(i['items']) > 0:
                if('country' in i['items'][0]['snippet']):
                    row.append(i['items'][0]['snippet']['country'])
                else:
                    row.append(" ")
            else:
                row.append(" ")

        except Exception as error:
            print(error)
            
        row.append(author.encode('unicode-escape').decode('utf-8'))
        row.append(polarity['compound'])
        row.append(polarity['neg']*100)
        row.append(polarity['neu']*100)
        row.append(polarity['pos']*100)
        #PUBLISHED DATE & TIME
        row.append(self.getFormatDateTime(publishedAt))
        #print(type(publishedAt))   
        #UPDATED DATE & TIME
        row.append(self.getFormatDateTime(updatedAt))   
        self.writeToCSV(row)

    def writeToCSV(self, row):
        '''
        Objective       : Write data in csv file after checking if it is not already added
        Input Parameter : row - list containing data to be inserted
        Return          : -
        '''
        if(row[1] == " "):
            #added date time check logic
            #print(self.isAddedInCSV(row))
            #print('\n')
            if(self.isAddedInCSV(row, 1)): 
                return None
            else:
                try: 
                    fd1 = open("output.csv", "a", newline='')
                    try:
                        writer1 = csv.writer(fd1, delimiter=',')
                        writer1.writerows([row])
                    finally:
                        fd1.close()
                except Exception as error:
                    print(error)
                    return None
        else:
            #to be added date time check logic 
            if(self.isAddedInCSV(row, 0)): 
                return None
            else:
                try:
                    fd2 = open("review.csv", "a", newline='')
                    try:
                        writer2 = csv.writer(fd2, delimiter=',')
                        writer2.writerows([row])
                    finally:
                        fd2.close()
                except Exception as error:
                    print(error)
                    raise
                    #return None
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
    yObject.getLastUpdatedDate()
    try:
        comments = yObject.getComments(videoIds)
        
        for comment in comments:
            yObject.writeRow(comment, 0)
            replies = yObject.getReplies(comment[2])
            for reply in replies["items"]:
                #print(reply)
                yObject.writeRow(reply, 1)
    except TypeError as error:
        print(error)
        raise
    yObject.setLastUpdatedDate()
    
if __name__ == "__main__":
    # calling main function
    main()

