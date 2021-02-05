from .app import db

class Weather(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.HistoricalWeather'
    location_id = db.Column(db.Integer)
    forecast_date = db.Column(db.DateTime)
    maxTempC = db.Column(db.Integer)
    humidity = db.Column(db.Float)
    total_precip = db.Column(db.Float)
    avg_cloudcover = db.Column(db.Float)
    avg_windspeed = db.Column(db.Float)

    def __repr__(self):
        return '<Weather %r>' % (self.location_id)


class PricingIndex(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Pricing'
    price_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    member_type = db.Column(db.String)
    plan = db.Column(db.String)
    amount = db.Column(db.Float)

    def __repr__(self):
        return '<Member Type %r>' % (self.member_type)


class Stations(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Stations'
    station_id = db.Column(db.Integer)
    station_name = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Station %r' % (self.station_name)


class BikeTrips(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Ridership'
    trip_duration = db.Column(db.Integer)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    start_station_id = db.Column(db.Integer)
    end_station_id = db.Column(db.Integer)
    bike_id = db.Column(db.Integer)
    member_type = db.Column(db.String)
    location_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Trip %r' % (self.location_id)
