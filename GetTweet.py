import tweepy
import re
class Twitter():
    def __init__(self):
        '''
        Class constructor or initialization method.
        '''
        # keys and tokens from the Twitter Dev Console
        consumerKey    = '8WjP9Q9vu94yEhFMs2YIgVZp5'
        consumerSecret = 'scv2Ic3jhnFQMKJuI6NoyGfaxmSteSQMySSOxmAgSc8K1ufTOU'

        #access_token = '3548080632-xT2YIjmeVxrlnnJJmt9z5uBMADYPlfBU2Bxieks'
        # access_token_secret = 'Y22P9HnY46Jqnz0M2t1XofhcKbJvdZ7s8wO05ufS56vEV'
 
        # attempt authentication
        try:
            # create OAuthHandler object
            self.authorization = tweepy.OAuthHandler(consumerKey,consumerSecret)
            # create tweepy API object to fetch tweets
            self.apiObject = tweepy.API(self.authorization)
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
    def cleanTweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def getTweets(self, query, count = 100):
        '''
        Main function to fetch tweets and parse them.
        '''
        # empty list to store parsed tweets
        tweets = []
 
        try:
            # call twitter api to fetch tweets
            fetchedTweets = self.apiObject.search(q = query, count = count)
 
            # parsing tweets one by one
            for tweet in fetchedTweets:
                # empty dictionary to store required params of a tweet
                parsedTweet = {}
 
                # saving text of tweet
                parsedTweet['text'] = self.cleanTweet(tweet.text)
                parsedTweet['location'] = tweet.user.location

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsedTweet not in tweets:
                        tweets.append(parsedTweet)
                else:
                    tweets.append(parsedTweet)
 
            # return parsed tweets
            return tweets
 
        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))
def main():
    # creating object of TwitterClient Class
    twitterObject = Twitter()
    # calling function to get tweets
    topic = "amazon locker"
    tweets = twitterObject.getTweets(query = topic, count = 200)
    for i in tweets:
        print (i['text'],'\n',i['location'],"\n\n")

if __name__ == "__main__":
    # calling main function
    main()