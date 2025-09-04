from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime

app = Flask(__name__)

class WeatherScraper:
    def __init__(self):
        self.base_url = "https://weather.com/weather/today/l/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_weather_data(self, city_code):
        try:
            url = self.base_url + city_code
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Get temperature
            temp = soup.find('span', {'data-testid': 'TemperatureValue'})
            temperature = temp.text if temp else 'N/A'

            # Get weather condition
            condition = soup.find('div', {'data-testid': 'wxPhrase'})
            weather_condition = condition.text if condition else 'N/A'

            # Get humidity
            humidity = soup.find('span', {'data-testid': 'PercentageValue'})
            humidity_value = humidity.text if humidity else 'N/A'

            return {
                'temperature': temperature,
                'condition': weather_condition,
                'humidity': humidity_value,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except requests.RequestException as e:
            return {"error": f"Error fetching data: {str(e)}"}

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None

    if request.method == "POST":
        city_code = request.form.get("city_code")
        if city_code:
            scraper = WeatherScraper()
            weather_data = scraper.get_weather_data(city_code)

    return render_template("weather.html", weather=weather_data)

if __name__ == "__main__":
    app.run(debug=True)
