from crypto_bot.bot import CryptoBot
from crypto_bot.tests.test import test1, twitter_test
from crypto_bot.twitter_wizard import TwitterClient


def main():
	bot = CryptoBot()
	bot.start()
	#test1()
	#tc = TwitterClient()
	#tc.btc_sentiment_score()
	#score = btc_sentiment_score()
	#print("Score: ", score)



if __name__ == '__main__':
	main()
