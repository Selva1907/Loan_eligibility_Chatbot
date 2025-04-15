from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd

# Initialize Flask app
app = Flask(__name__)

# Enable CORS to allow requests from frontend
CORS(app, resources={r"/predict": {"origins": "*"}})

# Load the model and encoders
model = joblib.load("loan_model.pkl")  # Your trained model
label_encoders = joblib.load("label_encoders.pkl")  # Encoders for categorical variables

# Define features for the input data
features = [
    "no_of_dependents",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
]

@app.route("/")
def home():
    return "✅ Loan Eligibility API is running. Use /predict to check eligibility."


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON data from request
        data = request.get_json()

        # Validate required inputs
        for feature in features:
            if feature not in data:
                return jsonify({"error": f"Missing input: {feature}"}), 400

        # Create a DataFrame from input data
        input_data = pd.DataFrame([data])

        print("Input Data:", input_data)
        
        # Make prediction using the trained model
        prediction = model.predict(input_data)[0]

        # Return result (1 for Approved, 0 for Rejected)
        result = "Approved" if prediction == 1 else "Rejected"
        return jsonify({"loan_status": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Run on 0.0.0.0 to allow external access
    app.run(host="0.0.0.0", port=5000, debug=True)
