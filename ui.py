import eel

def switch_to_main_ui():
    eel.goToMain()

def expandCalendar():
    eel.openWeekView()

def close():
    eel.reloadMainPage() #just closes week view