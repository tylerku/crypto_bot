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
		investment = 500
		initial_price = None
		print("Initial investment: ", investment)

		while(True):

			# Get data from API

			r = get_algorithm_data()
			res = r.json()
			algorithm_data = res['data']

			# Calculate Neuryx Strength Index
			neuryx_hint = None
			score_sum = 0
			score_count = 0
			price = algorithm_data[0]['price']
			neuryx_strength_index = None

			# Set initial Price
			if initial_price == None:
				initial_price = float(price)

			percent_gain = float(((float(price) / initial_price) - 1) * 100)

			for alg_data in algorithm_data:
				if alg_data['rsi'] != "0":
					score_sum += float(alg_data['rsi'])
					score_count += 1
			neuryx_strength_index = score_sum / score_count

			if neuryx_strength_index > 40 and neuryx_strength_index < 60:
				neuryx_hint = "KEEP"
			elif neuryx_strength_index >= 60 and neuryx_strength_index < 80:
				neuryx_hint = "SELL"
			elif neuryx_strength_index <= 40 and neuryx_strength_index > 20:
				neuryx_hint = "BUY"
			elif neuryx_strength_index >= 80:
				neuryx_hint = "OVERBOUGHT"
			elif neuryx_strength_index <= 20:
				neuryx_hint = "OVERSOLD"

			if(prev_hint != neuryx_hint):
				print(neuryx_hint, "... Price: ", price, " Time: ", datetime.datetime.now())
				print("Percent Gain: ", percent_gain, "%... Dollar Gains: $",(investment * percent_gain * .01)) # ex. 2 = 2% and .01 = .01% of starting money
				print(" ")

				prev_hint = neuryx_hint
				#send_notification(neuryx_hint, neuryx_strength_index)
				self.make_noise(neuryx_hint)
				# hook up to GDAX API here for automation

			# Only check every 5 seconds
			time.sleep(5)

