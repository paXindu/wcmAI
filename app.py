import numpy as np
import pickle

model = pickle.load(open('model.pkl', 'rb'))
# model.predict(features)

# Initialize the i list
i = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# Define the user input values
userin = [21, 30]

# Define the number of iterations you want to perform
num_iterations = 10

# Loop to modify the i list and create the features array
for j in range(num_iterations):
    # Modify the i list by setting the j-th element to 1 and the rest to 0
    i = [int(k == j) for k in range(num_iterations)]
    
    # Create the features array with the updated i list
    features = np.array([userin + i])
    
    # Use the features array to make predictions
    pred = model.predict(features)
    
    # Print the predictions
    pred = int(model.predict(features)[0])
    print(pred)