#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 03 17:01:14 2016
                                        Insight Data Engineering Code Challenge
The challenge is to get the calculate the average degree of a vertex in a Twitter hashtag graph for the last 60 seconds, and update this each time a new tweet appears. 
The main task is to calculate the average degree over a 60-second sliding window.


@author: Vybhavreddy KC
"""
""" Importing the essential libraries for python """

import simplejson,os
import pandas as pd 
from datetime import timedelta
    
    
""" Inputing the tweets.txt from the tweet_input folder and calculating the average degree"""    
def main():

    parent_dir = os.path.dirname(os.path.realpath('__file__'))
    input_file = parent_dir + r'/tweet_input/tweets.txt'
    output_file = parent_dir + r'/tweet_output/output.txt'
    calculate_average_degree(input_file,output_file)


unique_tags=list()
class Generate_tweetscore(object):
		
		""" 
             This class is generate the tweetscore to the hashtags according to the time it created
		Attributes:
                  tweet_time=time at which tweet is created
                  hashtags= hashtags present in the tweet
                  new_hashtags=A list to store the new hashtags from the new tweets
                  unique_tags= A global list to store the unique hashtags from the 60-second window
           Methods:
                   Score: to calculate the scores of the hashtags in each tweet
			
		"""

		def __init__(self, tweet_time,hashtags):
			self.tweet_time = tweet_time
			self.hashtags = hashtags
			self.length=len(hashtags)
			self.new_hashtags=[]
			global unique_tags 
			self.new_hashtags = list(set(hashtags)-set(unique_tags))
			if self.length != 1:
				unique_tags = unique_tags+self.new_hashtags
			self.newtags_length=len(self.new_hashtags)
		def score(self):
			self.scores=(self.length-1)*(self.newtags_length)+(self.newtags_length)*(self.length-self.newtags_length)   
			return (self.scores)
## to calculate the average_degree for the 60-second window
   
def calculate_average_degree(input_file,output_file):
	twitter_input = open(input_file,"r")
	f = open(output_file, 'w')
	f.close()
	
	total_tweet_time = list()
	total_hash = list()
     # Function to input the data from the input path     
	def inputfile(twitter_input):
		for line in twitter_input:        
			single_tweet = simplejson.loads(line)
			if 'created_at'in single_tweet:            
				if(len(single_tweet["entities"]['hashtags'])>0):
					hashtags=[]
					time_stamp = single_tweet['created_at']                
					hash_tags = single_tweet["entities"]['hashtags']
					total_tweet_time.append(time_stamp)
					for i in range(len(hash_tags)):
						hashtags.append(hash_tags[i]["text"])
					total_hash.append(hashtags) 
		return (pd.to_datetime(total_tweet_time),total_hash)

# function to calcualte average score of the hashtags

	def avg_score(score_val):
		return((score_val)/float(len(unique_tags)))
# function to write the output to the file 
  
	def write_file(score_val):
         with open(output_file,'a') as f:
             f.write("{0:.2f}\n".format((score_val)))

  
	Tweet_data=pd.DataFrame(columns=('Time_stamp','Hashtags'))
	Tweet_data.Time_stamp,Tweet_data.Hashtags=inputfile(twitter_input)
	#Tweet_data.Time_stamp=pd.to_datetime(Tweet_data.Time_stamp)
	Tweet_data=Tweet_data.sort_values('Time_stamp')
	Tweet_data.index = range(0,Tweet_data.shape[0])
			 
	prev_score = list()
	timeframe = pd.DataFrame(columns=('Time_stamp','Hashtags'))
	score_val = 0
	for j in range(Tweet_data.shape[0]):
		End_tag=Tweet_data.Time_stamp[j]
		Start = End_tag - timedelta(seconds=60)
		timeframe = timeframe.append(Tweet_data.loc[j])
		timeframe_window= timeframe[(timeframe['Time_stamp']>Start) & (timeframe['Time_stamp']<=End_tag)]
		if((timeframe.shape[0]-timeframe_window.shape[0])>0):
		   unique_tags[:] = []
		   score_val=0
		   timeframe = timeframe_window
		timeframe_window.index = range(0,timeframe_window.shape[0])
		for i in range(timeframe_window.shape[0]):
			temp_score=Generate_tweetscore(timeframe_window.Time_stamp[i],timeframe_window.Hashtags[i])
			score_val = temp_score.score() + score_val
		
		if (len(unique_tags) == 0):
			write_file(round(prev_score,2))  
		else:
			prev_score = avg_score(score_val)
			write_file(round(prev_score,2))

if __name__ == '__main__':
    main()
    
