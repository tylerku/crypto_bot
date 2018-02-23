import time
import os
from subprocess import call
import datetime
from .twilio_wizard import send_notification
from .api_wizard import get_algorithm_data

class CryptoBot(object):

	def __init__(self):#, simulation=True, investment=500):
		pass

	def make_noise(self, hint):
		call(['say', hint + ' bitcoin on neurex'])


	def start(self):

		prev_hint = None
		start_investment = 500
		current_investment = start_investment
		current_investment_btc_price = None
		start_investment_btc_price = None
		print("Initial investment: ", start_investment)

		while(True):

			# Get data from API

			r = get_algorithm_data()
			res = r.json()
			algorithm_data = res['data']

			# Calculate Neuryx Strength Index
			neuryx_hint = None
			score_sum = 0
			score_count = 0
			current_price = algorithm_data[0]['price']
			neuryx_strength_index = None

			# Remember the initial investment price
			if start_investment_btc_price == None:
				start_investment_btc_price = float(current_price)


			for alg_data in algorithm_data:
				if alg_data['rsi'] != "0":
					score_sum += float(alg_data['rsi'])
					score_count += 1
			neuryx_strength_index = score_sum / score_count

			current_percent_gain = None 
			current_dollar_gains = None 
			dollar_gains_from_start = None 
			percent_gain_from_start = None

			if neuryx_strength_index > 40 and neuryx_strength_index < 60:
				neuryx_hint = "KEEP"
			elif neuryx_strength_index >= 60 and neuryx_strength_index < 80:
				if neuryx_hint == "SELL" or neuryx_hint == None:
					time.sleep(5)
					continue
				neuryx_hint = "SELL"
				current_percent_gain = (float(current_price) / current_investment_btc_price - 1) # as a decimal
				current_dollar_gains = current_investment * current_percent_gain
				current_investment_btc_price = None
				dollar_gains_from_start = (current_investment - start_investment) + current_dollar_gains
				percent_gain_from_start = (dollar_gains_from_start + start_investment) / start_investment - 1
				current_investment += current_dollar_gains
			elif neuryx_strength_index <= 40 and neuryx_strength_index > 20:
				if neuryx_hint == "BUY":
					time.sleep(5)
					continue
				neuryx_hint = "BUY"
				if current_investment_btc_price == None:
					current_investment_btc_price = float(current_price)
				current_percent_gain = (float(current_price) / current_investment_btc_price - 1) # as a decimal
				current_dollar_gains = current_investment * current_percent_gain
				dollar_gains_from_start = (current_investment - start_investment) + current_dollar_gains
				percent_gain_from_start = (dollar_gains_from_start + start_investment) / start_investment - 1
			elif neuryx_strength_index >= 80:
				neuryx_hint = "OVERBOUGHT"
			elif neuryx_strength_index <= 20:
				neuryx_hint = "OVERSOLD"


			if prev_hint != neuryx_hint and (neuryx_hint == "BUY" or neuryx_hint == "SELL") and :
				print(neuryx_hint, "on Neuryx")
				print("% Gain on current investment: ", current_percent_gain * 100, "%")
				print("Dollar Gains from current investment: $", current_dollar_gains)
				print("% Gain From Beginning: ", percent_gain_from_start * 100, "%")
				print("Dollar Gains From Beginning: $", dollar_gains_from_start)
				print(" ")

				prev_hint = neuryx_hint
				self.make_noise(neuryx_hint)
				#send_notification(neuryx_hint, neuryx_strength_index)
				# hook up to GDAX API here for automation

			# Only check every 5 seconds
			time.sleep(5)

