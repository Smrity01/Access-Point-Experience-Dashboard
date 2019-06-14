import pandas
import numpy
import random
from datetime import datetime
#Twitter

twitterLastUpdatedDate = '2018-06-13 02:58:58'
tweets = pandas.read_csv('tweety.csv')
tweets = tweets[['Comment','Location','UserId','Compound','Negative','Neutral','Positive','PublishedDate']]
tweets1 = tweets[tweets['PublishedDate'] == " "]
tweets = tweets[tweets['PublishedDate'] > twitterLastUpdatedDate]
#print(tweets1)
#print(tweets['PublishedDate'])
#Youtube_Review original
youtubeLastUpdatedDate = '2010-06-12 19:45:08'
youtubeReview = pandas.read_csv('review.csv') 
youtubeReview = youtubeReview[['Comment','Location','UserId','Compound','Negative','Neutral','Positive','PublishedDate']]
youtubeReview = youtubeReview[youtubeReview['PublishedDate'] > youtubeLastUpdatedDate]
#print(youtubeReview)
#youtubeReview = youtubeReview[youtubeReview['PublishedDate'] > youtubeLastUpdatedDate]


#Youtube_manipulated data
youtubeLastUpdatedDate2 = '2010-06-12 19:45:08'
countries = [ 'US' , 'UK','GB' ,'MX' ,'SE' ,'DK','DE']
youtubeManipulated = pandas.read_csv('output.csv') 
youtubeManipulated = youtubeManipulated[['Comment','Location','UserId','Compound','Negative','Neutral','Positive','PublishedDate']]
youtubeManipulated['Location'] = youtubeManipulated['Location'].apply(lambda x:random.choice(countries))
youtubeManipulated = youtubeManipulated[youtubeManipulated['PublishedDate'] > youtubeLastUpdatedDate2]

mergedData = pandas.concat([tweets1,tweets,youtubeReview, youtubeManipulated], ignore_index = False)
mergedData.to_csv('lockerData.csv',index=False)
