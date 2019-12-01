import pika          ## To be able to send messages in RabbitMQ
import time, json 
from datetime import datetime as dt
import numpy as np
from rabbit_connector import RabbitConnector as RC
import shared_params as params

class Meter():
	'''
	This class mocks the power comsumption  of a regular home. 
	It generates a random power value and sends it to the RabbitMQ broker, 
	where it will be further processed.

	Random values are generated as follows:
		* Create and initial watt value in the __init__, between meter_range range,
		  and call it as last_watt.
		* For each read_value, add the uniformly generated random value
		  which is in the range [200,200] to the last_watt, and 
		  put the latest last_watt between the range meter_range.

	
	server_ip = IP of the server to connect, default is localhost.
	queue_name = queue name of the RabbitMQ broker.
	random_seed = For reproducible results, seed for the random number.
	meter_range = range of the meter values.
	'''
	def __init__(self, random_seed = None, meter_range=(0,9000)):
		
		self.random_seed = random_seed
		self.meter_range = meter_range

		np.random.seed(random_seed)
		self.last_watt = np.random.randint(*meter_range)
		self.rc = RC()


	def send_init(self, file_name, m_type=2):
		'''
		Sends a message to PV, to do the initial work.

		file_name: name of the file to write the data
		m_type: indicates type of message.
			  m_type == 1 => close the connection in the PV side.
			  m_type == 0 => leave connection open. 
			  m_type == 2 => do the initial work in the PV side.
		'''
		data = {
			"file_name":file_name,
			"m_type":m_type
		}
		self.rc.send_data(data)
	
	def send_value(self,value,timestamp,m_type):
		'''
		Send the meter value with timestamp to the broker.
		value: meter value sent to the broker.
		timestamp: timestamp of the meter value
		m_type: indicates type of message.
			  m_type == 1 => close the connection in the PV side.
			  m_type == 0 => leave connection open. 
			  m_type == 2 => do the initial work in the PV side.
		'''
		data = {
			"meter_value":value,
			"timestamp":timestamp,
			"m_type":m_type
		}
		self.rc.send_data(data)
	
	def read_value(self):
		'''
		Read and return meter value.
		'''
		## increase or decrease the last watt value read from the meter
		self.last_watt += np.random.randint(-200,201)

		## make the output between self.meter_range range.
		self.last_watt = max(min(self.last_watt,self.meter_range[1]), self.meter_range[0])
		return self.last_watt

	def process_meter(self,timestamp,m_type):
		'''
		Read and send the value of the meter through the channel.
		'''
		m_value = self.read_value()
		self.send_value(m_value, timestamp,m_type)