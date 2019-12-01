import pytest,json,os
from photovoltaic import Photovoltaic as PV
import pandas as pd
from datetime import datetime as dt
def test_init():
	pv =  PV()

	assert type(pv) == PV

def test_initial_work():
	pv =  PV()
	pv.initial_work("test_file.csv")
	pv.the_file.close()
	
	with open('./data/test_file.csv') as f:
		first_line = f.readline()

	
	assert first_line == ",Meter,PV,Total\n"
	os.remove("./data/test_file.csv")


def test_process_pv():
	pv =  PV()
	pv.initial_work("test_file.csv")
	data = {
		"meter_value":10,
		"timestamp": "2019/12/13 14:07:08",
		"m_type":0,
	}
	pv.process_pv(data)
	pv.the_file.close()
	
	test_df = pd.read_csv("./data/test_file.csv",index_col=0,parse_dates=True,infer_datetime_format=True)
	assert test_df.iloc[0].name == dt(2019,12,13,14,7,8)
	assert	test_df.iloc[0].Meter == 10
	assert	test_df.iloc[0].Meter + test_df.iloc[0].PV == test_df.iloc[0].Total
	os.remove("./data/test_file.csv")