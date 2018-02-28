import time
import os
from subprocess import call
import datetime

from crypto_bot.twilio_wizard import send_notification
from crypto_bot.api_wizard import get_algorithm_data, get_price_data
from crypto_bot.logger import log_output, clear_output_log

class CryptoBot(object):

	def __init__(self):#, simulation=True, investment=500):
		pass

	def make_noise(self, hint):
		call(['say', hint + ' bitcoin on neurex'])


	def start(self):

		r = get_algorithm_data()
		res = r.json()
		algorithm_data = res['data']

		prev_hint = None
		start_investment = 500
		current_investment = start_investment
		current_investment_btc_price = None
		start_investment_btc_price = None
		hint = None

		BUY_RSI = 45
		SELL_RSI = 55
		OVERBOUGHT_RSI = 80
		OVERSOLD_RSI = 20

		clear_output_log()
		log_output("Initial investment: ", start_investment)
		log_output("Initial price: ", algorithm_data[0]['price'])
		log_output("Start Time: ", (datetime.datetime.now()))
		log_output("\n")

		while(True):

			# Get data from API
			alg_data = get_algorithm_data()
			alg_res = alg_data.json()

			price_data = get_price_data()
			price_res = price_data.json()

			# Calculate Strength Index
			score_sum = 0
			score_count = 0
			strength_index = None

			# Catch errors from bad data to avoid crash
			try:
				current_price = price_res['btc_price']['price']
				algorithm_data = alg_res['data']
				for alg_data in algorithm_data:
					if alg_data['rsi'] != "0":
						score_sum += float(alg_data['rsi'])
						score_count += 1
				strength_index = score_sum / score_count
				#log_output("BTC PRICE: ", current_price)
				#log_output("RSI: ", strength_index)
			except KeyError:
				log_output("KeyError, trying again...")
				time.sleep(5)
				continue
			except:
				log_output("Caught an unknown error type...")
				time.sleep(5)
				continue

			# Remember the initial investment price
			if start_investment_btc_price == None:
				start_investment_btc_price = float(current_price)

			current_percent_gain = None
			current_dollar_gains = None
			dollar_gains_from_start = None
			percent_gain_from_start = None

			if strength_index > BUY_RSI and strength_index < SELL_RSI:
				if hint == "KEEP":
					time.sleep(5)
					continue
				hint = "KEEP"
			elif strength_index >= SELL_RSI and strength_index < OVERBOUGHT_RSI:
				if hint == "SELL" or current_investment_btc_price == None:
					time.sleep(5)
					continue
				hint = "SELL"
				log_output(hint, " Bitcoin! Price:", current_investment_btc_price, " Time: ", datetime.datetime.now())
				current_percent_gain = (float(current_price) / current_investment_btc_price - 1) # as a decimal
				current_dollar_gains = current_investment * current_percent_gain
				current_investment_btc_price = None
				dollar_gains_from_start = (current_investment - start_investment) + current_dollar_gains
				percent_gain_from_start = (dollar_gains_from_start + start_investment) / start_investment - 1
				current_investment += current_dollar_gains
			elif strength_index <= BUY_RSI and strength_index > OVERSOLD_RSI:
				if hint == "BUY":
					time.sleep(5)
					continue
				log_output("BUY")
				hint = "BUY"
				if current_investment_btc_price == None:
					current_investment_btc_price = float(current_price)
				log_output(hint, " Bitcoin! Price:", current_investment_btc_price, " Time: ", datetime.datetime.now())
				current_percent_gain = (float(current_price) / current_investment_btc_price - 1) # as a decimal
				current_dollar_gains = current_investment * current_percent_gain
				dollar_gains_from_start = (current_investment - start_investment) + current_dollar_gains
				percent_gain_from_start = (dollar_gains_from_start + start_investment) / start_investment - 1
			elif strength_index >= OVERBOUGHT_RSI:
				hint = "OVERBOUGHT"
			elif strength_index <= OVERSOLD_RSI:
				hint = "OVERSOLD"


			if prev_hint != hint and (hint == "BUY" or hint == "SELL"):
				log_output("% Gain on current investment: ", current_percent_gain * 100, "%")
				log_output("Dollar Gains from current investment: $", current_dollar_gains)
				log_output("% Gain From Beginning: ", percent_gain_from_start * 100, "%")
				log_output("Dollar Gains From Beginning: $", dollar_gains_from_start)

				prev_hint = hint
				#self.make_noise(hint)
				#send_notification(hint, strength_index)
				# hook up to GDAX API here for automation

			# Only check every 5 seconds
			time.sleep(5)
