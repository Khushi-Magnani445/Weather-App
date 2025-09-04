import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

class WeatherAnalyzer:
    def __init__(self, csv_file):
        # Reading the CSV file
        self.df = pd.read_csv(csv_file, encoding='utf-8', engine='python')


        # Converting timestamp to datetime
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        # Converting temperature strings to numeric values
        self.df['temperature'] = self.df['temperature'].str.replace('°', '').astype(float)
        # Converting humidity strings to numeric values
        self.df['humidity'] = self.df['humidity'].str.replace('%', '').astype(float)

    def temperature_trends(self):
        """
        Plotting temperature over time for all cities
        """
        plt.figure(figsize=(12, 6))
        for city in self.df['city_code'].unique():
            city_data = self.df[self.df['city_code'] == city]
            print(city_data)
            plt.plot(city_data['timestamp'], city_data['temperature'], marker='o', label=city)
        
        plt.title('Temperature Trends Over Time')
        plt.xlabel('Timestamp')
        plt.ylabel('Temperature (°F)')
        plt.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def humidity_distribution(self):
        """
        Creating box plots of humidity distribution by city
        """
        plt.figure(figsize=(10, 6))
        sns.boxplot(x='city_code', y='humidity', data=self.df)
        plt.title('Humidity Distribution by City')
        plt.xlabel('City')
        plt.ylabel('Humidity (%)')
        plt.tight_layout()
        plt.show()

    def temp_vs_humidity(self):
        """
        Creating scatter plot of temperature vs humidity
        """
        plt.figure(figsize=(10, 6))
        for city in self.df['city_code'].unique():
            city_data = self.df[self.df['city_code'] == city]
            plt.scatter(city_data['temperature'], city_data['humidity'], label=city, alpha=0.6)
        
        plt.title('Temperature vs Humidity')
        plt.xlabel('Temperature (°F)')
        plt.ylabel('Humidity (%)')
        plt.legend()
        plt.tight_layout()
        plt.show()

    def weather_conditions(self):
        """
        Creating bar plot of weather conditions frequency
        """
        plt.figure(figsize=(12, 6))
        condition_counts = self.df['condition'].value_counts()
        condition_counts.plot(kind='bar')
        plt.title('Frequency of Weather Conditions')
        plt.xlabel('Weather Condition')
        plt.ylabel('Count')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def summary_stats(self):
        """
        Generating summary statistics for each city
        """
        summary = self.df.groupby('city_code').agg({
            'temperature': ['mean', 'min', 'max', 'std'],
            'humidity': ['mean', 'min', 'max', 'std']
        }).round(2)
        
        return summary

    def daily_avg(self):
        """
        Plot daily average temperature and humidity
        """
        self.df['date'] = self.df['timestamp'].dt.date
        daily_avg = self.df.groupby(['date', 'city_code']).agg({
            'temperature': 'mean',
            'humidity': 'mean'
        }).reset_index()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

        for city in daily_avg['city_code'].unique():
            city_data = daily_avg[daily_avg['city_code'] == city]
            ax1.plot(city_data['date'], city_data['temperature'], marker='o', label=city)
            ax2.plot(city_data['date'], city_data['humidity'], marker='o', label=city)

        ax1.set_title('Daily Average Temperature')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Temperature (°F)')
        ax1.legend()
        ax1.tick_params(axis='x', rotation=45)

        ax2.set_title('Daily Average Humidity')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Humidity (%)')
        ax2.legend()
        ax2.tick_params(axis='x', rotation=45)

        plt.tight_layout()
        plt.show()


def main():
    analyzer = WeatherAnalyzer('weather_data.csv')
    
    # Generating and displaying all graphs
    analyzer.temperature_trends()
    analyzer.humidity_distribution()
    analyzer.temp_vs_humidity()
    analyzer.weather_conditions()
    analyzer.daily_avg()
    
    # Printing summary statistics
    print("\nSummary Statistics:")
    print(analyzer.summary_stats())

if __name__ == "__main__":
    main()