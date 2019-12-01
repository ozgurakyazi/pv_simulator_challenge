import pytest, pika, json
from rabbit_connector import RabbitConnector as RC

def test_connection():
	rc = RC(queue_name="test")
	assert type(rc.channel)==pika.adapters.blocking_connection.BlockingChannel
	rc.connection.close()

@pytest.mark.skip
def data_receive_callback(ch, method, properties, body):
	ch.basic_ack(delivery_tag=method.delivery_tag)
	data = json.loads(body)
	assert data["test_int"] == 10
	assert data["test_str"] == "pika.pika"
	ch.stop_consuming()

def test_send_receive():
	rc = RC(queue_name="test")
	
	data={
		"test_int":10,
		"test_str":"pika.pika"
	}
	rc.send_data(data)
	rc.start_listening(data_receive_callback)
	
	rc.connection.close()	