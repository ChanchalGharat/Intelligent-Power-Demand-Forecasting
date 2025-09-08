const baseURL = "http://127.0.0.1:8000";

// --------------------
// Fetch Data Functions
// --------------------
async function fetchForecast(periods = 144) {
    const res = await fetch(`${baseURL}/forecast?periods=${periods}`);
    return await res.json();
}

async function fetchWeather() {
    const res = await fetch(`${baseURL}/weather`);
    return await res.json();
}

async function fetchHolidays() {
    const res = await fetch(`${baseURL}/holidays`);
    return await res.json();
}

// --------------------
// Render Forecast Chart
// --------------------
async function renderForecastChart() {
    const data = await fetchForecast(144); // 144 steps = 24 hours at 10-min intervals
    const labels = data.map(item => item.ds);
    const yhat = data.map(item => item.yhat);

    const ctx = document.getElementById('forecastChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Electricity Demand (MW)',
                data: yhat,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.3
            }]
        },
        options: { responsive: true }
    });
}

// --------------------
// Render Weather Chart
// --------------------
async function renderWeatherChart() {
    
    const data = await fetchWeather();
    const labels = data.map(item => item.time);

    // Check if backend returned dummy or real data
    const temperature = data.map(item => item.temperature ?? 0);
    const humidity = data.map(item => item.humidity ?? 0);
    const cloudCover = data.map(item => item.cloudCover ?? 0);

    const ctx = document.getElementById('weatherChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [
                { label: 'Temperature (°C)', data: temperature, borderColor: 'red', tension: 0.3 },
                { label: 'Humidity (%)', data: humidity, borderColor: 'blue', tension: 0.3 },
                { label: 'Cloud Cover (%)', data: cloudCover, borderColor: 'gray', tension: 0.3 }
            ]
        },
        options: { responsive: true }
    });
    
}

// --------------------
// Display Holidays
// --------------------
async function displayHolidays() {
    const holidays = await fetchHolidays();
    const list = document.getElementById("holidayList");
    list.innerHTML = ""; // clear previous list

    holidays.forEach(h => {
        const li = document.createElement("li");
        li.textContent = `${h.date} → ${h.holiday_name} (Weekend: ${h.is_weekend})`;
        list.appendChild(li);
    });
}

// --------------------
// Initialize all charts & lists
// --------------------
async function initDashboard() {
    await renderForecastChart();
    await renderWeatherChart();
    await displayHolidays();
}

// Call initialization
initDashboard();
