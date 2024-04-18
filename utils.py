import csv
import json

## function to load csv file and create a mapping between the long_url and bithash
def load_encodes(file_path):
	encodings=dict()
	decode_dict = dict()

	with open(file_path, newline='', encoding='utf-8') as csvfile:
		reader = csv.DictReader(csvfile)
		for row in reader:
			encodings[row['long_url']] = row['hash']
			decode_dict[row['hash']] = row['long_url']
	
	return encodings, decode_dict

## function to load json file consisting of click sessions
def load_decodes(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

## function to load json file consisting of click sessions
def filter_clicks_by_year(click_sessions,logging_object, year=2021):
    
	filtered_clicks =[]   ## object to store filtered clicks
    
	for session in click_sessions:
		try:
			session_year = session['timestamp'].split('-')[0]
			session_year = int(session_year)
			if(session_year== year):
				filtered_clicks.append(session)
		except:
				logging_object.info(f"invalid timestamp format--> {session['timestamp']}")
				continue

	return filtered_clicks


## function to count the number of clicks
def count_clicks(clicks, encodes,logging_object, decode_dict):
	count_dict = {hash: 0 for hash in encodes.keys()}
	for click in clicks:
		bithash = click['bitlink'].split('/')[-1]
		long_url = decode_dict.get(bithash)

		if long_url:      ## if long_url exists in decode_dict
			count_dict[long_url] += 1
		else:
			logging_object.info(f"encountered invalid bithash = {bithash} at timestamp --> {click['timestamp']}")
	return count_dict