import pika
import numpy as np, json
from datetime import datetime as dt, time
from rabbit_connector import RabbitConnector

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

		sample_time = sample_dt.to_pydatetime().time()

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
		data = json.loads(body)
		print("Received:", data)
		if data["done"] == 1:
			self.rc.channel.basic_cancel(None)
			self.rc.channel.stop_consuming()

	def listen_queue(self):
		self.rc.start_listening(self.queue_callback)