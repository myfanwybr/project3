#import dependencies
from flask import Flask, jsonify, render_template, redirect, json, url_for, request
from config import gcp_project, bigquery_uri
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq


##demo dictionary

my_dict={
    1: "catherine", 
    2: "myfanwy", 
    3: "rubal", 
    4: "manisha", 
    5: "sharanvika"

}

app=Flask(__name__)

credentials = service_account.Credentials.from_service_account_file('bikeshare-303620-8579d23e955b.json')
projectID = 'bikeshare-303620'

##front end routes
@app.route("/")
def main():
    # print(f'project is {gcp_project}')
    # print(f'project is {bigquery_uri}')
    return render_template("index.html")

##service routes
@app.route("/prices")
def api_prices():

    sql_prices= '''select location_id, member_type, plan, amount from 'bikeshare-303620.TripsDataset.Pricing' '''
    pricing_df = pd.read_gbq(sql_prices, project_id=gcp_project, credentials=credentials, dialect='standard')
    # print(pricing_df)

    json_obj = pricing_df.to_json(orient = 'records')
    #json_obj = 'Prices for all'

    return jsonify(json_obj)

@app.route("/weather")
def api_weather():
    locationID = 2
    sql_weather = f'select * from `bikeshare-303620.TripsDataset.HistoricalWeather` where location_id = {locationID} limit 10'
    weather_df = pd.read_gbq(sql_weather, project_id=gcp_project, credentials=credentials, dialect='standard')
    weather = weather_df.to_json(orient='records')

    return jsonify(weather)


@app.route("/citymap")
def api_citymap():
    myCity = "xxxxxxx"
    return myCity

@app.route("/visualize")
def api_visualize():
    locationID = 2
    sql_trips = f'select * from `bikeshare-303620.TripsDataset.Ridership` where location_id = {locationID} limit 10'
    trips_df = pd.read_gbq(sql_trips, project_id=gcp_project, credentials=credentials, dialect='standard')
    trips = trips_df.to_json(orient='records')
    parsed = json.loads(trips)
    trip_parsed = json.dumps(parsed, indent=4)


    return jsonify(trip_parsed)
    #return render_template("visualize.html")

#run app
if __name__=="__main__":
    app.run(debug=True)

