import requests


def get_algorithm_data():
	r = requests.get('https://api.neuryx.com/api/algorithm/btc')
	return r
