-- weather and usage
select 
  start_date,
  rides.location_id,
  weather.maxTempC, 
  weather.forecast_date,
  count(*) as trips
from 
  `bikeshare-303620.TripsDataset.Ridership` as rides,
  `bikeshare-303620.TripsDataset.HistoricalWeather` as weather
where rides.location_id = 2 and
  start_date between '2019-01-01' and '2019-12-31' and
  date(extract(year from start_date), extract(month from start_date), extract(day from start_date)) =
  date(extract(year from forecast_date), extract(month from forecast_date), extract(day from forecast_date))
group by start_date, location_id, maxTempC, forecast_date
limit 100;


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

-- popular station
select start_station_id, 
       end_station_id,
       date(rides.start_date),
       station.location_id,
       count(*) as trips
from 
  `bikeshare-303620.TripsDataset.Ridership` as rides,
  `bikeshare-303620.TripsDataset.Stations` as station
where rides.start_station_id = station.station_id and
  rides.location_id = station.location_id 
group by start_station_id, end_station_id, date(start_date), location_id;
  
-- average trip duration
select avg(trip_duration) as avg_trip_duration,
       min(trip_duration) as min_trip_duration,
       max(trip_duration) as max_trip_duration,
       location_id
from `bikeshare-303620.TripsDataset.Ridership` as rides
group by location_id;
