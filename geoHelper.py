import shapefile
import urllib2
import json
from bisect import *

GOOGLE_GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json?address="

# Description: creates URL for Google geocoding API
# Parameter: String address
# Returns: String URL 
def create_geocoding_url(query):
  query = query.replace(" ", "+")
  query = query.replace("%20", "+")
  return GOOGLE_GEOCODING_URL + query

# Description: given a URL encoding with address it will return zipcode for the address
# Parameter: String URL
# Returns: int zipcode 
def retrieve_zipcode(query):
  serialized_data = urllib2.urlopen(query).read()
  data = json.loads(serialized_data)
  if data['status'] == 'OK':
    results = data['results'][0]
    address_comps = results["address_components"]
    zipcode = address_comps[len(address_comps) - 1]
    zipcode = zipcode['long_name']
    return zipcode
  else:
    return None

# Description: given an address it uses helper functions to return zipcode
# Parameter: String address 
# Returns: int zipcode
def query_address(address):
  return int(retrieve_zipcode(create_geocoding_url(address)))

# Description: loads and sorts shape data by zipcode (increasing order) given path to shape files
# Parameter: String path 
# Returns: sorted shape data (shapeRecords)
def load_shape_data(path):
  sf = shapefile.Reader(path)
  data = sf.shapeRecords()
  data.sort(key = lambda x: x.record[0])
  return data

# Description: create list of zipcode in sorted order (increasing order)
# Parameter: List of sorted shapeRecords
# Returns: List of zipcodes (ints)
def create_zip_list(data):
  zip_list = [int(obj.record[0]) for obj in data]
  return zip_list

# Description: finds index of shapeRecord associated with given zipcode
# Parameter: int zipcode and sorted List of zipcodes (ints)
# Returns: int index
def search_data(zipcode, zip_list):
    i = bisect_left(zip_list, zipcode)
    if i != len(zip_list) and zip_list[i] == zipcode:
      return i
    else:
      return -1

def main():
  print "STARTED!"


if __name__ == "__main__":
  main() 
    
