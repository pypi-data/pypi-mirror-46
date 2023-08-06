class Config(object):
    DEBUG = False
    API_KEY = None   
    LATITUDE = None
    LONGITUDE = None
    UNITS = 'us'
    RAIN_THR = 0.3
    REFRESH_PERIOD = 15
    UPDATE_PERIOD = 29
    SENSOR_BLIND_MINUTES = 30
    GRAPH_HOURS = 18
    FORECAST_DAYS = 3

class DefaultConfig(Config):
    DEBUG = True

