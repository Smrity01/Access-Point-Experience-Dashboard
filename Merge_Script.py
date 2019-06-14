import pandas
import numpy
import random
from datetime import datetime
from FileHandling import TextHandling

def merging() :
    countries = [ 'US' , 'UK','GB' ,'MX' ,'SE' ,'DK','DE']

    DateTimeFileName = "merge_date_time.txt"#File which store time of latest fetched and stored tweet
    DateTimeFileDiscriptor = TextHandling(DateTimeFileName)
    LastUpdatedDate = DateTimeFileDiscriptor.read()
    LastUpdatedDate = list(LastUpdatedDate.split("\n"))

    #Twitter
    twitterLastUpdatedDate = LastUpdatedDate[0]
    tweets = pandas.read_csv('tweety.csv')
    tweets = tweets[['Comment','Location','UserId','Compound','Negative','Neutral','Positive','PublishedDate']]
    tweets['Location'] = tweets['Location'].replace(numpy.nan, random.choice(countries))
    twitterNewUpdatedDate = tweets['PublishedDate'].max()
    tweets = tweets[tweets['PublishedDate'] > twitterLastUpdatedDate]
    #print(tweets1)
    #print(tweets['PublishedDate'])
    #Youtube_Review original
    youtubeLastUpdatedDate = LastUpdatedDate[1]
    youtubeReview = pandas.read_csv('review.csv') 
    youtubeReview = youtubeReview[['Comment','Location','UserId','Compound','Negative','Neutral','Positive','PublishedDate']]
    youtubeNewUpdatedDate = youtubeReview['PublishedDate'].max()
    youtubeReview = youtubeReview[youtubeReview['PublishedDate'] > youtubeLastUpdatedDate]
    #print(youtubeReview)
    #youtubeReview = youtubeReview[youtubeReview['PublishedDate'] > youtubeLastUpdatedDate]


    #Youtube_manipulated data
    youtubeLastUpdatedDate2 = LastUpdatedDate[2]
    youtubeManipulated = pandas.read_csv('output.csv') 
    youtubeManipulated = youtubeManipulated[['Comment','Location','UserId','Compound','Negative','Neutral','Positive','PublishedDate']]
    youtubeManipulated['Location'] = youtubeManipulated['Location'].apply(lambda x:random.choice(countries))
    youtubeNewUpdatedDate2 = youtubeManipulated['PublishedDate'].max()
    youtubeManipulated = youtubeManipulated[youtubeManipulated['PublishedDate'] > youtubeLastUpdatedDate2]

    #Storing merged comments
    mergedData = pandas.concat([tweets,youtubeReview, youtubeManipulated], ignore_index = False)
    with open('lockerData.csv', 'a') as f:
        mergedData.to_csv(f, header=False,index=False)
    #Storing Updated Date
    NewUpdatedDate = twitterNewUpdatedDate + "\n" + youtubeNewUpdatedDate + "\n" + youtubeNewUpdatedDate2
    DateTimeFileDiscriptor.write(NewUpdatedDate)