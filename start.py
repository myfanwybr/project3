from .app import db

class Weather(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.HistoricalWeather'


class PricingIndex(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Pricing'



class BikeTrips(db.Model):
    __tablename__ = 'bikeshare-303620.TripsDataset.Ridership'