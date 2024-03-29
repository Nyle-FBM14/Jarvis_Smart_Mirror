import eel
import threading

eel.init('web')

#import all functions that should be exposed to eel
from weather import getForecast, getCurrentWeatherData, getHourlyWeatherData, getForecastData
from reminder import getReminders, load_reminders
from facialrecognition import getMainLocation, getUsername

from jarvis import initiateJarvis
t = threading.Thread(target=initiateJarvis)
t.start()

eel.start("index.html")




#start facial recognition

#once logged in, prepare main page

#go to main page
