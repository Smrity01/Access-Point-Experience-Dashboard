import pandas

colnames = ['Tweet','Location','Positive','Negative']
#Twitter
tweets = pandas.read_csv('tweety.csv',usecols = colnames)
tweets.insert(0,'Type','Twitter') #Inserting Type = 'Twitter' at the Beginning of the Data

#Youtube_Review
youtube_r = pandas.read_csv('review.csv',usecols = colnames) 
youtube_r.insert(0,'Type','Youtube') #Inserting Type = 'Youtube' at Beginning of the Data

#Youtube_Output
youtube_o = pandas.read_csv('output.csv',usecols = colnames) 
youtube_o.insert(0,'Type','Youtube') #Inserting Type = 'Youtube' at Beginning of the Data


final_data = pandas.concat([tweets,youtube_r])
final_data = pandas.concat([final_data,youtube_o])
final_data.to_csv('Test.csv',index=False)
