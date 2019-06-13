import tweepy
import re
from FileHandling import CSVHandling,TextHandling
from SentimentAnalysis import sentiment_scores
from datetime import datetime

class Twitter():
    file = 0
    header = 0
    TweetsFile = 0
    
    def __init__(self,filename,head):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console o get tweets from twitter
        consumerKey    = '8WjP9Q9vu94yEhFMs2YIgVZp5'
        consumerSecret = 'scv2Ic3jhnFQMKJuI6NoyGfaxmSteSQMySSOxmAgSc8K1ufTOU'
        '''
        These Tokens are for activities such as tweet, like, retweet, etc.
        access_token = '3548080632-xT2YIjmeVxrlnnJJmt9z5uBMADYPlfBU2Bxieks'
        access_token_secret = 'Y22P9HnY46Jqnz0M2t1XofhcKbJvdZ7s8wO05ufS56vEV'
        '''
        # Authentication Try-Catch Block OR print error (if any)
        try:
            # create OAuthHandler object and create tweepy API object to fetch tweets
            self.authentication = tweepy.OAuthHandler(consumerKey,consumerSecret)
            self.apiObject = tweepy.API(self.authentication)
        except tweepy.TweepError as error:
            print("Error : " + str(error))
        self.file = filename
        self.header = head
        self.TweetsFile = CSVHandling(self.file,self.header)

    def cleanTweet(self,tweet):
        '''
        Clean tweet by removing extra charaters or html tags
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def getTweets(self, query):
        '''
        ------Main function to fetch tweets and parse them-------
        -  Call twitter api to fetch tweets using search function refer README for details.
                request('search/tweets', {'q': query}) thiscan also be used

        '''
        tweetList = [] 
        fetchedTweets = []
        
        try:
            for i in query:
                fetchedTweets += self.apiObject.search(q = i)
            # parsing tweets one by one
                for tweet in fetchedTweets:
                # empty dictionary to store required params of a tweet
                    parsedTweet = {}
                # saving clean text and location of tweet in the form of dictionary into Tweet list
                parsedTweet['text'] = self.cleanTweet(tweet.text)
                parsedTweet['location'] = tweet.user.location
                parsedTweet['time'] = tweet.created_at
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsedTweet not in tweetList:
                        tweetList.append(parsedTweet)
                else:
                    tweetList.append(parsedTweet)
 
            # return Final list of clean tweets and there locations
            return tweetList
        except tweepy.TweepError as e:
            print("Error : " + str(e))
                    
    def write_data(self , data ,date) :
        '''
        input parameter:-
                        data: tweets that need to be write in csv,
                        date: time of latest stored tweet
        Objctive:-
                Write tweets which are tweeted after date to csv file.
        Output parameter:-
                return date of latest stored tweet
        '''
        newDate = date
        for tweet in data:
            strTime = tweet['time'].strftime("%y-%m-%d %H:%M:%S")
            if strTime > date :
                polarity = sentiment_scores(tweet['text'])
                self.TweetsFile.write_row([tweet['text'],tweet['location'],strTime,' ',polarity['compound'],polarity['neg']*100,polarity['neu']*100,polarity['pos']*100] )
                if newDate < strTime :
                    newDate = strTime
        return newDate

def main():
    '''
        Objective       : Main function / Driver Function
        Input Parameter : -
        Return          : -
    '''
    # creating object of Twitter Class and class class members to get tweets
    twitterObject = Twitter('tweety.csv',['Tweet','Location','Time','User Id','Compound','Negative','Neutral','Positive'])
    
    searchItem = ["amazonlocker","amazonlockers","amazon lockers"]
    
    DateTimeFileName = "twitter_date_time.txt"#File which store time of latest fetched and stored tweet
    DateTimeFileDiscriptor = TextHandling(DateTimeFileName)
    LastUpdatedDate = DateTimeFileDiscriptor.read()
    
    tweets = twitterObject.getTweets(query = searchItem)
    for i in tweets:
        print (i['text'],'\n',i['time'],'\n',i['location'],"\n\n")
        
    NewDate = twitterObject.write_data(tweets , LastUpdatedDate)
    DateTimeFileDiscriptor.write(NewDate)
    
if __name__ == "__main__":
    # calling main function
    main()





