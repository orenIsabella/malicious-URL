#!/usr/bin/env python

##############################################
# Author: Nitay Hason
# Collect DNS data by url csv file
##############################################

import time
import datetime
import schedule
import threading
import argparse
import pandas as pd
from Tools.CollectDNS import CollectDNS

parser = argparse.ArgumentParser()
parser.add_argument('-i','--csv_in', help='<Required>CSV input file datatset')
parser.add_argument('-o','--csv_out', help='<Required>CSV output file datatset')
parser.add_argument('-d','--dataframe', help='Dataframe save file')
parser.add_argument('-l','--log_file', help='Log file')

def getCurrentDayTime():
	now = datetime.datetime.now()
	return now.strftime("%Y-%m-%d %H:%M:%S")

def run(collector,frm=""):
	print("Run " + frm)
	print(getCurrentDayTime())
	try:
		t1 = threading.Thread(target=collector.startSniff)
		t1.daemon = True
		t1.start()
		t1.join()
	finally:
		collector.saveData()
		print("Saved Data after run")

def morning(collector):
	t = threading.Thread(target=run,args=(collector,"Morning",))
	t.daemon = True
	t.start()

def noon(collector):
	t = threading.Thread(target=run,args=(collector,"Noon",))
	t.daemon = True
	t.start()

def evening(collector):
	t = threading.Thread(target=run,args=(collector,"Evening",))
	t.daemon = True
	t.start()


args      = parser.parse_args()

csv_in = "D:/Users/Daniel/Projects/malicious-URL/robust-malicious-url-detection-master/Datasets/urls/maliciousURLS2020.csv"
csv_out = "D:/Users/Daniel/Projects/malicious-URL/robust-malicious-url-detection-master/Datasets/features_extractions/test/collectDnsTest.csv"
df = "D:/Users/Daniel/Projects/malicious-URL/robust-malicious-url-detection-master/Datasets/features_extractions/test/a.txt"
log_file = "D:/Users/Daniel/Projects/malicious-URL/robust-malicious-url-detection-master/Datasets/features_extractions/test/b.txt"

log_file  = "log_file_tmp.log" if log_file is None else log_file
df        = pd.read_csv(csv_in, sep=";", header=None)
collector = CollectDNS(df, output=csv_out, domains_tmp='domains_tmp.json', log_file=log_file)

print("Number of malicious %d" % df.shape[0])
schedule.every().day.at("06:00").do(morning,collector)
schedule.every().day.at("14:00").do(noon,collector)
schedule.every().day.at("22:00").do(evening,collector)

t = threading.Thread(target=run,args=(collector,"Start",))
t.daemon = True
t.start()

try:
	while 1:
		schedule.run_pending()
		time.sleep(1)
except Exception as exp:
	print(exp)
	print("Save Data")
	collector.saveData()
	# logging.error("Saved Data by Exception " + str(exp))
