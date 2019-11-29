import pika          ## To be able to send messages in RabbitMQ
import time
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
	def setup_connection(self):
		'''
		Sets up the connection and the queue with the name queue_name is created, so that
		we make sure the queue exists.
		'''
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.server_ip))
		self.channel = self.connection.channel()

		self.channel.queue_declare(queue=self.queue_declare)

	def send_value(self,value,timestamp):
		pass
	
	def read_value(self):
		'''
		Read and return meter value.
		'''

		return np.random.randint(*self.meter_range)

	self process_meter(self,timestamp):
		m_value = self.read_value()
		self.send_value(m_value, timestamp)