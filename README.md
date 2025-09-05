# 🌦️ Python Weather App

A Python-based weather application that fetches **real-time weather data** using city codes through **web scraping**.  
The app analyzes trends, plots graphs, and stores weather data in a CSV file for further insights.

---

## 🚀 Features
- Fetches **live weather data** using city codes.  
- **Web scraping** powered (no paid API required).  
- Stores data in **CSV format** for easy tracking.  
- **Trend analysis & graph plotting** for visualization.  
- Simple CLI-based interface.

---



## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

git clone https://github.com/Khushi-Magnani445/Weather-App.git
cd weather-app
2️⃣ Create Virtual Environment (optional but recommended)

python -m venv venv
Activate it:

Windows (PowerShell):


.\venv\Scripts\activate
Mac/Linux:


source venv/bin/activate

3️⃣ Install Dependencies



python weather.py

📊 Example Output
Fetches and displays current weather for the given city code.

Stores the data in weather_data.csv.

Generates graphs (temperature trends, humidity, etc.).

📝 Notes
Ensure you have an active internet connection (for web scraping).

If you want to customize city codes, update them inside weather.py.

If you use .env for configs (optional), don’t forget to create a .env file with placeholders and keep it out of version control.

🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to improve.
