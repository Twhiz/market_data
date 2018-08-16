# -*- coding: utf-8 -*-
"""
Test Script for calling amadeus APIs
Flight Low-Fare Search and Flight Affiliate Search
Created on Wed Aug 15 17:45:05 2018
@author: Jonas Romer
"""
token  = '25uFQEkQe59YIRWJJzQEu3AWPnnZfGIE'

# FLIGHT LOW-FARE CALL FUNCTION
def flight_lowfare_call(data, token):
    # Prerequisites
    import requests
    
    # Input handling
    base_url = 'https://api.sandbox.amadeus.com/v1.2/flights/low-fare-search?'
    input_url = "&".join('{0}={1}'.format(k, v) for k, v in data.items())
    auth = "apikey=" + token
    endpoint = base_url + auth + "&" + input_url
    
    # Main request
    r = requests.get(endpoint)
    
    # Error Handling
    if r.status_code == 200:
        return(r.json())
    else:
        print('[!] [{0}] Server Error'.format(r.status_code))
        print(r.json()['message'])
        return None
    return None

# Main part
data_lowfare   = {'origin': 'ZRH', 'destination': 'LON', 'departure_date': '2018-12-25', 'currency': 'CHF'}
                # optional: 'return_date': '2018-12-27', 'arrive_by': '2018-12-25T16:30', 
                #           'return_by': '2018-12-27T1430', 'adults': 1, 'children': 1,
                #           'infants': 1, 'include_airlines': 'SAZ', 
                #           'exclude_airlines': 'DLH', 'nonstop': 'false', 'max_price': 980,
                #           'currency': 'CHF', 'travel_class': 'ECONOMY', 
                #           'number_of_results': 5
result_lowfare = flight_lowfare_call(data_lowfare, token)
print(result_lowfare['currency'])
print(result_lowfare['results'][1])


# FLIGHT AFFILIATE SEARCH CALL FUNCTION
    # Note: Only for some special connections available
def flight_affiliate_call(data, token):
    # Prerequisites
    import requests
    
    # Input handling
    base_url = 'https://api.sandbox.amadeus.com/v1.2/flights/affiliate-search?'
    input_url = "&".join('{0}={1}'.format(k, v) for k, v in data.items())
    auth = "apikey=" + token
    endpoint = base_url + auth + "&" + input_url
    
    # Main request
    r = requests.get(endpoint)
    
    # Error Handling
    if r.status_code == 200:
        return(r.json())
    else:
        print('[!] [{0}] Server Error'.format(r.status_code))
        print(r.json()['message'])
        return None
    return None

# Main part
data_affil   = {'origin': 'ZRH', 'destination': 'LIS', 'departure_date': '2018-12-25', 'currency': 'CHF'}
                # optional: 'return_date': '2018-12-27', 'adults': 1, 'children': 1,
                #           'infants': 1, 'include_merchants': 'SAZ', 
                #           'exclude_merchants': 'DLH', 'max_price': 980,
                #           'currency': 'CHF', 'mobile': false
result_affiliate = flight_affiliate_call(data_affil, token)
print(result_affiliate['meta'])
print(result_affiliate['request_id'])
print(result_affiliate['results'][1])

# Merge with flight_data.py
