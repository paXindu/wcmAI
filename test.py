import streamlit as st
import numpy as np
import pickle


model = pickle.load(open('model.pkl', 'rb'))


def run_program(userin, num_iterations, truck_capacity):

    i = [1] + [0] * (num_iterations - 1)

    # Create a list of truck capacity and numbers
    truck_capacity_list = [3, 2, 5, 1, 7]
    truck_numbers = ['LM-645', 'LM-789', 'LM-234', 'LM-567', 'LM-890']

    # Initialize the route with the first location
    route = [0]

    # Calculate waste filling rate for each location and add it to the route
    for j in range(num_iterations-1):
        i = [int(k == j) for k in range(num_iterations)]
        filling_rate = int(model.predict(np.array([userin + i]))[0])

        # Find the index of the truck with the smallest capacity that can handle the waste
        suitable_truck_idx = np.argmin(
            [abs(filling_rate - cap) for cap in truck_capacity_list])
        suitable_truck_number = truck_numbers[suitable_truck_idx]
        suitable_truck_capacity = truck_capacity_list[suitable_truck_idx]

        # Add the current location and the suitable truck to the route
        route.append((j+1, filling_rate, suitable_truck_number,
                     suitable_truck_capacity))

        # Remove the suitable truck from the list of available trucks
        truck_capacity_list.pop(suitable_truck_idx)
        truck_numbers.pop(suitable_truck_idx)

    # Add the last location to the route
    route.append((num_iterations, 0, '', 0))

    # Initialize the total distance traveled
    total_distance = 0

    # Calculate the route distance using the nearest neighbor algorithm
    for i in range(len(route)-1):
        distance = np.sqrt((route[i+1][0]-route[i][0])
                           ** 2 + (route[i+1][1]-route[i][1])**2)
        total_distance += distance

    # Display the optimized route and the total distance traveled
    st.write(
        f"Optimized route: {[r[0] for r in route]}, Total distance: {total_distance} units")

    for location in route:
        st.write(
            f"Location {location[0]}: Waste filling rate: {location[1]} tons, Suitable truck: {location[2]} ({location[3]} tons)")


st.title("Waste Filling rate Prediction")

temp = st.number_input("Enter Temperature in C:",
                       min_value=10, max_value=50, step=1)
rainfall = st.number_input("Enter Rainfall in mm:",
                           min_value=0, max_value=50, step=1)
userin = [temp, rainfall]

num_iterations = st.slider(
    "Select number of location you need:", min_value=1, max_value=10)

# Create a list of truck capacities
truck_capacity = [3, 2, 5, 1, 7]

if st.button("Run Program"):
    run_program(userin, num_iterations, truck_capacity)
