from micInput import *
from openai import OpenAI
from dotenv import load_dotenv
import json
import eel
from datetime import date as dt, datetime
import time

from weather import getForecast
from reminder import add_task, complete_task
from calendar_events import create_event
from ui import expandCalendar, close
from maps import get_directions
from facialrecognition import facial_code


load_dotenv()
client = OpenAI()

tools = [
    {
        "type": "function",
        "function":{
            "name": "getForecast",
            "description": "Gets the current weather condition and a three-day forecast based on a location. Tell the user that they can see a 7-day forecast displayed on the screen, if the user is asking for a forecast.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The location in which to get weather conditions on. If not provided, do not try to parse a location from the command, the default location stored in the program will be used."
                    },
                    "date": {
                        "type": "string",
                        "description": "The date on which the user wants the forecast on. Must give the date in the format YYYY-MM-DD. If a date is not provided, do not try to parse a date from the command, a default parameter stored in the program will be used. The current date is " + str(dt.today().strftime("%Y-%m-%d"))
                    }
                },
                "required": [
                    
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "add_task",
            "description": "Adds a task or reminder to the user's reminders. Used when the user wants to reminded of something. Confirm the user's request at the end.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task or reminder to be added to the user's list of reminders."
                    }
                },
                "required": [
                    "task"
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "complete_task",
            "description": "Removes a completed task from the list of reminders. Call this whenever a user says they have completed a task. Confirm the user's request at the end.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The task or reminder that was completed from the user's list of reminders."
                    }
                },
                "required": [
                    "task"
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "create_event",
            "description": "Creates a calendar event for the user. Use this instead of the function 'add_task' when the user specifies a time and/or location, or when the user mentions an event instead of a task. The output should have the same amount of start times and end times with no duplicates.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title or short description of the event."
                    },
                    "dates": {
                        "type": "string",
                        "description": "The dates that the event occurs on. If multiple dates are given, return a list of dates separated by commas. If no dates are given, then return the current date. Parse the date in the format YYYY-MM-DD. The current date in YYYY-MM-DD format is " + str(dt.today().strftime("%Y-%m-%d"))
                    },
                    "start_times": {
                        "type": "string",
                        "description": "The start times that the event occurs on. If multiple start times are given, return a list of end times separated by commas. If no start times are given, then return the current time. Parse the time in the format hour:minute. The current time in hour:minute format is " + str(datetime.now().time().strftime("%H:%M"))
                    },
                    "end_times": {
                        "type": "string",
                        "description": "The end times that the event occurs on. If multiple end times are given, return a list of end times separated by commas. If no end times are given, then return the time an hour after the given start time. Parse the time in the format hour:minute. The current time in hour:minute format is " + str(datetime.now().time().strftime("%H:%M"))
                    },
                    "location": {
                        "type": "string",
                        "description": "The location at which the event takes place."
                    }
                },
                "required": [
                    "title"
                ]
            }
        }
    },
    {
        "type": "function",
        "function":{
            "name": "expandCalendar",
            "description": "Changes the display to show the user their entire schedule for the week."
        }
    },
    {
        "type": "function",
        "function":{
            "name": "close",
            "description": "It goes back to the main page. It closes expanded windows that the user no longer needs to see. Use this if the user says they are done looking something."
        }
    },
    {
        "type": "function",
        "function":{
            "name": "get_directions",
            "description": "Gives the user directions on how to get to their destination. Usually from home to work.",
            "parameters": {
                "type": "object",
                "properties": {
                    "origin": {
                        "type": "string",
                        "description": "The user's place of origin, in terms of location. If one is not given then return an empty string. The default home address that is saved in the program will be used."
                    },
                    "destination": {
                        "type": "string",
                        "description": "The user's desired destination. If one is not given then return an empty string. The default work address that is saved in the program will be used."
                    },
                    "mode": {
                        "type": "string",
                        "description": "The user's mode of transportation. If one is not given then return an empty string. Else return either driving, transit, walking, or bicycling."
                    }
                },
                "required": [
                ]
            }
        }
    },
]
def askJarvis(command):

    available_functions = {
        "getForecast": getForecast,
        "add_task": add_task,
        "complete_task": complete_task,
        "create_event": create_event,
        "expandCalendar": expandCalendar,
        "close": close,
        "get_directions": get_directions,
    }
    messages = [{"role": "user", "content": command}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    #print(response)
    #print("****************")
    response_message = response.choices[0].message
    #print(response_message)
    tool_calls = response_message.tool_calls

    if(tool_calls):
        messages.append(response_message)

        for f in tool_calls:
            function_to_call = available_functions[f.function.name]
            function_parameters = json.loads(f.function.arguments)
            function_response = None

            #weather functions
            if(function_to_call == getForecast):
                #print("Location : " + str(function_parameters.get("location")))
                #print("Date : " + str(function_parameters.get("date")))
                #print(tools[0]['function']['parameters']['properties']['date']['description'])
                function_response = function_to_call(location=function_parameters.get("location"), date=function_parameters.get("date"))
                eel.updateWeatherData()
            
            #reminder functions
            elif(function_to_call == add_task):
                function_response = function_to_call(task = function_parameters.get("task"))
                return "Task added." #saving tokens, can be removed
            elif(function_to_call == complete_task):
                from reminder import incomplete_tasks
                tasks = ", ".join(str(elem) for elem in incomplete_tasks)
                messages_t = [{
                    "role": "assistant",
                    "content": "Return the task, from the list of tasks, that is closest to the prompt. You should return the exact string of the task chosen. List of tasks: " + tasks + ". Prompt: " + function_parameters.get("task")
                }]

                task = client.chat.completions.create(
                    model="gpt-3.5-turbo-0613",
                    messages=messages_t
                ).choices[0].message.content
                function_response = function_to_call(task = task)

                return "Task removed from to-do list." #saving tokens, can be removed
            
            #calendar functions
            elif(function_to_call == create_event):
                function_response = function_to_call(title = function_parameters.get("title"), dates = function_parameters.get("dates"), start_times = function_parameters.get("start_times"), end_times = function_parameters.get("end_times"), location = function_parameters.get("location"))
                
                return "Event has been added to calendar." #saving tokens, can be removed
            elif(function_to_call == expandCalendar):
                function_to_call()
                return("Switched") #saving tokens, can be removed
            
            #GUI functions
            elif(function_to_call == close):
                function_to_call()
                return("Switched") #saving tokens, can be removed
            
            #map functions
            elif(function_to_call == get_directions):
                function_response = function_to_call(origin = function_parameters.get("origin"), destination = function_parameters.get("destination"), mode = function_parameters.get("mode"))
                return "map gpt" #REMOVE
            

            #GPT's response to the request, not the function's return
            messages.append(
                {
                    "tool_call_id": f.id,
                    "role": "tool",
                    "name": f.function.name,
                    "content": function_response
                }
            )

            response_to_user = client.chat.completions.create(
                model="gpt-3.5-turbo-0613",
                messages=messages
            )
        return response_to_user.choices[0].message.content
    else:
        return response_message.content

def initiateJarvis():
    eel.init('web') #giving terminal program access to the same eel instance
    while True:
        print("Listening for keyword")
        if(listen()):
            getVoiceCommand()
            command = transcribeCommand()["text"]
            print("Transcripted command: " + command)

            if("bye" in command.lower()):
                print("Goodbye sire")
                facial_code()
            else:
                print("GPT response to user: " + askJarvis(command))