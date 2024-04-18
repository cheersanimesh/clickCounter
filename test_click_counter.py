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

## testing the load_encodes function
def test_load_encodes(mock_csv_data, mock_csv_data_2):

	## running testcase -1
	with patch('builtins.open', mock_open(read_data=mock_csv_data)):
		encode_dict, decode_dict = load_encodes('fake_path.csv')
		
		assert encode_dict == {'https://google.com/': '31Tt55y'}
		assert decode_dict == {'31Tt55y': 'https://google.com/'}

	## running testcase -2
	with patch('builtins.open', mock_open(read_data=mock_csv_data_2)):
		encode_dict, decode_dict = load_encodes('fake_path.csv')
		
		assert encode_dict == {'https://google.com/': '31Tt55y'}
		assert decode_dict == {'31Tt55y': 'https://google.com/'}
        
## testing the load_decodes function
def test_load_decodes(mock_json_data):

    with patch('builtins.open', mock_open(read_data=mock_json_data)):
        result = load_decodes('fake_path.json')
        assert result == [
            {"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
        	{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
        ]

## testing the filter_clicks_by_year function
def test_filter_clicks_by_year():

	## creating dummy data for testing
	test_clicks = [
		{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-04-15", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2020-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/xxxx", "user_agent": "-", "timestamp": "", "referrer": "-", "remote_ip": "-"},
		{"bitlink": "http://bit.ly/xxxy", "user_agent": "-", "timestamp": "2020-02-15T00:00:00", "referrer": "-", "remote_ip": "-"}
	]
	result = filter_clicks_by_year(test_clicks, logging_object=logging)
	assert len(result) == 2
	assert result[0]['bitlink'] == "http://bit.ly/31Tt55y"
	assert result[1]['bitlink'] == "http://bit.ly/2kkAHNs"

def test_count_clicks():

	## Running testcase_1

	dummy_encode_dict_1 = {'https://google.com/': '31Tt55y'}
	dummy_decode_dict_1 = {'31Tt55y' : 'https://google.com/'}

	dummy_test_clicks_1 = [
			{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
	]
	result_1 = count_clicks(dummy_test_clicks_1, encodes = dummy_encode_dict_1, decode_dict= dummy_decode_dict_1,logging_object= logging)
	
	assert result_1 == {"https://google.com/": 1}

	## Running testcase_2

	dummy_test_clicks_2 = [
			{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/xxxbug1", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/xxxbug1", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/2kkAHNs", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
			{"bitlink": "http://bit.ly/31Tt55y", "user_agent": "-", "timestamp": "2021-02-15T00:00:00Z", "referrer": "-", "remote_ip": "-"},
	]

	dummy_encode_dict_2 = {'https://google.com/': '31Tt55y', 'https://twitter.com/': '2kkAHNs' }
	dummy_decode_dict_2 = {'31Tt55y' : 'https://google.com/', '2kkAHNs':'https://twitter.com/' }
	result_2 = count_clicks(dummy_test_clicks_2, encodes = dummy_encode_dict_2, decode_dict= dummy_decode_dict_2,logging_object= logging)
	
	assert result_2 == {"https://google.com/": 4, 'https://twitter.com/':3}
