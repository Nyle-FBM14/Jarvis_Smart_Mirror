import eel
import time
import datetime
import os

#time slots: if a time is listed, it is assumed that the event runs for an hour
#ints will be used to represent the hours of the day
#meaning if 7pm(19) is listed, the event runs from 7pm(19) to 8pm(20). 8pm(20) does not need to be put in the list
events = [
    {
        "title": "Easter Sunday",
        "dates": ["Sunday"],
        "time_slots": [0, 23],
        "location": "Everywhere"
    },
    {
        "title": "Doctah Apoyment",
        "dates": ["Wednesday"],
        "time_slots": [15, 16],
        "location": "Everywhere"
    },
    {
        "title": "Meeting",
        "dates": ["Monday", "Tuesday", "Thursday"],
        "time_slots": [14, 15, 16, 22],
        "location": "Everywhere"
    },
]
@eel.expose
def getDayEvents():
    '''
    end_of_day = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
    events = nylas.events.list(
        grant_id,
        query_params={
        "calendar_id": os.environ.get("CALENDAR_ID"),
        "start": int(end_of_day.timestamp())
        }
    )['data'] #list of events that started today and ongoing events that started before the end of day
    #assuming nylas only returns events that have not ended yet. if not, filter live events that are still going on this day'''

    return events

@eel.expose
def getWeekEvents():
    '''
    current_date = datetime.date.today()
    end_of_week = current_date + datetime.timedelta(days=(6 - current_date.weekday()))
    end_of_week = datetime.datetime.combine(end_of_week, datetime.time.max)

    events = nylas.events.list(
        grant_id,
        query_params={
        "calendar_id": os.environ.get("CALENDAR_ID"),
        "start": int(end_of_week.timestamp())
        }
    )['data'] #list of events that started today and ongoing events that started before the end of the week
    #assuming nylas only returns events that have not ended yet. if not, filter live events that are still going on this week'''

    return events

def create_event(title, start, end, location):
    if(isinstance(start, int)):
        ts = datetime.datetime.fromtimestamp(start)
        ts = ts.strftime('%Y-%m-%d %H:%M:%S')
        print(ts)
    if(isinstance(end, int)):
        te = datetime.datetime.fromtimestamp(end)
        te = te.strftime('%Y-%m-%d %H:%M:%S')
        print(te)
    print(title)
    print(location)
    print(start)
    print(end)

    events.append(
        {
            "title": "test add",
            "dates": ["Sunday"],
            "time_slots": [14, 16,],
            "location": "peepee"
        }
    )

    return "Event has been added to calendar."
    '''
    events = nylas.events.create(
        grant_id,
        request_body={
            "title": title,
            "when": {
            "start_time": start,
            "end_time": end,
            "location": location
            },
        },
        query_params={
            "calendar_id": os.environ.get("CALENDAR_ID")
        }
    )'''
