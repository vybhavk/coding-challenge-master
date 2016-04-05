#Insight data challenge
This code has been written using python 2.7

Dependencies are
Importing the libraries pandas, os, datetime, simplejson 

SourceCode.py - coding-challenge-master/src/SourceCode.py

#Process to run the code
Run the run.sh file which has command python src/SourceCode.py

#Algorithm

Each Tweet is loaded and collected a data frame

Ensure that the tweets which fall outside the sixty second bracket are removed

Collect the unique tags and the New tags from each Tweet

Calculate the score of each hashtag and sum the score 

Compute the average degree score by dividing the total sum of scores from all the hashtags divided by the unique tags collected after applying the sixty second bracket
