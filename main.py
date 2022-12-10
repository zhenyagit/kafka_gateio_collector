import time

from additional import *
from download import *
from schedule import *
from kafka_writer import *
import logging
import os


def write_all(data, writers):
	for writer in writers:
		logging.debug("Write by %s", writer.__class__.__name__)
		writer.write(data)


def demo():
	pair = "XCH_USDT"
	downloader = GateIODownloader(pair)
	candle_writers = [Writer(), FileWriter("./candlesticks"), KafkaWriter("candlesticks", ["localhost:9092"])]
	moment_writers = [Writer(), FileWriter("./momentum"), KafkaWriter("momentum", ["localhost:9092"])]

	def func1():
		write_all(Data(downloader.load_candlesticks(interval="10s"), pair), candle_writers)

	def func2():
		write_all(Data(downloader.load_momentum(), pair), moment_writers)

	scheduler = Scheduler()
	scheduler.add_and_start_loop_thread(func1, 5)
	scheduler.add_and_start_loop_thread(func2, 1)


def main():
	if "DELAY" in os.environ:
		delay_until_broker_start = int(os.environ['DELAY'])
	else:
		delay_until_broker_start = 20
	if "KAFKA_HOSTNAME" in os.environ:
		kafka_hostname = os.environ['KAFKA_HOSTNAME']
	else:
		kafka_hostname = ["localhost:9092"]
	if "PAIRS" in os.environ:
		pairs = os.environ['PAIRS'].split(";")
	else:
		pairs = "XCH_USDT"

	downloaders = []
	for pair in pairs:
		downloaders.append(GateIODownloader(pair))

	logging.info("Wait %i seconds until broker start...", delay_until_broker_start)
	time.sleep(delay_until_broker_start)

	candle_writer = KafkaWriter("candlesticks", [kafka_hostname])
	moment_writer = KafkaWriter("trade_cup", [kafka_hostname])

	def download_write_all_c(down):
		candle_writer.write(Data(down[0].load_candlesticks(interval="10s"), down[0].pair))

	def download_write_all_m(down):
		moment_writer.write(Data(down[0].load_momentum(), down[0].pair))

	scheduler = Scheduler()
	for downloader in downloaders:
		scheduler.add_and_start_loop_thread(download_write_all_c, 5, downloader)
		scheduler.add_and_start_loop_thread(download_write_all_m, 1, downloader)


if __name__=="__main__":
	logging.basicConfig(level=logging.DEBUG)
	main()
