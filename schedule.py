import time
from threading import Thread
import logging
import atexit


class Scheduler:
	def __init__(self):
		self.logger = logging.getLogger(__name__)
		self.threads = []

	def add_and_start_loop_thread(self, func, timer=10, *args):
		self.logger.info("Added job with name: " + func.__name__)
		job = Thread(target=self.loop_with_timer, args=[func, None, timer, args])
		self.threads.append(job)
		self.threads[-1].start()

	def loop_with_timer(self, func, logger=None, timer=0, *args):
		last_status_err = False
		if logger is None:
			logger = self.logger
		while True:
			temp = last_status_err
			try:
				func(*args)
				time.sleep(timer)
				last_status_err = False
			except Exception as ex:
				last_status_err = True
				self.logger.debug(ex)
			if temp != last_status_err:
				if last_status_err:
					logger.warning(str(time.time()) + " Thread with name: " + func.__name__ + " has problem")
				else:
					logger.info(str(time.time()) + " Thread with name: " + func.__name__ + " is work")

	def stop_all(self):
		self.logger.info("Terminate threads:")
		for thread in self.threads:
			thread.join(500)
		self.logger.info("Terminate threads done!")
