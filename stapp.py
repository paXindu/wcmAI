import streamlit as st
import numpy as np
import pickle


model = pickle.load(open('model.pkl', 'rb'))

def run_program(userin, num_iterations):
    
    i = [1] + [0] * (num_iterations - 1)

    
    for j in range(num_iterations):
        
        i = [int(k == j) for k in range(num_iterations)]

        
        features = np.array([userin + i])

        
        pred = int(model.predict(features)[0])

        
        st.write(f"Location {j+1}: {pred}")


st.title("Waste Filling rate Prediction")


temp = st.number_input("Enter Temperature in C:",min_value=10, max_value=50, step=1)
rainfall = st.number_input("Enter Rainfall in mm:",min_value=0, max_value=50, step=1)
userin = [temp, rainfall]


num_iterations = st.slider("Select number of location you need:", min_value=1, max_value=10)


if st.button("Run Program"):
    run_program(userin, num_iterations)