import requests
from tkinter import *
from PIL import ImageTk, Image
import urllib.request
import json
from datetime import datetime, timedelta
from datetime import date as dt
import eel

from dotenv import load_dotenv
from os import getenv
load_dotenv()

API_KEY = getenv("WEATHER_API_KEY")
from facialrecognition import main_location

current_weather_data = {
    "location": "Toronto",
    "region": "ON",
    "condition": "sunny",
    "icon": "https://cdn.weatherapi.com/weather/64x64/day/113.png",
    "temp": 0,
    "feels_like": 0,
    "humidity": 0,
    "precipitation": 0
}
hourly_weather_data = [None, None, None, None, None, None, None]
forecast_data = [None, None, None, None, None, None, None]

def parseCurrentWeatherData(data):
    global current_weather_data
    current_weather_data = {
        "location": data['location']['name'],
        "region": data['location']['region'],
        "condition": data['current']['condition']['text'],
        "icon": data['current']['condition']['icon'],
        "temp": data['current']['temp_c'],
        "feels_like": data['current']['feelslike_c'],
        "high": data['forecast']['forecastday'][0]['day']['maxtemp_c'],
        "low": data['forecast']['forecastday'][0]['day']['mintemp_c'],
        "humidity": data['current']['humidity'],
        "precipitation": data['current']['precip_mm']
    }
def parseHourlyWeatherData(data): #will throw an error if the user asks for the weather on a day 14 days past the current and past 5pm. Weather api would need to access forecast data on the next day past 11pm, which is out of range
    global hourly_weather_data
    currentHour = datetime.now().hour
    currentHour = currentHour if (currentHour < 5) else 4 #if the current hour exceeds 5pm, it will be set back to 4pm even if the next day is within range of the weather api. Might fix this problem with more time.
    hourly_weather_data = [
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour]['precip_mm']
        },
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour+1]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour+1]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour+1]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour+1]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour]['precip_mm']
        },
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour+2]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour+2]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour+2]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour+2]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour]['precip_mm']
        },
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour+3]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour+3]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour+3]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour+3]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour]['precip_mm']
        },
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour+4]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour+4]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour+4]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour+4]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour]['precip_mm']
        },
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour+5]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour+5]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour+5]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour+5]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour]['precip_mm']
        },
        {
            "time": data['forecast']['forecastday'][0]['hour'][currentHour+7]['time'].split()[1],
            "condition": data['forecast']['forecastday'][0]['hour'][currentHour+7]['condition']['text'],
            "icon": data['forecast']['forecastday'][0]['hour'][currentHour+7]['condition']['icon'],
            "temp": data['forecast']['forecastday'][0]['hour'][currentHour+7]['temp_c'],
            "precipitation": data['forecast']['forecastday'][0]['hour'][currentHour+7]['precip_mm']
        }
    ]
def parseForecastData(data):
    month = ["not a month", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day_data = {
        "month": month[datetime.strptime(data['forecast']['forecastday'][0]['date'], "%Y-%m-%d").date().month],
        "day": datetime.strptime(data['forecast']['forecastday'][0]['date'], "%Y-%m-%d").date().day,
        "condition": data['forecast']['forecastday'][0]['day']['condition']['text'],
        "icon": data['forecast']['forecastday'][0]['day']['condition']['icon'],
        "high": data['forecast']['forecastday'][0]['day']['maxtemp_c'],
        "low": data['forecast']['forecastday'][0]['day']['mintemp_c']
    }
    return day_data

def getCurrentWeather(location = main_location) -> str:
    request = "http://api.weatherapi.com/v1/current.json?key=%s&q=%s" % (API_KEY, location)
    data = requests.get(request)
    return json.dumps(data.json())

#setting hour = -1 or any number outside of [0..24] gets rid of hourly weather
def getForecastDays(location = main_location, days = 3, date = dt.today(), hour = -1, lang = "") -> str:
    request = "http://api.weatherapi.com/v1/forecast.json?key=%s&q=%s&days=%d&dt=%s&hour=%d&lang=%s" % (API_KEY, location, days, date, hour, lang)
    data = requests.get(request).json()
    return data

@eel.expose
def getForecast(location = main_location, days = 1, date = "", hour = -1, lang = "") -> str:
    '''
    I had to shorten the json data passed to open AI because it was over the token limit.
    So first I call the weather API with one specified hour and just one day.
    Including the weather for each hour of a day, with multiple days is way too much data to send back.
    I allowed one date and on specified hour in case the user asks for a specific time during the day.
    Otherwise the hours section is removed completly.
    I call the same weather API request while including all hours to display the hourly weather conditions.
    I allow chatgpt to either return a date or leave. It returns a date if the user gives one, therefore the mirror can show the forecast starting on that given date.
    Else it just gives the forecast starting on the current date.
    Problem explained in comment on line 157. I don't wanna fix it :p
    The GPT model seems to think the current year is still 2022. I fixed this problem by giving it the current date in the weather function date parameter description. This also gives it the current date even if the user doesn't ask for the weather and just the date.
    -Nyle
    '''
    if(location == None): #gpt model sends a None object when it doesn't parse a location and the api sends back the weather for Nonnette, France
        location = main_location
        
    if(isinstance(date, str) and (not date == "")):#turns the date string into a datetime.date object
        date = datetime.strptime(date, "%Y-%m-%d").date()
        if(date < dt.today()): #gpt repeatedly gives the date 2022-12-28 if asked for the date 2 days from now
            date = dt.today()
    else:#sets date to current date if a date is not given
        date = dt.today()

    request = "http://api.weatherapi.com/v1/forecast.json?key=%s&q=%s&days=%d&dt=%s&hour=%d&lang=%s" % (API_KEY, location, days, date, hour, lang)
    initial_data = requests.get(request).json()

    parseCurrentWeatherData(initial_data)

    if(hour == -1):
        request = "http://api.weatherapi.com/v1/forecast.json?key=%s&q=%s&days=%d&dt=%s&hour=&lang=" % (API_KEY, location, days, date)
        parseHourlyWeatherData(requests.get(request).json())
    else:
        parseHourlyWeatherData(initial_data)

    if(date == "" or date == None):#sets date to current date if a date is not given
        date = dt.today()
    if(isinstance(date, str)):#turns the date string into a datetime.date object
        date = datetime.strptime(date, "%Y-%m-%d").date()

    if(date > (dt.today() + timedelta(days=13))): #weather api can only show forecast between current date and the next 14 days
        return "Say 'Sorry that forecast date is out of my range.'"
    
    num_days = 7
    if((date + timedelta(days=6)) > (dt.today() + timedelta(days=13))): #only affects the days that are within the range of the weather api
        num_days = (dt.today() + timedelta(days=13)).day - date.day

    for i in range(num_days):#since a full 7-day forecast given the starting date may be out of range of the api, the unaffected days are gonna show old data
        data = getForecastDays(location, 1, date.strftime('%Y-%m-%d'), -1, "") #api only provides a 1-day forecast when a date is provided
        forecast_data[i] = parseForecastData(data)
        date = date + timedelta(days=1)

    return json.dumps(initial_data)

@eel.expose
def getCurrentWeatherData():
    return current_weather_data
@eel.expose
def getHourlyWeatherData():
    return hourly_weather_data
@eel.expose
def getForecastData():
    return forecast_data