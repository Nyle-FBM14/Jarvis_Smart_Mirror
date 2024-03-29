import eel
#from ui import switch_to_main_ui

#global variables
global username, main_location
username = "Guest"
main_location = "Toronto"

@eel.expose
def getUsername():
    return username
@eel.expose
def getMainLocation():
    return main_location
#when user is logged in, use this to switch to main page
#switch_to_main_ui()