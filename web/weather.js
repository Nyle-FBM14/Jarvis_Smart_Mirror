var currentWeatherData, hourlyWeatherData, forecastData;
let hourly_forecast = document.getElementById("hourly_forecast");
let weekly_forecast = document.getElementById("weekly_forecast");

function updateWeatherSection(){
    document.getElementById("current_temp").innerHTML = currentWeatherData['temp'];
    document.getElementById("current_feelsLike").innerHTML = currentWeatherData['feels_like'];
    document.getElementById("current_high").innerHTML = currentWeatherData['high'];
    document.getElementById("current_low").innerHTML = currentWeatherData['low'];
    document.getElementById("current_humidity").innerHTML = currentWeatherData['humidity'];
    document.getElementById("current_precipitation").innerHTML = currentWeatherData['precipitation'];
    document.getElementById("current_location").innerHTML = currentWeatherData['location'];
    document.getElementById("current_region").innerHTML = currentWeatherData['region'];
    document.getElementById("current_icon").src = "https:" + currentWeatherData['icon'];
    document.getElementById("current_icon").alt = currentWeatherData['condition'];

    for (let i = 0; i < 7; i++) {
        hourly_forecast.innerHTML = "";
        weekly_forecast.innerHTML = "";
        //hourly
        fetch(`./hourly_weather.html`)
        .then(res => {
            if(res.ok) {
                return res.text();
            }
        }).then(html => {
            html = html.replace(/\[hourly_time_var\]/g, hourlyWeatherData[i]['time']);
            html = html.replace(/\[hourly_icon_var\]/g, hourlyWeatherData[i]['icon']);
            html = html.replace(/\[hourly_alt_var\]/g, hourlyWeatherData[i]['condition']);
            html = html.replace(/\[hourly_temp_var\]/g, hourlyWeatherData[i]['temp']);
            html = html.replace(/\[hourly_p_var\]/g, hourlyWeatherData[i]['precipitation']);
            
            let temp = document.createElement('div');
            temp.innerHTML = html;
            hourly_forecast.appendChild(temp);
        });
        //daily
        fetch(`./weekly_weather.html`)
        .then(res => {
            if(res.ok) {
                return res.text();
            }
        }).then(html => {
            html = html.replace(/\[day_month_var\]/g, forecastData[i]['month']);
            html = html.replace(/\[day_day_var\]/g, forecastData[i]['day']);
            html = html.replace(/\[day_icon_var\]/g, forecastData[i]['icon']);
            html = html.replace(/\[day_condition_var\]/g, forecastData[i]['condition']);
            html = html.replace(/\[day_high_var\]/g, forecastData[i]['high']);
            html = html.replace(/\[day_low_var\]/g, forecastData[i]['low']);

            let temp = document.createElement('div');
            temp.innerHTML = html;
            weekly_forecast.appendChild(temp);
        });
    }
}

eel.expose(updateWeatherData);
function updateWeatherData(){ //use to just expose updateWeatherSection but it does not reload the weather data first so I made this function instead to be called
    Promise.all([
        eel.getCurrentWeatherData()(),
        eel.getHourlyWeatherData()(),
        eel.getForecastData()()
    ]).then(function(responses) {
        // Assign responses to variables
        currentWeatherData = responses[0];
        hourlyWeatherData = responses[1];
        forecastData = responses[2];
    
        // Update weather section
        updateWeatherSection();
    }).catch(function(error) {
        console.error("Error fetching data:", error);
    });
}

//INITIALIZE MAIN PAGE
eel.getForecast()().then(function() {
    // After getForecast() finishes, fetch other data
    return Promise.all([
        eel.getCurrentWeatherData()(),
        eel.getHourlyWeatherData()(),
        eel.getForecastData()()
    ]);
}).then(function(responses) {
    // Assign responses to variables
    currentWeatherData = responses[0];
    hourlyWeatherData = responses[1];
    forecastData = responses[2];

    updateWeatherSection();
}).catch(function(error) {
    console.error("Error fetching data:", error);
});