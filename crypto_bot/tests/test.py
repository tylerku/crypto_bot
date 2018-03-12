from crypto_bot.gdax_wizard import test
from crypto_bot.twitter_wizard import TwitterClient

def test1():
	test()


def twitter_test():
    # creating object of TwitterClient Class
	#test_twitter()
    #api.test_update()

	# calling function to get tweets
	tweets = get_tweets(query = 'Bitcoin')

	# picking positive tweets from tweets
	ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
	# percentage of positive tweets
	print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
	# picking negative tweets from tweets
	ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
	# percentage of negative tweets
	print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
	# percentage of neutral tweets
	print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

	# printing first 5 positive tweets
	#print("\n\nPositive tweets:")
	#for tweet in ptweets[:10]:
	#    print(tweet['text'])

	# printing first 5 negative tweets
	# print("\n\nNegative tweets:")
	# for tweet in ntweets[:10]:
	#    print(tweet['text'])
