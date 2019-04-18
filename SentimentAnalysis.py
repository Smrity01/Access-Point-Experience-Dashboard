from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# Create a SentimentIntensityAnalyzer object. 
sid_obj = SentimentIntensityAnalyzer()
def sentiment_scores(sentence):  
    # polarity_scores method of SentimentIntensityAnalyzer 
    # oject gives a sentiment dictionary. 
    # which contains pos, neg, neu, and compound scores. 
    sentiment_dict = sid_obj.polarity_scores(sentence) 
    return sentiment_dict