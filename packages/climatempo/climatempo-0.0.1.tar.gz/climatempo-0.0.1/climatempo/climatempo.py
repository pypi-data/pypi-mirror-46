import requests
import json

FORECAST_URI = "http://apiadvisor.climatempo.com.br/api/v1/forecast/locale/{0}/days/15?token={1}"
CURRENT_URI =  "http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{0}/current?token={1}"

class Climatempo():

    def __init__(self, api_key, city):
        self._api_key = api_key
        self._city = city
        
    def get_current_status(self):
        return json.loads(requests.get(CURRENT_URI.format(self._city,self._api_key)).text)

    def get_forecast(self):
        return json.loads(requests.get(FORECAST_URI.format(self._city, self._api_key)).text)
        
