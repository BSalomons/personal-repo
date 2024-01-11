import folium
from geopy.geocoders import Nominatim
import time




# List of locations in your itinerary
locations = [
    "Heathrow Airport, London, UK", "Cotswold Distillery, UK", "Cockermouth, Lake District, UK", 
    "Lakes Distillery, UK", "Clydeside Distillery, Glasgow, UK", "George Square, Glasgow, UK", 
    "Ardrossan ferry port, UK", "Brodick, Isle of Arran, UK", "Lagg Distillery, Isle of Arran, UK", 
    "Lochranza Distillery, Isle of Arran, UK", "Lochranza ferry port, Isle of Arran, UK", 
    "Campbeltown, UK", "Springbank Distillery, Campbeltown, UK", "Kennacraig, UK", 
    "Islay, UK", "Bridgend, Islay, UK", "Oban, UK", "Mallaig, UK", "Armadale, Skye, UK", 
    "Torabhaig Distillery, Skye, UK", "Sconser, Skye, UK", "Raasay, UK", "Talisker Distillery, Skye, UK", 
    "Inverness, UK", "Dalmore Distillery, UK", "Glenmorangie Distillery, UK", "Balblair Distillery, UK", 
    "Tomatin Distillery, UK", "Glenfarclas Distillery, UK", "Balvenie Distillery, UK", 
    "Craigellachie, UK", "Glencadam Distillery, UK", "Edinburgh, UK", "Arthur's Seat, Edinburgh, UK", 
    "Holyrood Distillery, Edinburgh, UK", "Whiski Room, Edinburgh, UK", "Scotch Whisky Experience, Edinburgh, UK", 
    "Borders Distillery, UK", "Notting Hill Gate, London, UK"
]

# Initialize the geolocator
geolocator = Nominatim(user_agent="uk_tour_map")

# Create a map object (starting with the first location)
location = geolocator.geocode(locations[0])
map = folium.Map(location=[location.latitude, location.longitude], zoom_start=6)

# Loop through the locations and add them to the map
for place in locations:
    time.sleep(1)  # to avoid hitting request limits
    location = geolocator.geocode(place)
    if location:
        folium.Marker([location.latitude, location.longitude], popup=place).add_to(map)

# Save the map to an HTML file
map.save("distillery_tour_map.html")
