#import dependencies
from flask import Flask, jsonify, render_template, redirect, json, url_for, request
from config import gcp_project, bigquery_uri
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
from os import environ

app=Flask(__name__)

credentials = service_account.Credentials.from_service_account_file('bikeshare-303620-f28d36859136.json')
projectID = 'bikeshare-303620'

##front end routes
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/pricing")
def prices():
    return render_template("pricing.html")

@app.route("/visualize")
def plot():
    return render_template("visualize.html")

@app.route("/weather")
def historical():
    return render_template("weather.html")

@app.route("/citymap")
def stations():
    return render_template("citymap.html")


##service routes
@app.route("/api/pricing")
def api_pricing():

    sql_prices= '''select * from `bikeshare-303620.TripsDataset.Pricing` '''
    pricing_df = pd.read_gbq(sql_prices, project_id=gcp_project, credentials=credentials, dialect='standard')
    # print(pricing_df)

    json_obj = pricing_df.to_json(orient = 'records')
    json_loads=json.loads(json_obj)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/visualize")
def api_visualize():
    
    cityname = "VANCOUVER"
    sDate = '2019-01-01'
    eDate = '2019-12-31'

    print(cityname)
    if cityname == "TORONTO":
        locID = 1
    elif cityname == "VANCOUVER":
        locID = 2
    elif cityname == "BOSTON":
        locID = 3
    else:
        locID = 4
    
    print(locID)

    # popular time of day
    sql_daytime = """select extract(hour from start_date) as start_hour, 
                        count(extract(hour from start_date)) as hourly_trip_count 
                    from `bikeshare-303620.TripsDataset.Ridership` 
                    where location_id = 2 and extract(month from start_date) = 2
                    group by start_hour, location_id limit 100"""

    xsql_daytime = """ select start_date, extract(hour from start_date) as start_hour, 
    location_id, count(extract(hour from start_date)) as hourly_trip_count 
    from `bikeshare-303620.TripsDataset.Ridership` where location_id = {locID}
    group by start_date, start_hour"""
    
    print(sql_daytime)
    
    daytime_df = pd.read_gbq(sql_daytime, project_id=gcp_project, credentials=credentials, dialect='standard')
    daytime = daytime_df.to_json(orient='records', date_format='iso')

    json_loads=json.loads(daytime)
    json_formatted_str = json.dumps(json_loads, indent=2)

    # sql_trips = f'select * from `bikeshare-303620.TripsDataset.Ridership` where location_id = {locationID} limit 10'
    # trips_df = pd.read_gbq(sql_trips, project_id=gcp_project, credentials=credentials, dialect='standard')
    # trips = trips_df.to_json(orient='records')

    # json_loads=json.loads(trips)
    # json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str


@app.route("/api/weather")
def api_weather():
    locationID = 1
    # startDate = '01/01/2019'
    # endDate = '12/31/2019'
    sql_weather = f'select * from `bikeshare-303620.TripsDataset.HistoricalWeather` where location_id = {locationID}'
    weather_df = pd.read_gbq(sql_weather, project_id=gcp_project, credentials=credentials, dialect='standard')
    weather = weather_df.to_json(orient='records')

    json_loads=json.loads(weather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/citymap")
def api_citymap():
    monthValue = 8
    startStationIDvalue = 77
    locationID = 2

    sql_rides = """select extract(month from start_date) as startDate, 
                    end_station_id, station_name, 
                    count(end_station_id) as endCount 
                from `bikeshare-303620.TripsDataset.Ridership` rides, 
                     `bikeshare-303620.TripsDataset.Stations` stations 
                where stations.location_id = {locationID} and 
                    rides.location_id = {locationID} and 
                    start_station_id = {startStationIDvalue} and 
                    rides.end_station_id = stations.station_id and 
                    extract(month from start_date) = {monthValue} 
                group by startDate, end_station_id, station_name"""

    stations_df = pd.read_gbq(sql_rides, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/stations")
def api_stations():

    sql_stations = f'select * from `bikeshare-303620.TripsDataset.Stations`'
    stations_df = pd.read_gbq(sql_stations, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

#run app
if __name__=="__main__":
    app.run(debug=True)

