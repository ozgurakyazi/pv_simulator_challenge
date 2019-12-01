import pika, json

class RabbitConnector():
	'''
	Handles the connection operations in RabbitMQ. This is called by 
	Meter and PV class, and they get access to the same connection.
	'''

	def __init__(self, server_ip="localhost",queue_name="pv"):
		
		###  Connection Parameters
		self.server_ip = server_ip   # server of the broker
		self.queue_name = queue_name         # name of the queue/broker

		'''
		Sets up the connection and the queue with the name queue_name is created, so that
		we make sure the queue exists.
		'''
		self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.server_ip))
		self.channel = self.connection.channel()

		self.channel.queue_declare(queue=self.queue_name)
		

	def send_data(self, data):
		self.channel.basic_publish(
			exchange="",
			routing_key=self.queue_name,
			body = json.dumps(data)
		)

	def start_listening(self,method):
		self.channel.basic_consume(
			queue=self.queue_name, on_message_callback=method, auto_ack=False)

		### After this line, the sequential execution of the thread is blocked.!!
		### CAREFUL###
		self.channel.start_consuming()
