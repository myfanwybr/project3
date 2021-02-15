#import dependencies
from flask import Flask, jsonify, render_template, redirect, json, url_for, request
from google.oauth2 import service_account
import pandas as pd
import pandas_gbq
from datetime import datetime
import os


gcp_project = "bikeshare-303620"
bigquery_dataset = "TripsDataset"
bigquery_uri = f'bigquery://{gcp_project}/{bigquery_dataset}'


app=Flask(__name__)

# # the json credentials stored as env variable
# json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

# # generate json - if there are errors here remove newlines in .env
# json_data = json.loads(json_str)
# # the private_key needs to replace \n parsed as string literal with escaped newlines
# json_data['private_key'] = json_data['private_key'].replace('\\n', '\n')

# # use service_account to generate credentials object
# credentials = service_account.Credentials.from_service_account_info(json_data)
credentials = service_account.Credentials.from_service_account_file('bikeshare.json')

##front end routes
@app.route("/")
def main():
    return render_template("index.html")

@app.route("/pricing")
def prices():
    return render_template("pricing.html")

@app.route("/plots", methods=['GET','POST'])
def plots():
    cityNameIS = ""
    if request.method == "POST":
        cityNameIS = request.form["submit-button"]
        print(cityNameIS)
    else:
        return redirect("/")
        
    return render_template("visualize.html", cityNameIS = cityNameIS)

@app.route("/weather")
def historical():
    return render_template("h_weather.html")

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


@app.route("/api/visualize/destinations/<cityID>/<startDate>/<endDate>")
def api_visualize_stops(cityID, startDate, endDate):
    
    startDate = datetime.strptime(startDate, "%Y%m%d")
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = datetime.strptime(endDate, "%Y%m%d")
    endDate = endDate.strftime("%Y-%m-%d")

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
        f'where rides.location_id = {cityID} and stns.location_id = {cityID} ' \
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

@app.route("/api/visualize/time/<locID>/<startDate>/<endDate>")
def api_visualize(locID, startDate, endDate):
        
    startDate = datetime.strptime(startDate, "%Y%m%d")
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = datetime.strptime(endDate, "%Y%m%d")
    endDate = endDate.strftime("%Y-%m-%d")

    print(startDate)
    print(endDate)
    print(locID)

    # popular time of day
    sql_daytime = f'select extract(hour from start_date) as start_hour, ' \
                  f'      count(extract(hour from start_date)) as hourly_trip_count ' \
                  f' from `bikeshare-303620.TripsDataset.Ridership` ' \
                  f' where location_id = {locID} and ' \
                  f' extract(date from start_date) ' \
                  f'  between "{startDate}" and "{endDate}" ' \
                  f'  group by start_hour, location_id '
    
    print(sql_daytime)
    
    daytime_df = pd.read_gbq(sql_daytime, project_id=gcp_project, credentials=credentials, dialect='standard')
    # daytime = daytime_df.to_json(orient='records', date_format='iso')
    daytime = daytime_df.to_json(orient='records')

    json_loads=json.loads(daytime)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/visualize/weather/<hwLocID>/<startDate>/<endDate>")
