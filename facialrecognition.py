import eel
from ui import switch_to_main_ui

#set this when user is logged in
global username
username = "No"

@eel.expose
def getUsername():
    return username

#when user is logged in, use this to switch to main page
#switch_to_main_ui()