# Weather Dashboard

A real-time weather dashboard application that fetches data from OpenWeatherMap API. Get current weather conditions, 5-day forecasts, and detailed meteorological information for any location worldwide.

## Features

✨ **Current Weather Display**
- Real-time temperature and "feels like" temperature
- Weather description and conditions
- Humidity, pressure, and wind speed
- Visibility and cloud coverage
- Sunrise and sunset times
- Weather icons and visual representation

📅 **5-Day Forecast**
- Hourly and daily weather forecasts
- Temperature trends
- Precipitation predictions
- Wind and humidity forecasts

🎨 **Beautiful UI**
- Modern, responsive design
- Mobile-friendly interface
- Smooth animations and transitions
- Dark theme with gradient backgrounds
- Interactive weather cards

⚡ **Performance**
- Fast API response times
- Efficient data formatting
- Optimized frontend rendering
- Caching support

## Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: OpenWeatherMap API
- **Server**: Gunicorn

## Prerequisites

- Python 3.8 or higher
- OpenWeatherMap API key (free tier available at https://openweathermap.org/api)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/marksegi/weather-dashboard.git
cd weather-dashboard
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and add your OpenWeatherMap API key:

```
OPENWEATHER_API_KEY=your_api_key_here
```

### 5. Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Usage

1. **Search for a City**: Enter any city name in the search box and click "Search" or press Enter
2. **View Current Weather**: See real-time weather data including temperature, conditions, and meteorological details
3. **Check Forecast**: Scroll down to view the 5-day weather forecast
4. **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices

## API Endpoints

### Current Weather
```
GET /api/weather/current?city=London
```

Returns current weather data for the specified city.

### Weather Forecast
```
GET /api/weather/forecast?city=London&days=5
```

Returns 5-day weather forecast for the specified city.

### Air Quality
```
GET /api/weather/air-quality?lat=51.5074&lon=-0.1278
```

Returns air quality data for specified coordinates.

## Configuration

### Customize API Parameters

Edit `app.py` to modify:

- **Temperature Units**: Change `units` parameter to 'imperial' for Fahrenheit
- **Forecast Days**: Modify the `days` parameter in forecast requests
- **API Timeout**: Adjust the `timeout` parameter in requests

```python
# Example: Use Fahrenheit
params = {
    'q': city,
    'appid': OPENWEATHER_API_KEY,
    'units': 'imperial'  # Celsius: 'metric', Fahrenheit: 'imperial'
}
```

## Project Structure

```
weather-dashboard/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
├── README.md             # This file
├── templates/
│   └── index.html        # Main HTML template
└── static/
    ├── style.css         # CSS styles
    └── script.js         # Frontend JavaScript
```

## Deployment

### Deploy to Heroku

1. Install Heroku CLI
2. Create a Procfile:

```
web: gunicorn app:app
```

3. Deploy:

```bash
heroku create your-app-name
heroku config:set OPENWEATHER_API_KEY=your_api_key
git push heroku main
```

### Deploy to AWS, Google Cloud, or Azure

Refer to the respective platform's documentation for deploying Flask applications.

## Troubleshooting

### "OPENWEATHER_API_KEY not found"
- Ensure `.env` file exists in the project root
- Verify the API key is correctly added
- Restart the application

### "City not found" Error
- Check the spelling of the city name
- Try using the city code or coordinates
- Ensure you have internet connectivity

### API Rate Limiting
- Free tier has limits on requests
- Wait a moment before making the next request
- Consider upgrading your OpenWeatherMap plan

### CORS Issues (when accessing from different domain)
- Install Flask-CORS: `pip install flask-cors`
- Add CORS support to `app.py`

## Cost Considerations

- **OpenWeatherMap Free Tier**: 1,000 API calls per day
- **Current Weather**: 1 API call per request
- **Forecast Data**: 1 API call per request
- **Total Daily Limit**: ~500 searches with free tier

Monitor usage at: https://openweathermap.org/api/calls

## Future Enhancements

- [ ] Add user location detection (geolocation)
- [ ] Save favorite cities
- [ ] Add weather alerts and notifications
- [ ] Implement air quality index (AQI) display
- [ ] Add UV index information
- [ ] Support for multiple language displays
- [ ] Weather comparison between cities
- [ ] Historical weather data
- [ ] Weather-based recommendations
- [ ] Dark/Light theme toggle

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please:
1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Contact the maintainers

## Acknowledgments

- Weather data provided by [OpenWeatherMap](https://openweathermap.org/)
- Icons and design inspiration from modern weather applications

## More Information

- [OpenWeatherMap API Documentation](https://openweathermap.org/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [OpenWeatherMap Free API Tier](https://openweathermap.org/price)
