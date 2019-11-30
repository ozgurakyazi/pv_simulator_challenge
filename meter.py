import pika          ## To be able to send messages in RabbitMQ
import time, json 
from datetime import datetime as dt
import numpy as np

class Meter():
	'''
	This class mocks the power comsumption  of a regular home. 
	It generates a random power value and sends it to the RabbitMQ broker, 
	where it will be further processed.
	
	server_ip = IP of the server to connect, default is localhost.
	queue_name = queue name of the RabbitMQ broker.
	random_seed = For reproducible results, seed for the random number.
	meter_range = range of the meter values to be sampled from a uniform distribution.
	'''
	def __init__(
			self,  server_ip="localhost",
			queue_name="pv", random_seed = None,
			meter_range=(0,9000)
		):

		self.queue_name = queue_name
		self.random_seed = random_seed
		self.meter_range = meter_range
		self.server_ip = server_ip

		np.random.seed(random_seed)
		
		self.setup_connection()


	def send_value(self,value,timestamp):
		'''
		Send the meter value with timestamp to the broker.
		'''
		data = {
			"meter_value":value,
			"timestamp":timestamp
		}

		self.channel.basic_publish(
			exchange="",
			routing_key=self.queue_name,
			body = json.dumps(data)
		)
	
	def read_value(self):
		'''
		Read and return meter value.
		'''

		return np.random.randint(*self.meter_range)

	def process_meter(self,timestamp):
		'''
		Read and send the value of the meter through the channel.
		'''
		m_value = self.read_value()
		self.send_value(m_value, timestamp)