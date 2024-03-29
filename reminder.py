import json
import os
import eel

from facialrecognition import username
global incomplete_tasks, complete_tasks
incomplete_tasks = []
complete_tasks = []

@eel.expose
def getReminders():
    return incomplete_tasks
@eel.expose
def load_reminders():
    global incomplete_tasks, complete_tasks
    reminders_filename = f"reminders/{username}/{username}_reminders.json"
    if not os.path.exists(reminders_filename):
        incomplete_tasks, complete_tasks = [], []  # Returns empty lists if the file does not exist
    else:
        with open(reminders_filename, 'r') as file:
            data = json.load(file)
        incomplete_tasks, complete_tasks = data.get('incomplete', []), data.get('complete', [])

def save_reminders(incomplete_reminders, complete_reminders):
    directory_path = f"reminders/{username}"  # Define the directory path
    reminders_filename = f"{directory_path}/{username}_reminders.json"
    data = {'incomplete': incomplete_reminders, 'complete': complete_reminders}
    
    # Check if the directory exists, if not, create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
    
    with open(reminders_filename, 'w') as file:
        json.dump(data, file, indent=4)

def add_task(task):
    print(task)
    if task:
        incomplete_tasks.append(task)
        save_reminders(incomplete_tasks, complete_tasks)  # Save reminders after adding a task
        eel.updateReminderData()
    else:
        print("Warning", "The task cannot be empty.")

    return ("Task to be added to reminders: " + task)

def complete_task(task):
    print(task)
    if task in incomplete_tasks:
        incomplete_tasks.remove(task)
        complete_tasks.append(task)
        save_reminders(incomplete_tasks, complete_tasks)  # Save reminders after completing a task
        eel.updateReminderData()

        return ("Task completed and removed from reminders: " + task)
    else:
        return "Task does not exit."

def test():
    global incomplete_tasks, complete_tasks
    print(type(incomplete_tasks))
    load_reminders()
    print(type(incomplete_tasks))
    add_task("eat shit")
    print(type(incomplete_tasks))
    print(incomplete_tasks)
#test()