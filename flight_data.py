# -*- coding: utf-8 -*-
"""
Test Script for calling the Instaflight API (SABRE)
Created on Wed May 16 10:21:00 2018

@author: sebastian.buechler
"""
#%% FUNCTIONS
# TOKEN CALL FUNCTION
def token_call():
    # Credentials
    client_id     = 'V1:ipfkapyu5odbsfz5:DEVCENTER:EXT'
    client_secret = 'mb5SY6Ki'
    
    # Prerequisites
    import requests
    import base64
    
    client_id_enc     = base64.b64encode(client_id.encode()).decode("utf-8")
    client_secret_enc = base64.b64encode(client_secret.encode()).decode("utf-8")    
    combined          = ":".join([client_id_enc, client_secret_enc])
    combined_enc      = base64.b64encode(combined.encode()).decode("utf-8")
    
    url     = 'https://api-crt.cert.havail.sabre.com/v2/auth/token'
    headers = {'Authorization': 'Basic ' + combined_enc}
    params  = {'grant_type': 'client_credentials'}
    
    # Token request
    r = requests.post(url, headers=headers, data=params)
    
    # Error Handling
    if r.status_code >= 500:
        print('[!] [{0}] Server Error'.format(r.status_code))
        return None
    elif r.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(r.status_code,url))
        return None  
    elif r.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(r.status_code))
        return None
    elif r.status_code == 400:
        print('[!] [{0}] Bad Request'.format(r.status_code))
        return None
    elif r.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(r.status_code))
        return None
    elif r.status_code == 200:
        return(r.json())
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(r.status_code, r.content))
    return None

# INSTAFLIGHT CALL FUNCTION
def instaflight_call(data, token):
    # Prerequisites
    import sys
    import requests
    
    # Input check
    if not 'origin' in data or not data['origin']:
        sys.exit('[!] No origin specified')
    if not 'destination' in data or not data['destination']:
        sys.exit('[!] No destination specified')
    if not 'departuredate' in data or not data['departuredate']:
        sys.exit('[!] No departure date specified')
        
    # Input handling
    headers = {'Authorization': 'Bearer ' + token[u'access_token']}
    base_url = 'https://api-crt.cert.havail.sabre.com/v1/shop/flights?'
    input_url = "&".join('{0}={1}'.format(k, v) for k, v in data.items())
    endpoint = base_url + input_url
    
    # Main request
    r = requests.get(endpoint, headers=headers)
    
    # Error Handling
    if r.status_code >= 500:
        print('[!] [{0}] Server Error'.format(r.status_code))
        return None
    elif r.status_code == 404:
        print('[!] [{0}] URL not found: [{1}]'.format(r.status_code,base_url))
        return None  
    elif r.status_code == 401:
        print('[!] [{0}] Authentication Failed'.format(r.status_code))
        return None
    elif r.status_code == 400:
        print('[!] [{0}] Bad Request'.format(r.status_code))
        return None
    elif r.status_code >= 300:
        print('[!] [{0}] Unexpected Redirect'.format(r.status_code))
        return None
    elif r.status_code == 200:
        return(r.json())
    else:
        print('[?] Unexpected Error: [HTTP {0}]: Content: {1}'.format(r.status_code, r.content))
    return None

# DATA EXTRACTION FUNCTION
def data_extraction(data):
    # Prerequisites
    import pandas as pd
    
    # Extract data
    prices_list         = [data['PricedItineraries'][x]['AirItineraryPricingInfo']['ItinTotalFare']['TotalFare']['Amount'] for x in range(len(data['PricedItineraries'])-1)]
    airline_list        = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment'][0]['OperatingAirline']['Code'] for x in range(len(data['PricedItineraries'])-1)]
    flight_number_list  = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment'][0]['OperatingAirline']['FlightNumber'] for x in range(len(data['PricedItineraries'])-1)]
    origin_list         = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment'][0]['DepartureAirport']['LocationCode'] for x in range(len(data['PricedItineraries'])-1)]
    destination_list    = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment'][-1]['ArrivalAirport']['LocationCode'] for x in range(len(data['PricedItineraries'])-1)]
    duration_list       = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['ElapsedTime'] for x in range(len(data['PricedItineraries'])-1)]
    nmb_segments_list   = [len(data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment']) for x in range(len(data['PricedItineraries'])-1)]
    departure_time_list = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment'][0]['DepartureDateTime'] for x in range(len(data['PricedItineraries'])-1)]
    arrival_time_list   = [data['PricedItineraries'][x]['AirItinerary']['OriginDestinationOptions']['OriginDestinationOption'][0]['FlightSegment'][-1]['ArrivalDateTime'] for x in range(len(data['PricedItineraries'])-1)]
    
    # Pandas dataframe
    flight_df                   = pd.DataFrame()
    flight_df['airline']        = airline_list
    flight_df['flight_number']  = flight_number_list
    flight_df['duration']       = duration_list
    flight_df['nmb_segments']   = nmb_segments_list
    flight_df['departure_time'] = departure_time_list
    flight_df['arrival_time']   = arrival_time_list
    flight_df['prices']         = pd.to_numeric(prices_list, errors='coerce')
    flight_df['origin']         = origin_list
    flight_df['destination']    = destination_list
    
    # Drop duplicates
    flight_df.drop_duplicates(inplace=True)
    
    return flight_df
 
#%% MAIN PART    
# Input 
data        = {
               'origin'                 : 'MUC',
               'destination'            : 'FRA',
               'departuredate'          : '2018-10-14',
               'returndate'             : '2018-10-17',
               'onlineitinerariesonly'  : 'N',
               'limit'                  : '200', 
               'offset'                 : '1' ,
               'eticketsonly'           : 'N',
               'sortby'                 : 'totalfare',
               'order'                  : 'asc',
               'sortby2'                :'departuretime',
               'order2'                 :'asc',
               'pointofsalecountry'     :'DE',
#               'outbounddeparturewindow': '06001600',
#               'inbounddeparturewindow' : '08002100',
               'passengercount'         : '1',
               'outboundflightstops'    : '1',
               'inboundflightstops'     : '1'
               }

# Call
token       = token_call()
result      = instaflight_call(data, token)
flight_df   = data_extraction(result)

# Output
print(flight_df.head())
flight_df.to_csv(path_or_buf='flight_data.csv')
