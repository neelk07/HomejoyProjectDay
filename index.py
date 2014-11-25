from flask import Flask
from flask import render_template
from flask import jsonify
from flask import g
from werkzeug.contrib.cache import SimpleCache
import geoHelper as geoHelper
import shapefile

#USING GLOBAL VARIABLES LOAD SHAPE DATA INTO MEMORY SINCE IT IS VERY LARGE
global data
global zip_list

app = Flask(__name__)

# Description: loads shape data and initial map view center in California
@app.route("/")
def index():
  global data
  global zip_list
  data = geoHelper.load_shape_data("data/tl_2014_us_zcta510")
  zip_list = geoHelper.create_zip_list(data)
  print "FINISHED LOADING SHAPE DATA INTO MEMORY....."
  return render_template('index.html')

# Description: query at /address/ADDRESS/ where we display zipcode area associated with ADDRESS
@app.route('/address/<address>')
def show_zipcode_area(address):
    global data
    global zip_list
    zipcode = geoHelper.query_address(address)
    if zipcode != None:
    	index = geoHelper.search_data(zipcode, zip_list)
        recShape = data[index]
    	zipcode = recShape.record[0]
    	lat = recShape.record[7]
    	lng = recShape.record[8]
    	coord_list = recShape.shape.points
   	return render_template('display.html', zipcode=zipcode, coord_list=coord_list, lat=lat, lng=lng)

if __name__ == "__main__":
  app.run(debug=True, port=8000)

