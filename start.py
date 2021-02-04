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
        return '<Weather %r>' % (self.name)


class PricingIndex(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Pricing'
    price_id = db.Column(db.Integer)
    location_id = db.Column(db.Integer)
    member_type = db.Column(db.String)
    plan = db.Column(db.String)
    amount = db.Column(db.Float)


class Stations(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Stations'
    


class BikeTrips(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Ridership'