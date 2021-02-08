-- weather and usage
sql_hw = select 
    extract(date from start_date) as startDate, 
    weather.maxTempC, 
    count(*) as trips 
    from 
    `bikeshare-303620.TripsDataset.Ridership` as rides, 
    `bikeshare-303620.TripsDataset.HistoricalWeather` as weather 
    where rides.location_id = 2 and weather.location_id = 2 and
    extract(quarter from start_date) = 3 and 
    extract(date from rides.start_date) = extract(date from weather.forecast_date) 
    group by startDate, maxTempC 
    order by startDate


-- popular time of day
select 
  start_date,
  extract(hour from start_date) as start_hour,
  rides.location_id,
  count(extract(hour from start_date)) as hourly_trip_count,
from `bikeshare-303620.TripsDataset.Ridership` as rides
where rides.location_id = 2 and
  start_date between '2019-01-01' and '2019-12-31'
group by start_date, start_hour, location_id;

-- top 5 destination stations
with activeStations as 
  (select station_id, station_name, count(end_station_id) as trip_count, stations.location_id as location_id
    from `bikeshare-303620.TripsDataset.Ridership` as rides,
    `bikeshare-303620.TripsDataset.Stations` as stations
    where rides.location_id = 2 and stations.location_id = 2
    and rides.end_station_id = stations.station_id
    group by station_id, station_name, location_id
    order by trip_count desc
    limit 5) 
select extract(dayofweek from start_date) as weekday, station_name, station_id, count(*) as trip_count
from `bikeshare-303620.TripsDataset.Ridership` as rides,
     activeStations stns
where rides.location_id = 2 and stns.location_id = 2
and rides.end_station_id = stns.station_id
and extract(date from start_date) between '2019-01-01' and '2019-01-31'
group by weekday, station_name, station_id
order by weekday, station_name
  
-- average trip duration
select avg(trip_duration) as avg_trip_duration,
       min(trip_duration) as min_trip_duration,
       max(trip_duration) as max_trip_duration,
       location_id
from `bikeshare-303620.TripsDataset.Ridership` as rides
group by location_id;


-- where do people go given starting station
select end_station_id, station_name, count(end_station_id) as endCount 
from `bikeshare-303620.TripsDataset.Ridership` rides,
    `bikeshare-303620.TripsDataset.Stations` stations
where 
  stations.location_id = 2 and 
  rides.location_id = 2 and
  start_station_id = 77 and
  rides.end_station_id = stations.station_id
-- and  extract(month from start_date) = 8
group by end_station_id, station_name
