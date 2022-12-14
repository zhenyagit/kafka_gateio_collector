import json
import logging
import time
import os


class Data:
	def __init__(self, obj, currency_pair):
		self.obj = obj
		self.currency_pair = currency_pair
		self.time = time.time()
		self.add_time_to_data()

	def add_time_to_data(self):
		self.obj["time"] = self.time

	def get_currency_pair(self):
		return self.currency_pair

	def get_time(self):
		return self.time

	def __str__(self):
		return json.dumps(self.obj)


class Writer:
	def __init__(self):
		self.logger = logging.getLogger(__name__)

	def write(self, data: Data):
		self.logger.debug(data.currency_pair + " " + str(data.time) + " " + str(data))


class FileWriter(Writer):
	def __init__(self, path_to_folder):
		super().__init__()
		self.path_to_folder = path_to_folder
		self.check_folder(path_to_folder)

	def check_folder(self, path_to_folder):
		self.logger.debug("Check folder exist : %s", path_to_folder)
		if not os.path.exists(path_to_folder):
			self.logger.debug("Create folder : %s", path_to_folder)
			os.mkdir(path_to_folder)

	def write(self, data: Data):
		file_name = self.path_to_folder + "/" + str(data.time) + "-" + data.currency_pair + ".json"
		with open(file_name, 'w') as file:
			file.write(str(data))
