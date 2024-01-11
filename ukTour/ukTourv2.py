import requests
import folium
import polyline
import time
from geopy.geocoders import Nominatim
from folium.plugins import MarkerCluster, PolyLineTextPath

def get_directions(origin, destination, api_key):
    endpoint = f"https://maps.googleapis.com/maps/api/directions/json?origin={origin}&destination={destination}&key={api_key}"
    # Make a request to the API
    response = requests.get(endpoint)
    # Parse the response JSON to get the route
    directions = response.json()
    # Extract polyline
    encoded_polyline = directions['routes'][0]['overview_polyline']['points']
    return polyline.decode(encoded_polyline)

# Your itinerary
itinerary = [
    {"date": "Sep 5, 2025", "location": "Heathrow Airport, London, UK", "details": "start"},
    {"date": "Sep 5, 2025", "coords": [52.02578227220297, -1.5662283509382824], "label": "Cotswolds Distillery Visitor Centre, Whichford Road, Stourton, Shipston-on-Stour, UK", "details": "tasting"},
    {"date": "Sep 5, 2025", "location": "Cockermouth, UK", "details": "end"},
    {"date": "Sep 6, 2025", "location": "Lakes Distillery, UK", "details": "tasting"},
    {"date": "Sep 6, 2025", "location": "Clydeside Distillery, Glasgow, UK", "details":"tasting"},
    {"date": "Sep 6, 2025", "location": "Glasgow, UK", "details": "end"},
    {"date": "Sep 7, 2025", "location": "Ardrossan Ferry Terminal, Ardrossan, UK", "details":"start"},
    {"date": "Sep 7, 2025", "location": "Brodick, Isle of Arran, UK", "details": "start"},
    {"date": "Sep 7, 2025", "coords": [55.44577461354579, -5.248004221613457], "label": "Lagg Distillery, Kilmory, Isle of Arran, UK", "details": "tasting"},
    {"date": "Sep 7, 2025", "location": "Brodick, Isle of Arran, UK", "details": "end"},
    {"date": "Sep 8, 2025", "coords": [55.69782407377481, -5.275397996982812], "label": "Lochranza Distillery, Lochranza, Isle of Arran, UK", "details": "tasting"},
    {"date": "Sep 8, 2025", "coords": [55.7078091166635, -5.301949676494947], "label": "Lochranza Ferry Terminal, Slipway, Lochranza, Isle of Arran, UK", "details": "start"},
    {"date": "Sep 8, 2025", "location": "Campbeltown, UK", "details": "end"},
    {"date": "Sep 9, 2025", "location": "Springbank Distillery, Campbeltown, UK", "details": "tasting"},
    {"date": "Sep 9, 2025", "location": "Kilkerran Distillery, Campbeltown, UK", "details": "tasting"},
    {"date": "Sep 9, 2025", "location": "Glen Scotia Distillery, Campbeltown, UK", "details": "tasting"},
    {"date": "Sep 9, 2025", "location": "Campbeltown, UK", "details": "end"},
    {"date": "Sep 10, 2025", "location": "Kennacraig, UK", "details": "start"},
    {"date": "Sep 10, 2025", "coords": [55.78695820229685, -6.430518697375225], "label": "Kilchoman Distillery, Bruichladdich, Isle of Islay, UK", "details": "tasting"},
    {"date": "Sep 10, 2025", "coords": [55.75688792226465, -6.289848803014897], "label": "Bowmore Distillery, School Street, Bowmore, Isle of Islay, UK", "details": "tasting"},
    {"date": "Sep 10, 2025", "coords": [55.78185984363014, -6.250026982170923], "label": "Bridgend, Isle of Islay, UK", "details": "end"},
    {"date": "Sep 11, 2025", "coords": [55.64056939710109, -6.108168937268014], "label": "Ardbeg Distillery, Port Ellen, Islay, UK", "details": "tasting"},
    {"date": "Sep 11, 2025", "coords": [55.86919163511476, -6.117426823613169], "label": "Ardnahoe Distillery, Ardnahoe, Port Askaig, Isle of Islay, UK", "details": "tasting"},
    {"date": "Sep 11, 2025", "coords": [55.88350370624749, -6.126697208811781], "label": "Bunnahabhain Distillery, Bunnahabhain, Isle of Islay, UK", "details": "tasting"},
    {"date": "Sep 11, 2025", "coords": [55.78185984363014, -6.250026982170923], "label": "Bridgend, Isle of Islay, UK", "details": "end"},
    {"date": "Sep 12, 2025", "location": "Kennacraig, UK", "details": "start"},
    {"date": "Sep 12, 2025", "location": "Oban, UK", "details": "start"},
    {"date": "Sep 12, 2025", "location": "Oban Distillery, UK", "details": "start"},
    {"date": "Sep 12, 2025", "location": "Mallaig, UK", "details": "start"},
    {"date": "Sep 12, 2025", "coords": [57.06517047931361, -5.901448787254494], "label": "Armadale, Isle of Skye, UK", "details": "end"},
    {"date": "Sep 13, 2025", "coords": [57.11287280031337, -5.848684627516856], "label": "Torabhaig Distillery, Teangue, Isle of Skye, UK", "details": "tasting"},
    {"date": "Sep 13, 2025", "location": "Raasay, Skye, UK", "details": "start"},
    {"date": "Sep 13, 2025", "coords": [57.35212816717851, -6.0741871188809355], "label": "Isle of Raasay Distillery, Kyle, UK", "details": "tasting"},
    {"date": "Sep 13, 2025", "coords": [57.312277870033256, -6.116078285721454], "label": "Sconser, Isle of Skye, UK", "details": "start"},
    {"date": "Sep 13, 2025", "coords": [57.3024437800875, -6.356842403858532], "label": "Talisker Distillery, Carbost, Isle of Skye, UK", "details": "tasting"},
    {"date": "Sep 13, 2025", "coords": [57.312277870033256, -6.116078285721454], "label": "Sconser, Isle of Skye, UK", "details": "end"},
    {"date": "Sep 14, 2025", "location": "Skye Bridge, UK", "details": "start"},
    {"date": "Sep 14, 2025", "location": "Loch Ness, UK", "details": "start"},    
    {"date": "Sep 14, 2025", "location": "Inverness, UK", "details": "end"},
    {"date": "Sep 15, 2025", "location": "Dalmore Distillery, UK", "details": "tasting"},
    {"date": "Sep 15, 2025", "location": "Dalmore Distillery, UK", "details": "tasting"},
    {"date": "Sep 15, 2025", "location": "Glenmorangie Distillery, UK", "details": "tasting"},
    {"date": "Sep 15, 2025", "location": "Balblair Distillery, UK", "details": "tasting"},
    {"date": "Sep 15, 2025", "location": "Inverness, UK", "details": "end"},
    {"date": "Sep 16, 2025", "location": "Tomatin Distillery, UK", "details": "tasting"},
    {"date": "Sep 16, 2025", "location": "Glenfarclas Distillery, UK", "details": "tasting"},
    {"date": "Sep 16, 2025", "location": "Balvenie Distillery, UK", "details": "tasting"},
    {"date": "Sep 16, 2025", "location": "Craigellachie, UK", "details": "end"},
    {"date": "Sep 17, 2025", "location": "Craigellachie Distillery, UK", "details": "tasting"},
    {"date": "Sep 17, 2025", "location": "Glencadam Distillery, UK", "details": "tasting"},
    {"date": "Sep 17, 2025", "location": "Edinburgh, UK", "details": "end"},
    {"date": "Sep 18, 2025", "location": "Arthur's Seat, Edinburgh, UK", "details": "start"},    
    {"date": "Sep 18, 2025", "location": "Holyrood Distillery, Edinburgh, UK", "details": "tasting"},
    {"date": "Sep 18, 2025", "location": "Whiski Rooms, North Bank Street, Edinburgh, UK", "details": "tasting"},
    {"date": "Sep 18, 2025", "location": "Scotch Whisky Experience, Edinburgh, UK", "details": "tasting"},
    {"date": "Sep 18, 2025", "location": "Edinburgh, UK", "details": "end"},
    {"date": "Sep 19, 2025", "location": "Borders Distillery, UK", "details": "tasting"},
    {"date": "Sep 19, 2025", "location": "Notting Hill Gate, London, UK", "details": "end"},
    {"date": "Sep 20, 2025", "location": "Heathrow Airport, London, UK", "details": "start"},
]

