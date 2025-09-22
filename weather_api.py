import requests

API_KEY = "35450d818349ea09eec734b071f38e26"
BASE_URL = "https://api.openweathermap.org/data/2.5/"

class WeatherAPI:
    def __init__(self):
        self.api_key = API_KEY

    def get_current_weather(self, city):

        try:
            url = f"{BASE_URL}weather?q={city}&appid={self.api_key}&units=metric"
            print(f"Fetching data: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") != 200:
                print(f"Error: {data.get('message')}")
                return None
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching current data: {e}")
            return None

    def get_forecast(self, city):

        try:
            url = f"{BASE_URL}forecast?q={city}&appid={self.api_key}&units=metric"
            print(f"Fetching data: {url}")
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data.get("cod") != "200":
                print(f"Error: {data.get('message')}")
                return None
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