def api_vizualize_weather(hwLocID, startDate, endDate):

    startDate = datetime.strptime(startDate, "%Y%m%d")
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = datetime.strptime(endDate, "%Y%m%d")
    endDate = endDate.strftime("%Y-%m-%d")

    print(hwLocID)
    print(startDate)
    print(endDate)

    sql_hw = f'select extract(date from start_date) as startDate, ' \
            f' weather.maxTempC, ' \
            f'count(*) as trips ' \
            f'from ' \
            f'`bikeshare-303620.TripsDataset.Ridership` as rides, ' \
            f'`bikeshare-303620.TripsDataset.HistoricalWeather` as weather ' \
            f'where rides.location_id = {hwLocID} and weather.location_id = {hwLocID} and' \
            f' extract(date from start_date) ' \
            f'   between "{startDate}" and "{endDate}" and' \
            f' extract(date from rides.start_date) = extract(date from weather.forecast_date) ' \
            f'group by startDate, maxTempC ' \
            f'order by startDate '

    print(sql_hw)

    hw_df = pd.read_gbq(sql_hw, project_id=gcp_project, credentials=credentials, dialect='standard')
    hweather = hw_df.to_json(orient='records')

    json_loads=json.loads(hweather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

#  ============ WEATHER =================
# get weather for specific city and date range
@app.route("/api/weather/<locationID>/<startDate>/<endDate>")
def api_weather_loc_date(locationID, startDate, endDate):

    startDate = datetime.strptime(startDate, "%Y%m%d")
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = datetime.strptime(endDate, "%Y%m%d")
    endDate = endDate.strftime("%Y-%m-%d")

    sql_weather = f'select forecast_date, maxTempC, humidity, total_precip, avg_cloudcover, avg_windspeed, location_id ' \
                    f'from `bikeshare-303620.TripsDataset.HistoricalWeather` ' \
                    f'where location_id = {locationID} ' \
                    f'and extract(date from forecast_date) between "{startDate}" and "{endDate}" ' \
                    f'order by forecast_date'
    weather_df = pd.read_gbq(sql_weather, project_id=gcp_project, credentials=credentials, dialect='standard')
    weather = weather_df.to_json(orient='records')

    json_loads=json.loads(weather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

# get weather for specific location
@app.route("/api/weather/<locationID>")
def api_weather_loc(locationID):

    sql_weather = f'select forecast_date, maxTempC, humidity, total_precip, avg_cloudcover, avg_windspeed, location_id ' \
                    f'from `bikeshare-303620.TripsDataset.HistoricalWeather` as weather ' \
                    f'where weather.location_id = coalesce({locationID}, weather.location_id) ' \
                    f'order by forecast_date'

    weather_df = pd.read_gbq(sql_weather, project_id=gcp_project, credentials=credentials, dialect='standard')
    weather = weather_df.to_json(orient='records')

    json_loads=json.loads(weather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

# get all weather information for all cities
@app.route("/api/weather")
def api_weather():
    # locationID = 1
    # startDate = '01/01/2019'
    # endDate = '12/31/2019'
    sql_weather = f'select forecast_date, maxTempC, humidity, total_precip, avg_cloudcover, avg_windspeed, location_id ' \
                    f'from `bikeshare-303620.TripsDataset.HistoricalWeather` order by location_id, forecast_date'
    weather_df = pd.read_gbq(sql_weather, project_id=gcp_project, credentials=credentials, dialect='standard')
    weather = weather_df.to_json(orient='records')

    json_loads=json.loads(weather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

# get weather for all cities within specific date range
@app.route("/api/weather/<startDate>/<endDate>")
def api_weather_dates(startDate, endDate):

    startDate = datetime.strptime(startDate, "%Y%m%d")
    startDate = startDate.strftime("%Y-%m-%d")

    endDate = datetime.strptime(endDate, "%Y%m%d")
    endDate = endDate.strftime("%Y-%m-%d")

    sql_weather = f'select forecast_date, maxTempC, humidity, total_precip, avg_cloudcover, avg_windspeed, location_id ' \
                    f'from `bikeshare-303620.TripsDataset.HistoricalWeather` ' \
                    f'where extract(date from forecast_date) between "{startDate}" and "{endDate}" ' \
                    f'order by location_id, forecast_date'
    weather_df = pd.read_gbq(sql_weather, project_id=gcp_project, credentials=credentials, dialect='standard')
    weather = weather_df.to_json(orient='records')

    json_loads=json.loads(weather)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/citymap/<locationID>/<startStationID>")
def api_citymap_stn(locationID, startStationID):

    sql_rides = f'select extract(month from start_date) as startDate, ' \
                    f'end_station_id, station_name, latitude, longitude,' \
                    f'count(end_station_id) as trips_count ' \
                f'from `bikeshare-303620.TripsDataset.Ridership` rides, ' \
                     f'`bikeshare-303620.TripsDataset.Stations` stations ' \
                f'where ' \
                    f'stations.location_id = {locationID}  and ' \
                    f'rides.location_id = {locationID}  and ' \
                    f'start_station_id = {startStationID} and ' \
                    f'rides.end_station_id = stations.station_id ' \
                f'group by startDate, end_station_id, station_name, latitude, longitude'

    stations_df = pd.read_gbq(sql_rides, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/citymap/<locationID>")
def api_citymap_loc(locationID):

    sql_rides = f'select extract(month from start_date) as startDate, ' \
                    f'end_station_id, station_name, latitude, longitude,' \
                    f'count(end_station_id) as trips_count ' \
                f'from `bikeshare-303620.TripsDataset.Ridership` rides, ' \
                     f'`bikeshare-303620.TripsDataset.Stations` stations ' \
                f'where ' \
                    f'stations.location_id = {locationID}  and ' \
                    f'rides.location_id = {locationID}  and ' \
                    f'rides.end_station_id = stations.station_id ' \
                f'group by startDate, end_station_id, station_name, latitude, longitude'

    stations_df = pd.read_gbq(sql_rides, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str


# get all end stations for all cities
@app.route("/api/citymap")
def api_citymap():

    sql_rides = f'select extract(month from start_date) as startDate, ' \
                    f'end_station_id, station_name, ' \
                    f'count(end_station_id) as trips_count ' \
                f'from `bikeshare-303620.TripsDataset.Ridership` rides, ' \
                     f'`bikeshare-303620.TripsDataset.Stations` stations ' \
                f'where ' \
                    f'rides.location_id = stations.location_id and ' \
                    f'rides.end_station_id = stations.station_id ' \
                f'group by startDate, end_station_id, station_name'

    stations_df = pd.read_gbq(sql_rides, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str


@app.route("/api/stations/<locationID>")
def api_stations_loc(locationID):

    sql_stations = f'select * from `bikeshare-303620.TripsDataset.Stations` ' \
                    f'where location_id = coalesce({locationID}, location_id)'
    print(sql_stations)
    stations_df = pd.read_gbq(sql_stations, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

@app.route("/api/stations")
def api_stations():

    sql_stations = f'select * from `bikeshare-303620.TripsDataset.Stations` ' 
    print(sql_stations)
    stations_df = pd.read_gbq(sql_stations, project_id=gcp_project, credentials=credentials, dialect='standard')
    stations_data = stations_df.to_json(orient='records')

    json_loads=json.loads(stations_data)
    json_formatted_str = json.dumps(json_loads, indent=2)

    return json_formatted_str

#run app
if __name__=="__main__":
    app.run(debug=True)

