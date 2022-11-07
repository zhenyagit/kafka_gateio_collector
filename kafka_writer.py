import json
import logging

from additional import Writer, Data
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic


class KafkaAdmin:
	def __init__(self, servers=None):
		self.logger = logging.getLogger(__name__)
		if servers is None:
			self.servers = ['localhost:9092']
		else:
			self.servers = servers
		self.logger.info("Connect kafka admin to server : %s", str(self.servers))
		self.admin_client = KafkaAdminClient(
			bootstrap_servers=self.servers,
			client_id='admin_python')

	def add_topic(self, topic_name, num_partitions=1, replication_factor=1):
		self.logger.info("Create topic %s", topic_name)
		topic_list = [NewTopic(name=topic_name,
							   num_partitions=num_partitions,
							   replication_factor=replication_factor)]
		self.admin_client.create_topics(new_topics=topic_list, validate_only=False)


class KafkaWriter(Writer):
	def __init__(self, topic, servers=None):
		super().__init__()
		if servers is None:
			self.servers = ['localhost:9092']
		else:
			self.servers = servers
		self.topic = topic
		self.logger.info("Create producer to topic %s", topic)

		self.producer = KafkaProducer(bootstrap_servers=self.servers,
									  value_serializer=lambda m: json.dumps(m).encode('ascii'))
		if self.producer.bootstrap_connected():
			self.logger.info("Producer connected")
		else:
			self.logger.info("Producer not connected")
		self.logger.debug("Check topic %s exist", topic)
		logging.error("Connect to server %s", self.servers[0])
		self.check_topic_exist(topic)

	def write(self, data: Data):
		self.logger.debug("Write to Kafka at %s to topic %s data: %s", str(self.servers), self.topic, str(data))
		try:
			self.producer.send(self.topic, key=data.currency_pair.encode("ascii"), value=str(data))
		except Exception as ex:
			self.logger.error("Kafka Error while write to %s topic", self.topic)

	def wait_done(self):
		self.producer.flush()

	def topic_exist(self, topic=None):
		if topic is None:
			topic = self.topic
		consumer = KafkaConsumer(group_id='checker', bootstrap_servers=self.servers)
		topics = consumer.topics()
		print(topics)
		if topic in topics:
			return True
		else:
			return False

	def create_topic(self, topic_name):
		admin = KafkaAdmin(self.servers)
		admin.add_topic(topic_name)

	def check_topic_exist(self, topic):
		if not self.topic_exist(topic):
			self.create_topic(topic)


def demo():
	writer = KafkaWriter("candlesticks")
	writer.topic_exist()


if __name__ == "__main__":
	demo()
