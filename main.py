import numpy as np
import json
import logging
import csv
import datetime
import os
import sys
from utils import load_encodes, load_decodes, filter_clicks_by_year, count_clicks


def main():
	encodes_path = 'data/encodes.csv'
	decodes_path = 'data/decodes.json'
	encodings = dict()
	decode_dict = dict()
	try:
		### Setting up the Logging Environment
		os.makedirs('LOGS', exist_ok=True)  
		currrent_time = datetime.datetime.now()
		logging.basicConfig(filename=f'LOGS/LOGS_{currrent_time}.txt', filemode='a',level=logging.DEBUG,format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s')
		
		encodings, decode_dict = load_encodes(encodes_path) ## creating a mapping between long_url and bithash

		decodes = load_decodes(decodes_path)   ## reading the load 
		filtered_clicks = filter_clicks_by_year(decodes, logging_object=logging)
		
		click_counts = count_clicks(filtered_clicks, encodings, logging_object= logging, decode_dict=decode_dict)

		# Sorting and formatting the output
		sorted_clicks = sorted(click_counts.items(), key=lambda item: item[1], reverse=True)
		formatted_output = [{item[0]: item[1]} for item in sorted_clicks]
		print(formatted_output)
    
	except Exception as e:
		logging.error(f"An error occurred: {e}")

if __name__=='__main__':
	main()