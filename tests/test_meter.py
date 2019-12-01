import pytest,json
from meter import Meter

def test_init():
	mt = Meter()
	assert type(mt.last_watt) == int

@pytest.mark.skip
def init_callback(ch, method, properties, body):
	ch.basic_ack(delivery_tag=method.delivery_tag)
	data = json.loads(body)
	assert data["file_name"]=="test_file.csv"
	assert data["m_type"]==2
	ch.stop_consuming()
def test_send_init():
	mt = Meter()
	mt.send_init(file_name="test_file.csv")

	mt.rc.start_listening(init_callback)
	mt.rc.connection.close()


def test_read_value():
	mt = Meter(meter_range=(0,500))
	mt_val = mt.read_value()
	assert (mt_val <=500 and mt_val>=0)

@pytest.mark.skip
def send_value_callback(ch, method, properties, body):
	ch.basic_ack(delivery_tag=method.delivery_tag)
	data = json.loads(body)
	assert data["meter_value"]==333
	assert data["timestamp"]=="timestamp-xyz"
	assert data["m_type"]==13
	ch.stop_consuming()
def test_send_value():
	mt = Meter()
	mt.send_value(333,"timestamp-xyz",13)

	mt.rc.start_listening(send_value_callback)
	mt.rc.connection.close()

