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

    sql_prices= '''select location_id, member_type, plan, amount from `bikeshare-303620.TripsDataset.Pricing` '''
    pricing_df = pd.read_gbq(sql_prices, project_id=gcp_project, credentials=credentials, dialect='standard')
    # print(pricing_df)

    json_obj = pricing_df.to_json(orient = 'records')
    json_loads=json.loads(json_obj)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str


@app.route("/api/visualize/destinations/<startDate>/<endDate>")
def api_visualize_stops(startDate, endDate):
    
    cityID = 2
    print(startDate)
    print(endDate)

    sql_stops = f' with activeStations as ' \
        f'(select station_id, station_name, count(end_station_id) as trip_count, stations.location_id as location_id ' \
        f'from `bikeshare-303620.TripsDataset.Ridership` as rides, ' \
        f'`bikeshare-303620.TripsDataset.Stations` as stations ' \
        f'where rides.location_id = {cityID} and stations.location_id = {cityID} ' \
        f'and rides.end_station_id = stations.station_id ' \
        f'group by station_id, station_name, location_id ' \
        f'order by trip_count desc ' \
        f'limit 5) ' \
        f'select extract(dayofweek from start_date) as weekday, ' \
            f'station_name, station_id, count(*) as trip_count ' \
        f'from `bikeshare-303620.TripsDataset.Ridership` as rides, ' \
            f'activeStations stns ' \
        f'where rides.location_id = 2 and stns.location_id = 2 ' \
        f'and rides.end_station_id = stns.station_id ' \
        f'and extract(date from start_date) between "{startDate}" and "{endDate}" '  \
        f'group by weekday, station_name, station_id ' \
        f'order by weekday, station_name'

    print(sql_stops)

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
                  f'  between "{sDate}" and "{eDate}" ' \
                  f'  group by start_hour, location_id '
    
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
    sDate = '2019-01-01'
    eDate = '2019-12-31'

    sql_hw = f'select extract(date from start_date) as startDate, ' \
            f' weather.maxTempC, ' \
            f'count(*) as trips ' \
            f'from ' \
            f'`bikeshare-303620.TripsDataset.Ridership` as rides, ' \
            f'`bikeshare-303620.TripsDataset.HistoricalWeather` as weather ' \
            f'where rides.location_id = {hwLocID} and weather.location_id = {hwLocID} and' \
            f' extract(date from start_date) ' \
            f'   between "{sDate}" and "{eDate}" and' \
            f' extract(date from rides.start_date) = extract(date from weather.forecast_date) ' \
            f'group by startDate, maxTempC ' \
            f'order by startDate '

    print(sql_hw)

    hw_df = pd.read_gbq(sql_hw, project_id=gcp_project, credentials=credentials, dialect='standard')
    hweather = hw_df.to_json(orient='records')

    json_loads=json.loads(hweather)
    json_formatted_str = json.dumps(json_loads, indent=2)

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

    sql_rides = f'select extract(month from start_date) as startDate, ' \
                    f'end_station_id, station_name, ' \
                    f'count(end_station_id) as endCount ' \
                f'from `bikeshare-303620.TripsDataset.Ridership` rides, ' \
                     f'`bikeshare-303620.TripsDataset.Stations` stations ' \
                f'where stations.location_id = {locationID} and ' \
                    f'rides.location_id = {locationID} and ' \
                    f'start_station_id = {startStationIDvalue} and ' \
                    f'rides.end_station_id = stations.station_id and ' \
                    f'extract(month from start_date) = {monthValue} ' \
                f'group by startDate, end_station_id, station_name'

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

