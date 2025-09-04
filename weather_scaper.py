import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time
import urllib.parse

class WeatherScraper:
    def __init__(self):
        self.base_url = "https://weather.com/weather/today/l/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def get_weather_data(self, city_code):
        """
        Scrape weather data for a given city code
        """
        try:
            url = self.base_url + city_code
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            print(response)
            print(response.text)
            print(response.url)
            
            
            
            
            # Get current temperature 
            """ <span data-testid="TemperatureValue" class="CurrentConditions--tempValue--zUBSz" 
             dir="ltr">74<span class="CurrentConditions--degreeSymbol--tzLy9">°</span><span>
             </span></span> """
             
            temp = soup.find('span', {'data-testid': 'TemperatureValue'})
            temperature = temp.text if temp else 'N/A'
            print(temp.text)
            
            # Get weather condition
            """
                <div data-testid="wxPhrase" class="CurrentConditions--phraseValue---VS-k">Smoke</div>
            """
            condition = soup.find('div', {'data-testid': 'wxPhrase'})
            weather_condition = condition.text if condition else 'N/A'
            
            # Get humidity
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
            
            return {
                
                'city_code': city_code,
                'temperature': temperature,
                'condition': weather_condition,
                'humidity': humidity_value,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except requests.RequestException as e:
            print(f"Error fetching data for {city_code}: {str(e)}")
            return None

    def save_to_csv(self, data, filename='weather_data.csv'):
        """
        Save weather data to CSV file
        """
        try:
            with open(filename, 'a', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=data.keys())
                
                # Write header if file is empty
                file.seek(0, 2)
                if file.tell() == 0:
                    writer.writeheader()
                    
                writer.writerow(data)
                print(f"Data saved to {filename}")
                
        except IOError as e:
            print(f"Error saving to CSV: {str(e)}")

def main():
    # Example city codes (you can find these in weather.com URLs)
    city_codes = {
        'New York': 'USNY0996',
        
    }
    
    scraper = WeatherScraper()
    
    # Scrape data for each city
    for city, code in city_codes.items():
        print(f"\nFetching weather data for {city}...")
        weather_data = scraper.get_weather_data(code)
        
        if weather_data:
            print(f"Weather in {city}:")
            print(f"Temperature: {weather_data['temperature']}")
            print(f"Condition: {weather_data['condition']}")
            print(f"Humidity: {weather_data['humidity']}")
            
            # Save to CSV
            scraper.save_to_csv(weather_data)
        
        # Add delay to be respectful to the website
        time.sleep(2)

if __name__ == "__main__":
    main()