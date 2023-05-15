import heapq
from geopy.distance import distance
import streamlit as st
import streamlit_folium
from streamlit_folium import folium_static
import folium

# Define the base location and its coordinates
base_location = (6.902186, 79.919317)

# Define the truck capacities and their corresponding dustbin filling rate ranges
truck_capacities = {
    'A': (1, 3),
    'B': (4, 7),
    'C': (8, 20)
}

# Define the locations and their coordinates, along with the dustbin filling rates
locations = {
    'Location 1': (6.888136, 79.869102, 7),
    'Location 2': (6.945807, 79.913755, 5),
    'Location 3': (6.910571, 79.892075, 8),
    'Location 4': (6.913320, 79.857913, 2),
    'Location 5': (6.915242, 79.860805, 8),
    'Location 6': (6.905158, 79.851642, 7),
    'Location 7': (6.922649, 79.862037, 9),
    'Location 8': (6.914665, 79.972227, 6),
    'Location 9': (6.881169, 79.890561, 5),
    'Location 10': (6.947261, 79.869701, 8)
}

# Calculate the distance between the base location and each location
distances = {location: distance(base_location, coord[:2]).meters for location, coord in locations.items()}

# Sort the locations based on their distances from the base location
sorted_locations = sorted(locations.items(), key=lambda x: distances[x[0]])

# Initialize empty routes for each truck
truck_routes = {
    'A': [],
    'B': [],
    'C': []
}

# Initialize counters for the number of locations assigned to each truck
truck_counters = {
    'A': 0,
    'B': 0,
    'C': 0
}

# Iterate through the sorted locations
for location, coord in sorted_locations:
    # Determine the appropriate truck for the location based on its dustbin filling rate
    filling_rate = coord[2]
    truck = None
    for key, value in truck_capacities.items():
        if value[0] <= filling_rate <= value[1]:
            truck = key
            break
    
    # Check if the current truck's capacity is exceeded by adding the location
    if truck_counters[truck] >= 5 or truck_capacities[truck][1] < filling_rate:
        # Start a new truck route
        truck = 'A' if truck_counters['A'] < 5 else 'B' if truck_counters['B'] < 5 else 'C'
        truck_counters[truck] = 0
    
    # Add the location to the current truck's route
    truck_routes[truck].append(location)
    truck_counters[truck] += 1

# Initialize the map centered around the base location
m = folium.Map(location=base_location, zoom_start=13)

# Add markers for the base location and each location
folium.Marker(base_location, popup='Base Location').add_to(m)
for location, coord in locations.items():
    folium.Marker(coord[:2], popup=location).add_to(m)

# Initialize colors for different truck routes
colors = ['red', 'blue', 'green']

# Add polylines for each truck route
for i, (truck, route) in enumerate(truck_routes.items()):
    # Get the color for the current truck route
    color = colors[i % len(colors)]
    
    # Generate the coordinates for the truck route
    truck_route = [base_location] + [locations[loc][:2] for loc in route]
    
    # Add the polyline for the truck route
    folium.PolyLine(locations=truck_route, color=color, weight=2.5, opacity=0.8).add_to(m)

# Display the map in Streamlit using st.write and folium_static
st.title("Truck Routes")
folium_static(m)

# Display the truck routes in Streamlit using st.write
for truck, route in truck_routes.items():
    st.write(f"Truck {truck} Route:")
    for location in route:
        st.write(location)

