import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

load_dotenv()

app = Flask(__name__)

# Configuration
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
OPENWEATHER_BASE_URL = 'https://api.openweathermap.org/data/2.5'

if not OPENWEATHER_API_KEY:
    raise ValueError('OPENWEATHER_API_KEY not found in environment variables')

class WeatherService:
    """Service to handle weather API calls"""
    
    @staticmethod
    def get_current_weather(city):
        """Fetch current weather for a city"""
        try:
            url = f'{OPENWEATHER_BASE_URL}/weather'
            params = {
                'q': city,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_forecast(city, days=5):
        """Fetch weather forecast for a city"""
        try:
            # First, get coordinates from city name
            geo_url = f'{OPENWEATHER_BASE_URL}/weather'
            params = {
                'q': city,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
            geo_response = requests.get(geo_url, params=params, timeout=10)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            lat = geo_data['coord']['lat']
            lon = geo_data['coord']['lon']
            
            # Get forecast
            forecast_url = f'{OPENWEATHER_BASE_URL}/forecast'
            forecast_params = {
                'lat': lat,
                'lon': lon,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric',
                'cnt': days * 8  # 8 forecasts per day (3-hour intervals)
            }
            forecast_response = requests.get(forecast_url, params=forecast_params, timeout=10)
            forecast_response.raise_for_status()
            return forecast_response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_air_quality(lat, lon):
        """Fetch air quality data"""
        try:
            url = f'{OPENWEATHER_BASE_URL}/air_pollution'
            params = {
                'lat': lat,
                'lon': lon,
                'appid': OPENWEATHER_API_KEY
            }
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {'error': str(e)}

class WeatherFormatter:
    """Format weather data for display"""
    
    @staticmethod
    def format_current_weather(data):
        """Format current weather data"""
        if 'error' in data:
            return data
        
        return {
            'city': data.get('name'),
            'country': data.get('sys', {}).get('country'),
            'temperature': data.get('main', {}).get('temp'),
            'feels_like': data.get('main', {}).get('feels_like'),
            'humidity': data.get('main', {}).get('humidity'),
            'pressure': data.get('main', {}).get('pressure'),
            'description': data.get('weather', [{}])[0].get('description'),
            'icon': data.get('weather', [{}])[0].get('icon'),
            'wind_speed': data.get('wind', {}).get('speed'),
            'wind_deg': data.get('wind', {}).get('deg'),
            'clouds': data.get('clouds', {}).get('all'),
            'sunrise': datetime.fromtimestamp(data.get('sys', {}).get('sunrise')).strftime('%H:%M:%S'),
            'sunset': datetime.fromtimestamp(data.get('sys', {}).get('sunset')).strftime('%H:%M:%S'),
            'visibility': data.get('visibility'),
            'rain': data.get('rain', {}).get('1h', 0)
        }
    
    @staticmethod
    def format_forecast(data):
        """Format forecast data"""
        if 'error' in data:
            return data
        
        forecast_list = []
        for item in data.get('list', []):
            forecast_list.append({
                'dt': datetime.fromtimestamp(item.get('dt')).strftime('%Y-%m-%d %H:%M'),
                'temp': item.get('main', {}).get('temp'),
                'feels_like': item.get('main', {}).get('feels_like'),
                'humidity': item.get('main', {}).get('humidity'),
                'pressure': item.get('main', {}).get('pressure'),
                'description': item.get('weather', [{}])[0].get('description'),
                'icon': item.get('weather', [{}])[0].get('icon'),
                'wind_speed': item.get('wind', {}).get('speed'),
                'clouds': item.get('clouds', {}).get('all'),
                'rain': item.get('rain', {}).get('3h', 0)
            })
        
        return {
            'city': data.get('city', {}).get('name'),
            'country': data.get('city', {}).get('country'),
            'forecast': forecast_list
        }

# Routes
@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/weather/current')
def get_current():
    """API endpoint for current weather"""
    city = request.args.get('city', 'London')
    weather_data = WeatherService.get_current_weather(city)
    formatted_data = WeatherFormatter.format_current_weather(weather_data)
    return jsonify(formatted_data)

@app.route('/api/weather/forecast')
def get_forecast():
    """API endpoint for weather forecast"""
    city = request.args.get('city', 'London')
    days = request.args.get('days', 5, type=int)
    forecast_data = WeatherService.get_forecast(city, days)
    formatted_data = WeatherFormatter.format_forecast(forecast_data)
    return jsonify(formatted_data)

@app.route('/api/weather/air-quality')
def get_air_quality():
    """API endpoint for air quality"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    
    if lat is None or lon is None:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    air_quality = WeatherService.get_air_quality(lat, lon)
    return jsonify(air_quality)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
