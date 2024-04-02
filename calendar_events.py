import eel
import time
from datetime import date, datetime, timedelta
import os
import json
from facialrecognition import username
#time slots: if a time is listed, it is assumed that the event runs for an hour
#ints will be used to represent the hours of the day
#meaning if 7pm(19) is listed, the event runs from 7pm(19) to 8pm(20). 8pm(20) does not need to be put in the list
events = []

def getHour(time_string):
    return int(datetime.strptime(time_string, "%H:%M").hour)
def getWeekday(date_string):
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day = datetime.strptime(date_string, "%Y-%m-%d").date()
    return weekdays[day.weekday()]
def getLastWeekday():
    current_day = date.today()
    days_until_saturday = (5 - current_day.weekday()) % 7
    return current_day + timedelta(days=days_until_saturday)
def isWithinWeek(date, saturday):
    d = datetime.strptime(date, "%Y-%m-%d")
    return d.date() <= saturday
def eventIsLive(date, saturday):
    d = datetime.strptime(date, "%Y-%m-%d")
    sunday = saturday - timedelta(days=6)
    return d < (sunday)
def loadEvents():
    global events
    if(not len(events)):
        filename = f"UserData/calendar/{username}_events.json"
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                events = json.load(file)

    #print(events)
def saveEvents():
    global events
    new_events = []
    for event in events:
        if eventIsLive(event['dates'][-1], getLastWeekday()):
            new_events.append(event)
    
    events = new_events
    filename = f"UserData/calendar/{username}_events.json"
    with open(filename, 'w') as file:
        json.dump(new_events, file, indent=4)

@eel.expose
def getDayEvents():
    global events
    loadEvents()

    daily_events = []
    for event in events:
        if date.today().strftime("%Y-%m-%d") in event['dates']:
            for i in range(len(event['start_times'])):
                daily_event = {
                    "title": event['title'],
                    "start": event['start_times'][i],
                    "end": event['end_times'][i],
                    "location": event['location']
                }
                daily_events.append(daily_event)
    return daily_events

@eel.expose
def getWeekEvents():
    global events
    loadEvents()
    times = ["12AM", "1AM", "2AM", "3AM", "4AM", "5AM", "6AM", "7AM", "8AM", "9AM", "10AM", "11AM", "12PM", "1PM", "2PM", "3PM", "4PM", "5PM", "6PM", "7PM", "8PM", "9PM", "10PM", "11PM"]
    weekly_events = []
    for event in events:
        for date in event['dates']:
            if isWithinWeek(date, getLastWeekday()):
                for i in range(len(event['start_times'])):
                    weekly_event = {
                        "title": event['title'],
                        "start": event['start_times'][i],
                        "end": event['end_times'][i],
                        "location": event['location'],
                        "weekday": getWeekday(date),
                        "time": times[getHour(event['start_times'][i])]
                    }
                    weekly_events.append(weekly_event)

    return weekly_events

def create_event(title, dates, start_times, end_times,  location):
    print(title)
    print(location)
    print(dates)
    print(start_times)
    print(end_times)
    if(dates == None):
        dates = str(date.today().strftime("%Y-%m-%d"))
    if(start_times == None):
        start_times = str(datetime.now().time().strftime("%H:%M"))
    if(end_times == None):
        end_times = str((datetime.now() + timedelta(hours=1)).time().strftime("%H:%M"))
    date_list = dates.split(",")
    start_list = start_times.split(",")
    end_list = end_times.split(",")
    events.append(
        {
            "title": title,
            "dates": date_list,
            "start_times": start_list,
            "end_times": end_list,
            "location": location
        }
    )
    saveEvents()
    if(datetime.strptime(date_list[0], "%Y-%m-%d").date() == date.today()): #if the event added starts today - CHANGE
        eel.updateDailyEventsData()
    return "Event has been added to calendar."
