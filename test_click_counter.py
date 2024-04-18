import json
from utils import load_encodes, load_decodes, filter_clicks_by_year, count_clicks
import pytest
from unittest.mock import mock_open, patch
import logging

@pytest.fixture
def mock_csv_data():
	return 'long_url,domain,hash\nhttps://google.com/,bit.ly,31Tt55y'

@pytest.fixture
def mock_csv_data_2():
	return 'long_url,domain,hash\nhttps://google.com/,,31Tt55y'

@pytest.fixture
def mock_json_data():
    return json.dumps([
        {"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
        {"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"}
    ])

def test_load_encodes(mock_csv_data, mock_csv_data_2):
	with patch('builtins.open', mock_open(read_data=mock_csv_data)):
		encode_dict, decode_dict = load_encodes('fake_path.csv')
		
		assert encode_dict == {'https://google.com/': '31Tt55y'}
		assert decode_dict == {'31Tt55y': 'https://google.com/'}

	with patch('builtins.open', mock_open(read_data=mock_csv_data_2)):
		encode_dict, decode_dict = load_encodes('fake_path.csv')
		
		assert encode_dict == {'https://google.com/': '31Tt55y'}
		assert decode_dict == {'31Tt55y': 'https://google.com/'}
        

def test_load_decodes(mock_json_data):

    with patch('builtins.open', mock_open(read_data=mock_json_data)):
        result = load_decodes('fake_path.json')
        assert result == [
            {"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
        	{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
        ]

def test_filter_clicks_by_year():
	test_clicks = [
		{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"}
	]
	result = filter_clicks_by_year(test_clicks, logging_object=logging)
	assert len(result) == 2
	assert result[0]['bitlink'] == "http://bit.ly/31Tt55y"
	assert result[1]['bitlink'] == "http://bit.ly/2kkAHNs"

def test_count_clicks():
	test_clicks = [
			{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
	]

	encode_dict = {'https://google.com/': '31Tt55y'}
	decode_dict = {'31Tt55y' : 'https://google.com/'}
	result = count_clicks(test_clicks, encodes = encode_dict, decode_dict= decode_dict,logging_object= logging)
	
	assert result == {"https://google.com/": 1}