api_key = 'AIzaSyC8zO3frn40ihOPbhc2jV_WsTR7GQyd2VQ'  # Replace with your actual API key

# Initialize your folium map (starting with the first location)
geolocator = Nominatim(user_agent="tour_map_script")
first_location = geolocator.geocode(itinerary[0]["location"])
map = folium.Map(location=[first_location.latitude, first_location.longitude], zoom_start=6)

# Initialize MarkerCluster
marker_cluster = MarkerCluster().add_to(map)

# Function to determine marker color based on details
def determine_marker_color(details):
    # Implement logic to determine color based on 'details'
    if "tasting" in details:
        return "blue"
    elif "start" in details:
        return "green"
    else:
        return "red"

# Loop through the itinerary to add markers
for i, stop in enumerate(itinerary):
    # Check if coordinates are provided
    if 'coords' in stop:
        latitude, longitude = stop['coords']
        location_label = stop['label']
    else:
        location = geolocator.geocode(stop["location"])
        if location:
            latitude, longitude = location.latitude, location.longitude
            location_label = stop["location"]
        else:
            print(f"Geocode failed for location: {stop['location']}")
            continue

    # Marker setup
    marker_color = determine_marker_color(stop["details"])
    popup_content = f"{stop['date']} - {location_label}"
    folium.Marker(
        [latitude, longitude],
        popup=popup_content,
        icon=folium.Icon(color=marker_color, icon="info-sign")
    ).add_to(marker_cluster)

    # Route setup (for all but the last point)
    if i < len(itinerary) - 1:
        # Determine the next stop's coordinates
        if 'coords' in itinerary[i + 1]:
            next_latitude, next_longitude = itinerary[i + 1]['coords']
        else:
            next_location = itinerary[i + 1]["location"]
            next_stop = geolocator.geocode(next_location)
            if next_stop:
                next_latitude, next_longitude = next_stop.latitude, next_stop.longitude
            else:
                print(f"Geocode failed for location: {next_location}")
                continue

        # Get directions and plot the route
        route = get_directions(f"{latitude},{longitude}",
                               f"{next_latitude},{next_longitude}", 
                               api_key)
        my_route = folium.PolyLine(route, color="blue", weight=2.5, opacity=1).add_to(map)
        PolyLineTextPath(my_route, "►", repeat=True, offset=8, attributes={'fill': 'black', 'font-weight': 'bold'}).add_to(map)

# Save the map
map.save('uk_tour_map2.html')
