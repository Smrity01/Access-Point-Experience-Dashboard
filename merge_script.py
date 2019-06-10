import pandas

colnames = ['Tweet','Location','Positive','Negative']
#Twitter
tweets = pandas.read_csv('tweety.csv',usecols = colnames)
tweets.insert(0,'Type','Twitter') #Inserting Type = 'Twitter' at the Beginning of the Data

#Youtube
youtube = pandas.read_csv('review.csv',usecols = colnames) 
youtube.insert(0,'Type','Youtube') #Inserting Type = 'Youtube' at Beginning of the Data

final_data = pandas.concat([tweets,youtube])
final_data.to_csv('Test.csv',index=False)
