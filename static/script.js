// Weather Icon Mapping
const WEATHER_ICONS = {
    '01d': '☀️', '01n': '🌙',
    '02d': '⛅', '02n': '☁️',
    '03d': '☁️', '03n': '☁️',
    '04d': '☁️', '04n': '☁️',
    '09d': '🌧️', '09n': '🌧️',
    '10d': '🌧️', '10n': '🌧️',
    '11d': '⛈️', '11n': '⛈️',
    '13d': '❄️', '13n': '❄️',
    '50d': '🌫️', '50n': '🌫️'
};

class WeatherDashboard {
    constructor() {
        this.cityInput = document.getElementById('cityInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.errorDiv = document.getElementById('error');
        this.loadingDiv = document.getElementById('loading');
        this.currentWeatherSection = document.getElementById('currentWeatherSection');
        this.forecastSection = document.getElementById('forecastSection');

        this.init();
    }

    init() {
        this.searchBtn.addEventListener('click', () => this.handleSearch());
        this.cityInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.handleSearch();
        });

        // Load default city on page load
        this.loadWeather('London');
    }

    handleSearch() {
        const city = this.cityInput.value.trim();
        if (!city) {
            this.showError('Please enter a city name');
            return;
        }
        this.loadWeather(city);
    }

    async loadWeather(city) {
        this.showLoading(true);
        this.hideError();

        try {
            const [currentData, forecastData] = await Promise.all([
                this.fetchCurrentWeather(city),
                this.fetchForecast(city)
            ]);

            if (currentData.error) {
                throw new Error(currentData.error);
            }

            this.displayCurrentWeather(currentData);
            if (!forecastData.error) {
                this.displayForecast(forecastData);
            }
        } catch (error) {
            this.showError(`Error: ${error.message}`);
        } finally {
            this.showLoading(false);
        }
    }

    async fetchCurrentWeather(city) {
        const response = await fetch(`/api/weather/current?city=${encodeURIComponent(city)}`);
        return await response.json();
    }

    async fetchForecast(city) {
        const response = await fetch(`/api/weather/forecast?city=${encodeURIComponent(city)}&days=5`);
        return await response.json();
    }

    displayCurrentWeather(data) {
        if (data.error) return;

        document.getElementById('cityName').textContent = `${data.city}, ${data.country}`;
        document.getElementById('weatherDate').textContent = new Date().toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
        document.getElementById('temperature').textContent = `${Math.round(data.temperature)}°C`;
        document.getElementById('weatherIcon').textContent = WEATHER_ICONS[data.icon] || '🌤️';
        document.getElementById('weatherDescription').textContent = data.description || 'N/A';
        document.getElementById('feelsLike').textContent = `${Math.round(data.feels_like)}°C`;
        document.getElementById('humidity').textContent = `${data.humidity}%`;
        document.getElementById('pressure').textContent = `${data.pressure} mb`;
        document.getElementById('windSpeed').textContent = `${data.wind_speed} m/s`;
        document.getElementById('visibility').textContent = `${(data.visibility / 1000).toFixed(1)} km`;
        document.getElementById('clouds').textContent = `${data.clouds}%`;
        document.getElementById('sunrise').textContent = data.sunrise;
        document.getElementById('sunset').textContent = data.sunset;

        this.currentWeatherSection.style.display = 'block';
    }

    displayForecast(data) {
        if (data.error) return;

        const forecastContainer = document.getElementById('forecastContainer');
        forecastContainer.innerHTML = '';

        // Group forecast by day (take one forecast per day, at noon)
        const dailyForecasts = {};
        data.forecast.forEach(item => {
            const date = item.dt.split(' ')[0];
            const hour = parseInt(item.dt.split(' ')[1].split(':')[0]);

            // Keep the forecast closest to 12:00
            if (!dailyForecasts[date] || Math.abs(hour - 12) < Math.abs(parseInt(dailyForecasts[date].dt.split(' ')[1].split(':')[0]) - 12)) {
                dailyForecasts[date] = item;
            }
        });

        Object.values(dailyForecasts).slice(0, 5).forEach(forecast => {
            const card = document.createElement('div');
            card.className = 'forecast-card';
            card.innerHTML = `
                <div class="forecast-card-date">${new Date(forecast.dt).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</div>
                <div class="forecast-card-icon">${WEATHER_ICONS[forecast.icon] || '🌤️'}</div>
                <div class="forecast-card-temp">${Math.round(forecast.temp)}°C</div>
                <div class="forecast-card-desc">${forecast.description}</div>
                <div class="forecast-card-details">
                    <div>💧 ${forecast.humidity}%</div>
                    <div>💨 ${forecast.wind_speed} m/s</div>
                </div>
            `;
            forecastContainer.appendChild(card);
        });

        this.forecastSection.style.display = 'block';
    }

    showLoading(show) {
        this.loadingDiv.style.display = show ? 'block' : 'none';
    }

    showError(message) {
        this.errorDiv.textContent = message;
        this.errorDiv.classList.add('show');
    }

    hideError() {
        this.errorDiv.classList.remove('show');
        this.errorDiv.textContent = '';
    }
}

// Initialize dashboard when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    new WeatherDashboard();
});
