import requests
import logging

class SimpleDownloader:
	def __init__(self):
		self.logger = logging.getLogger(__name__)


	def load_candlesticks(self):
		pass

	def load_momentum(self):
		pass


class FileDownloader(SimpleDownloader):
	pass


class BinanceDownloader(SimpleDownloader):
	pass


class GateIODownloader(SimpleDownloader):
	def __init__(self, currency_pair='XCH_USDT'):
		super().__init__()
		self.pair = currency_pair
		self.candlesticks_intervals = ['10s', '5m', '1h', '1d']

	def default_request(self, url, params):
		host = "https://api.gateio.ws"
		prefix = "/api/v4"
		headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
		try:
			return requests.request('GET', host + prefix + url, params=params, headers=headers)
		except Exception as ex:
			self.logger.error(ex)

	def load_candlesticks(self, interval='10s', limit=180, pair=None):
		if pair is None:
			pair = self.pair
		url = '/spot/candlesticks'
		params = {'currency_pair': pair,
				  'interval': interval,
				  'limit': limit}
		return self.default_request(url, params).json()

	def load_momentum(self, limit=50, pair=None):
		if pair is None:
			pair = self.pair
		url = '/spot/order_book'
		params = {'currency_pair': pair,
				  'limit': limit}
		return self.default_request(url, params).json()

	def load_ticker_info(self, pair=None):
		if pair is None:
			pair = self.pair
		url = '/spot/tickers'
		params = {'currency_pair': pair}
		r = self.default_request(url, params)
		return r.json()[0]['last']


def demo():
	downloader = GateIODownloader("XCH_USDT")
	print(downloader.load_candlesticks())
	print(downloader.load_momentum())


if __name__ == '__main__':
	demo()
