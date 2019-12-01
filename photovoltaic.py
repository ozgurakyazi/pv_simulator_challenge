import pika
import numpy as np, json
from datetime import datetime as dt, time
from rabbit_connector import RabbitConnector
import shared_params as params

class Photovoltaic():
	'''
	Photovoltaic class. This class should generate (simulate) a power value
	based on an equation.
	'''
	
	def __init__(self):
		self.rc = RabbitConnector()

	def read_value(self,sample_dt):
		'''
		This should read (sample) a value from the PV power, which conforms the
		distribution in the pdf provided.

		To sample that value, first an approximate equation of the graph in the pdf is 
		extracted. Based on the time of the day, the value is 
		Then, a random value is generated in the range [-50,50] W, and added to the value
		got from the equation.
		'''

		## Generate the random value in W, then convert it to kW.
		rand_value = np.random.randint(-50,50+1)/1000.0 

		sample_time = sample_dt.time()

		## Extract the power value from the equation.
		if sample_time < time(5,30,0) :
			## First part of the graph, which is between 00:00 - 05:30
			## No power generation
			y = 0.0

		
		elif sample_time < time(8,20,0):
			## Linear power generation between 05:30-08:20
			x = sample_time.hour - 5.50
			x += sample_time.minute/60.0
			
			y = 0.11786*x + rand_value
			

		elif sample_time < time(19,50,0):
			
			## Power generation based on the curve in the middle, 08:20-19.50
			x = sample_time.hour - 14
			x += sample_time.minute/60.0
			
			y = (-0.09091 * x * x  +2.75 ) + 0.5   + rand_value



		elif sample_time < time(21,0,0) :
			## Linear power generation between 19:50-21:00
			x = sample_time.hour - 19.83333
			x += sample_time.minute/60.0
			
			y = -0.13379*x + 0.15653  + rand_value

		else:
			## No power generation after 21:00
			y = 0.0


		return y

	def queue_callback(self,ch, method, properties, body):
		'''
		Fired when a message is sent to the channel, if the channel is being listened
		'''
		ch.basic_ack(delivery_tag=method.delivery_tag)
		data = json.loads(body)
		print("Received:", data)
			
		if data["m_type"] == 0:
			## Do a normal processing.
			self.process_pv(data)

		elif  data["m_type"] == 2:
			## Do the initial tasks
			self.initial_work(data["file_name"])

		elif data["m_type"] == 1:
			## Stop waiting for consuming. The session is over.
			self.rc.channel.stop_consuming()
			self.the_file.close()

	def listen_queue(self):
		## Starts listening the queue
		self.rc.start_listening(self.queue_callback)


	def initial_work(self,file_name):
		'''
		Initial work is done here.
			* The file with the file_name under ./data folder is created
			with the header for csv file.
		'''
		self.the_file = open("./data/"+file_name, "w+")
		self.the_file.write(",Meter,PV,Total\n")
		self.the_file.flush()

	def process_pv(self,data):
		m_value = data["meter_value"]
		m_dt = dt.strptime(data["timestamp"],params.datetime_format)
		pv_value = self.read_value(m_dt)*1000.0
		total_value = m_value + pv_value
		write_str = data["timestamp"] +"," +str(m_value) + ","+str(pv_value) + "," + str(total_value)
		self.the_file.write(write_str + "\n")
		#self.the_file.flush()