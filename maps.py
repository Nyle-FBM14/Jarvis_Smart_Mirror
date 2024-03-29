import base64
import eel
import requests
from io import BytesIO
from html.parser import HTMLParser

home_address = "835+Roselawn+Avenue+Toronto+ON"
work_address = "350+Victoria+Street+Toronto+ON"

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = ""

    def handle_data(self, data):
        self.output += data

def build_static_map_url(location1, location2, api_key):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    encoded_location1 = "+".join(location1.split())
    encoded_location2 = "+".join(location2.split())
    parameters = {
        "center": f"{encoded_location1}|{encoded_location2}",
        "size": "500x500",
        "zoom": 10,
        "markers": f"{encoded_location1}|{encoded_location2}",
        "path": f"color:red|{encoded_location1}|{encoded_location2}",
        "key": api_key
    }
    url = base_url + "&".join([f"{key}={value}" for key, value in parameters.items()])
    return url

def display_static_map(location1, location2, api_key):
    static_map_url = build_static_map_url(location1, location2, api_key)
    response = requests.get(static_map_url)

    '''
    # Read the PNG file as binary data
    with open(response.content, 'rb') as file:
        image_data = file.read()
    
    # Convert binary data to Base64-encoded string
    base64_data = base64.b64encode(image_data).decode('utf-8')
    
    return base64_data'''

    return response.content

def format_directions(raw_directions):
    parser = HTMLStripper()
    formatted_directions = []
    for step in raw_directions:
        parser.feed(step["html_instructions"])
        formatted_directions.append(parser.output)
        parser.output = ""
    return formatted_directions

def parse_directions(directions):
    directions_text = ""
    if directions:
        steps = directions["routes"][0]["legs"][0]["steps"]
        formatted_steps = format_directions(steps) #not sure if this returns html elements or strings, but I'm gonna assume strings
        for step in formatted_steps:
            directions_text += step + "\n"
    else:
        directions_text = "Failed to fetch directions."
    
    return directions_text

def get_directions(origin = home_address, destination = work_address, mode = "transit", **kwargs):
    if(origin == "" or origin == None or origin == "home"):
        origin = home_address
    if(destination == "" or destination == None or destination == "home"):
        destination = work_address
    if(mode == "" or mode == None or mode == "home"):
        mode = "transit"
    
    print(origin)
    print(destination)
    print(mode)
    '''
    map_image = display_static_map(origin, destination, api_key) #i'm gonna insert this as the src in an <img> tag
    api_key = "INSERT_API_KEY"
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
        "mode": mode,
        **kwargs
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        directions = parse_directions(response.json())
        map_data = {
            "origin": origin,
            "destination": destination,
            "map": map_image,
            "directions": directions
        }
    else:
        map_data = {
            "origin": origin,
            "destination": destination,
            "map": "./images/cet.png",
            "directions": "Error fetching directions"
        }
        print("Error:", response.status_code)
        return "Failed to fetch directions."'''
    map_data = {
        "origin": origin,
        "destination": destination,
        "map": "./images/cet.png",
        "directions": "Error fetching directions"
    }
    eel.showMap(map_data)
    return "map test"
    #return directions #gpt will respond to user with directions