document.getElementById('fetchBtn').addEventListener('click', async () => {
    const location = document.getElementById('locationInput').value.trim();
    if (!location) return alert('Please enter a location.');
  
    const res = await fetch(`/api/weather/${location}`);
    const data = await res.json();
  
    if (!data.success) {
      alert('Failed to fetch weather data.');
      return;
    }
  
    document.getElementById('weatherOutput').style.display = 'block';
    document.getElementById('locationName').textContent = data.location;
    document.getElementById('temp').textContent = data.current_weather.temperature;
    document.getElementById('humidity').textContent = data.current_weather.humidity;
    document.getElementById('desc').textContent = data.current_weather.description;
  
    // Forecast
    const forecastList = document.getElementById('forecast');
    forecastList.innerHTML = '';
    data.forecast.slice(0, 6).forEach(f => {
      const li = document.createElement('li');
      li.className = 'list-group-item';
      li.textContent = `${f.date}: ${f.temperature}°C, ${f.description}`;
      forecastList.appendChild(li);
    });
  
    // Disease Risks
    const riskContainer = document.getElementById('riskContainer');
    riskContainer.innerHTML = '';
    data.disease_risks.forEach(risk => {
      const div = document.createElement('div');
      div.className = `alert alert-${risk.risk_level === 'HIGH' ? 'danger' :
        risk.risk_level === 'MEDIUM' ? 'warning' : 'success'}`;
      div.innerHTML = `<strong>${risk.type}</strong> (${risk.risk_level})<br>${risk.reason}<br><em>${risk.preventive_action}</em>`;
      riskContainer.appendChild(div);
    });
  });
  