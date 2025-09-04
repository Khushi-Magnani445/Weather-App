from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import csv
import time

# This is the default template for the template engine used by Flask

app = Flask(__name__)

# Class for Scraping weather data from weather.com 
class WeatherScraper:
    def __init__(self):
        
        # Base URL of weather.com website and headers for making HTTP requests
        self.base_url = "https://weather.com/weather/today/l/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    # Getting Weather Data from the website Or Scrapping
    def get_weather_data(self, city_code):
        try:
            url = self.base_url + city_code
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # Getting temperature
             
            """ <span data-testid="TemperatureValue" class="CurrentConditions--tempValue--zUBSz" 
             dir="ltr">74<span class="CurrentConditions--degreeSymbol--tzLy9">°</span><span>
             </span></span> """
             
            temp = soup.find('span', {'data-testid': 'TemperatureValue'})
            temperature = temp.text if temp else 'N/A'
            
            

            # Getting weather condition
            
            """
                <div data-testid="wxPhrase" class="CurrentConditions--phraseValue---VS-k">Smoke</div>
            """
            
            condition = soup.find('div', {'data-testid': 'wxPhrase'})
            weather_condition = condition.text if condition else 'N/A'

            # Getting humidity
            
            """
                <div class="ListItem--listItem--UuEqg WeatherDetailsListItem--WeatherDetailsListItem--HLP3I" 
                data-testid="WeatherDetailsListItem"><svg class="WeatherDetailsListItem--icon--A88ff Icon--icon--ySD-o 
                Icon--darkTheme--RWEd0" set="current-conditions" name="humidity" 
                theme="dark" data-testid="Icon" viewBox="0 0 24 24">
                <title>Humidity</title><path fill-rule="evenodd" d="M11.743 17.912a4.182 4.182 0 0 1-2.928-1.182 3.972 
                3.972 0 0 1-.614-4.962.743.743 0 0 1 .646-.349c.234 0 .476.095.66.275l4.467 
                4.355c.385.376.39.998-.076 1.275a4.216 4.216 0 0 1-2.155.588M11.855 4c.316 
                0 .61.14.828.395.171.2.36.416.562.647 1.857 2.126 4.965 5.684 4.965 8.73 0 
                3.416-2.85 6.195-6.353 6.195-3.505 0-6.357-2.78-6.357-6.195 0-3.082 
                2.921-6.406 4.854-8.605.242-.275.47-.535.673-.772A1.08 1.08 0 0 1 11.855 4"></path>
                </svg><div data-testid="WeatherDetailsLabel" 
                class="WeatherDetailsListItem--label--U+Wrx">Humidity</div><div data-testid="wxData" class="WeatherDetailsListItem--wxData--lW-7H">
                <span data-testid="PercentageValue">29%</span></div></div>
            """
            
            humidity = soup.find('span', {'data-testid': 'PercentageValue'})
            humidity_value = humidity.text if humidity else 'N/A'

            
            # Returning All the values with city code and timestamp
            return {
                'city_code': city_code,
                'temperature': temperature,
                'condition': weather_condition,
                'humidity': humidity_value,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        # Handling the Errors if in case requests fails
        except requests.RequestException as e:
            return {"error": f"Error fetching data: {str(e)}"}
        
    # Method To save the weather data into csv file    
    def save_to_csv(self, data, filename='weather_data.csv'):
        """
        Saving weather data to CSV file named weather_data.csv
        """
        try:
            with open(filename, 'a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                
                
                file.seek(0, 2)
                if file.tell() == 0:
                    
                    # Writing the header only if the file is empty
                    # Like   city_code | temperature | condition | humidity | timestamp
                    writer.writeheader()
                
                # Writing Row Data     
                writer.writerow(data)
                print(f"Data saved to {filename}")
        
        # Handling the error in case of any error occurring to save the data in csv        
        except IOError as e:
            print(f"Error saving to CSV: {str(e)}")
    

@app.route("/", methods=["GET", "POST"])
def home():
    weather_data = None

    if request.method == "POST":
        
# Getting the city code from the form and getting weather data by calling the method get_weather_data
        city_code = request.form.get("city_code")
        if city_code:
            
            # Making object of class WeatherScraper 
            # and calling methods for getting the data and saving it to the CSV file
            scraper = WeatherScraper()
            weather_data = scraper.get_weather_data(city_code)
            scraper.save_to_csv(weather_data)
    
    # Respecting the website by not sending the requests continuously and giving the time of 2 seconds        
    time.sleep(5)
    
    # Returning the weather data to the weather.html template for rendering
    return render_template("weather.html", weather=weather_data)


# Running the Flask Application
if __name__ == "__main__":
    app.run(debug=True)
