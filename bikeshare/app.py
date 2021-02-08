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


@app.route("/api/visualize/destination")
def api_visualize_stops():
    sql_stops = ""
    stops_df = pd.read_gbq(sql_stops, project_id=gcp_project, credentials=credentials, dialect='standard')
    json_obj = stops_df.to_json(orient = 'records')
    json_loads=json.loads(json_obj)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/visualize/time")
def api_visualize():
    
    cityname = "VANCOUVER"
    sDate = '2019-01-01'
    eDate = '2019-12-31'
    byQTR = 3

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
    sql_daytime = f'select extract(hour from start_date) as start_hour, ' \
                  f'      count(extract(hour from start_date)) as hourly_trip_count ' \
                  f' from `bikeshare-303620.TripsDataset.Ridership` ' \
                  f' where location_id = {locID} and ' \
                  f' extract(date from start_date) ' \
                  f'  between extract(date from {sDate}) and extract(date from {eDate}) ' \
                  f'  group by start_hour, location_id )'
    
    print(sql_daytime)
    
    daytime_df = pd.read_gbq(sql_daytime, project_id=gcp_project, credentials=credentials, dialect='standard')
    # daytime = daytime_df.to_json(orient='records', date_format='iso')
    daytime = daytime_df.to_json(orient='records')

    json_loads=json.loads(daytime)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/visualize/weather")
def api_vizualize_weather():
    hwLocID = 2
    byQTR = 1

    sql_hw = f'(select 
        extract(date from start_date) as startDate, 
        weather.maxTempC, 
        count(*) as trips 
        from 
        `bikeshare-303620.TripsDataset.Ridership` as rides, 
        `bikeshare-303620.TripsDataset.HistoricalWeather` as weather 
        where rides.location_id = {hwLocID} and weather.location_id = {hwLocID} and
        extract(quarter from start_date) = {byQTR} and 
        extract(date from rides.start_date) = extract(date from weather.forecast_date) 
        group by startDate, maxTempC 
        order by startDate )'

    print(sql_hw)

    hw_df = pd.read_gbq(sql_hw, project_id=gcp_project, credentials=credentials, dialect='standard')
    hweather = hw_df.to_json(orient='records')

    json_loads=json.loads(hweather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    print(json_formatted_str)

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

