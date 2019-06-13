from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# Create a SentimentIntensityAnalyzer object. 
sid_obj = SentimentIntensityAnalyzer()
def sentiment_scores(sentence): 
    '''    
       polarity_scores method of SentimentIntensityAnalyzer 
       oject gives a sentiment dictionary. 
       which contains pos, neg, neu, and compound scores. 

       Input Parameter: sentence whose polarity needs to be determined.
       Objective: To calculate polarity of sentence
       Output Parameter: return sentiment dictionary
    '''
    sentiment_dict = sid_obj.polarity_scores(sentence) 
    return sentiment_dict