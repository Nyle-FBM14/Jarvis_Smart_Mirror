import base64
import os
import eel
import requests
from io import BytesIO
from html.parser import HTMLParser
import math

from dotenv import load_dotenv
from os import getenv
load_dotenv()
API_KEY = getenv("MAPS_API_KEY")
from facialrecognition import username

home_address = "835+Roselawn+Avenue+Toronto+ON"
work_address = "350+Victoria+Street+Toronto+ON"



def geocode_address(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['status'] == 'OK' and len(data['results']) > 0:
            location = data['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    return None, None

def get_addresses(username):
    address_file = f"Userdata/address/{username}.txt"
    home_address = "835+Roselawn+Avenue+Toronto+ON"
    work_address = "350+Victoria+Street+Toronto+ON"
    if os.path.exists(address_file):
        with open(address_file, "r") as file:
            lines = file.readlines()
            for line in lines:
                key, value = line.strip().split(":")
                if key.strip().lower() == "home":
                    home_address = value.strip()
                    home_address = home_address.replace("+", " ").replace('"', '')
                elif key.strip().lower() == "work":
                    work_address = value.strip()
                    work_address = work_address.replace("+", " ").replace('"', '')
    return home_address, work_address

class HTMLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.output = ""

    def handle_data(self, data):
        self.output += data

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    radius = 6371  # Radius of the Earth in kilometers
    distance = radius * c
    return distance

def calculate_zoom_level(distance):
    zoom_distances = {
        1: 10000,   # World
        3: 5000,   # Landmass/continent
        5: 1000,   # Landmass/continent
        7: 250,   # City
        10: 50,   # City
        12: 15,     # Streets
        13: 5,     # Streets
        15: 1,     # Streets
    }
    for zoom, zoom_distance in sorted(zoom_distances.items(), reverse=True):
        if distance < zoom_distance:
            print (distance)
            return zoom

    return max(zoom_distances.keys())
def build_static_map_url(location1, location2, api_key):
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    # Geocode origin and destination addresses to obtain coordinates
    origin_lat, origin_lon = geocode_address(location1, api_key)
    destination_lat, destination_lon = geocode_address(location2, api_key)
    
    if origin_lat is None or origin_lon is None or destination_lat is None or destination_lon is None:
        return None
    
    # Calculate distance between origin and destination
    earth_radius_km = 6371.0
    lat1_rad = math.radians(origin_lat)
    lon1_rad = math.radians(origin_lon)
    lat2_rad = math.radians(destination_lat)
    lon2_rad = math.radians(destination_lon)
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance_km = earth_radius_km * c
    
    zoom_level = calculate_zoom_level(distance_km)
    
    encoded_location1 = f"{origin_lat},{origin_lon}"
    encoded_location2 = f"{destination_lat},{destination_lon}"
    parameters = {
        "center": f"{encoded_location1}|{encoded_location2}",
        "size": "400x400",
        "zoom": zoom_level,  # Use calculated zoom level
        "markers": f"{encoded_location1}|{encoded_location2}",
        "path": f"color:red|{encoded_location1}|{encoded_location2}",
        "key": api_key
    }
    url = base_url + "&".join([f"{key}={value}" for key, value in parameters.items()])
    return url

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
    try:
        if directions and "routes" in directions and directions["routes"]:
            steps = directions["routes"][0]["legs"][0]["steps"]
            formatted_steps = format_directions(steps)
            for step in formatted_steps:
                directions_text += step + "\n"
        else:
            raise KeyError("Directions data is incomplete or missing.")
    except KeyError as e:
        directions_text = f"Failed to parse directions: {e}"
    return directions_text

def get_directions(origin = home_address, destination = work_address, mode = "transit", **kwargs):   
    home_address, work_address = get_addresses(username)
    
    print(origin)
    print(destination)
    if(origin == "" or origin == None or origin == "home"):
        origin = home_address
    elif(origin == "work"):
        origin = work_address
    if(destination == "" or destination == None or destination == "work"):
        destination = work_address
    elif(destination == "home"):
        destination = home_address
    if(mode == "" or mode == None or mode == "home"):
        mode = "transit"
    
    print(origin)
    print(destination)
    print(mode)
    api_key = API_KEY

    map_image = build_static_map_url(origin, destination, api_key) #i'm gonna insert this as the src in an <img> tag
    
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
        return "Failed to fetch directions."
    
    '''
    map_data = {
        "origin": origin,
        "destination": destination,
        "map": "./images/cet.png",
        "directions": "Error fetching directions"
    }#'''
    eel.showMap(map_data)
    return "map test"
    #return directions #gpt will respond to user with directions