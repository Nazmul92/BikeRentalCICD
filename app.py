import json
import pickle
import joblib
from flask import Flask, request, app, jsonify, url_for, render_template
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the model
bike_model = pickle.load(open('BikeShareModel.pkl', 'rb'))
scaling_model = pickle.load(open('scaling-model.pkl','rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    data = request.json['data']
    print(data)
    print(np.array(list(data.values())).reshape(1, -1))
    new_data = np.array(list(data.values())).astype('float64').reshape(1, -1)
    output = bike_model.predict(new_data)
    print(output[0])
    return jsonify(output[0])

@app.route('/predict', methods=['POST'])
def predict():
    # Get user input from the form
    data = [float(x) for x in request.form.values()]  # data is a list
    
    # do scaling for only nurerical columns
    
    scaled_data = scaling_model.fit_transform([data])

    # Convert data to numpy array and reshape for prediction
    input_data = np.array(scaled_data).astype('float64').reshape(1, -1)

    # Make prediction
    output = bike_model.predict(input_data)[0]

    # Render the result
    return render_template("home.html", prediction_text=f"Total Rentals: {output:.2f}")

if __name__ == "__main__":
    app.run(debug=True)