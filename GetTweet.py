'''
- Changes :
-At line - 66
  Replaced searchItem variable with a list.

  Problems to deal with:
-------------------------------

- At line - 72
    Its possible that the location is a city in USA but this code will only consider the location string containing 'USA'
        which is not correct.
'''
import tweepy
import re
class Twitter():
    def __init__(self):
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
def main():
    # creating object of Twitter Class and class class members to get tweets
    twitterObject = Twitter()
    searchItem = ["amazonlocker","amazonlockers","amazon lockers"]
    tweets = twitterObject.getTweets(query = searchItem)
    for i in tweets:
        #print the tweets from USA
        #if 'USA' in i['location']:
            print (i['text'],'\n',i['location'],"\n\n")

if __name__ == "__main__":
    # calling main function
    main()