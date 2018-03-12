import re
import tweepy
from TwitterSearch import *
from textblob import TextBlob


class TwitterClient(object):
	def __init__(self):
		consumer_key = 'iKmbJDDiIrsELIXEksfRWjHQ4'
		consumer_secret = 'Hovdy12ejkjv3JXmr2iqzZYO1H4iSFbicHeE9AXj3A7eNtBoFt'
		access_token = '1146793141-1pS296FJkyWP5LOOuBTuE2PxsZlBSCjdoXiboY6'
		access_token_secret = 'CvCzhf8fqSZVj9bMw4Dk3jMbeMI0OFRSMrU6jRZDQvxjB'

		try: 
			self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)  
			self.api = tweepy.API(self.auth)
		except:
			print("TwitterClient Error: Authentication Failed")


	def get_tweets(self, keyword, count=10):
		'''
		Main function to fetch tweets and parse them.
		'''
		# empty list to store parsed tweets
		tweets = []

		try:
			# call twitter api to fetch tweets
			fetched_tweets = self.api.search(q = keyword, count = count)

			# parsing tweets one by one
			for tweet in fetched_tweets:
				# empty dictionary to store required params of a tweet
				parsed_tweet = {}

				# saving text of tweet
				parsed_tweet['text'] = tweet.text
				# saving sentiment of tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

				# appending parsed tweet to tweets list
				if tweet.retweet_count > 0:
					# if tweet has retweets, ensure that it is appended only once
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			# return parsed tweets
			return tweets

		except tweepy.TweepError as e:
			# print error (if any)
			print("Error : " + str(e))

	def clean_tweet(self, tweet):
		'''
		Utility function to clean tweet text by removing links, special characters
		using simple regex statements.
		'''
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		'''
		Utility function to classify sentiment of passed tweet
		using textblob's sentiment method
		'''
		# create TextBlob object of passed tweet text
		analysis = TextBlob(self.clean_tweet(tweet))
		# set sentiment
		if analysis.sentiment.polarity > 0:
			return 'positive'
		elif analysis.sentiment.polarity == 0:
			return 'neutral'
		else:
			return 'negative'

	def btc_sentiment_score(self):
		tweets = self.get_tweets(keyword = 'Bitcoin', count = 100)


		# picking positive tweets from tweets
		ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
		pos_percentage = len(ptweets)/len(tweets)
		# percentage of positive tweets
		#print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
		# picking negative tweets from tweets
		ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
		neg_percentage = len(ntweets)/len(tweets)
		neut_percentage = (len(tweets) - (len(ntweets) + len(ptweets)))/len(tweets)
		print("Neut: ", neut_percentage * 100)
		print("Pos: ", pos_percentage * 100)
		print("Neg: ", neg_percentage * 100)

		score = 50 + (pos_percentage * 100 / 5)  - neg_percentage * 100
		return score

		# percentage of negative tweets
		#print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
		# percentage of neutral tweets
		#print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
