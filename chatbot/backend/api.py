# app.py - Run this after training the model to serve predictions
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
import numpy as np

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Enable CORS for all routes with specific origins

# Define features used by the model
features = [
    "no_of_dependents", "income_annum", "loan_amount", "loan_term", "cibil_score",
    "residential_assets_value", "commercial_assets_value",
]

# Load saved models
def load_models():
    if not os.path.exists('loan_model.joblib'):
        return None, None
        
    try:
        model = joblib.load('loan_model.joblib')
        scaler = joblib.load('scaler.joblib')
        return model, scaler
    except Exception as e:
        print(f"Error loading models: {e}")
        return None, None

# Load models at startup
model, scaler = load_models()
if model is None or scaler is None:
    print("⚠️ Warning: Model or scaler not found. Please run train_model.py first.")
    print("API will return an error for prediction requests")

@app.route('/predict', methods=['POST'])
def predict():
    # Check if model is loaded
    if model is None or scaler is None:
        return jsonify({
            "error": "Model not loaded. Please train the model first."
        }), 503  # Service Unavailable
    
    try:
        # Get input data from request
        data = request.json
        
        # Validate required fields
        for field in features:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Convert data to appropriate types and validate ranges
        try:
            input_data = {
                "no_of_dependents": int(data["no_of_dependents"]),
                "income_annum": float(data["income_annum"]),
                "loan_amount": float(data["loan_amount"]),
                "loan_term": int(data["loan_term"]),
                "cibil_score": int(data["cibil_score"]),
                "residential_assets_value": float(data["residential_assets_value"]),
                "commercial_assets_value": float(data["commercial_assets_value"]),
            }
            
            # Additional validation
            if not (300 <= input_data["cibil_score"] <= 900):
                return jsonify({"error": "CIBIL score must be between 300 and 900"}), 400
                
            if input_data["loan_term"] <= 0:
                return jsonify({"error": "Loan term must be positive"}), 400
                
            if input_data["loan_amount"] <= 0:
                return jsonify({"error": "Loan amount must be positive"}), 400
                
        except ValueError as e:
            return jsonify({"error": f"Invalid data format: {str(e)}"}), 400
        
        # Convert to DataFrame
        input_df = pd.DataFrame([input_data], columns=features)
        
        # Scale the input data
        input_scaled = scaler.transform(input_df)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        
        # Get probability if model supports it (for more detailed feedback)
        probability = None
        if hasattr(model, 'predict_proba'):
            try:
                probability = model.predict_proba(input_scaled)[0][1]  # Probability of class 1
            except:
                pass  # Not all models support probability
        
        # Return result
        response = {
            "loan_status": "Approved" if prediction == 1 else "Rejected",
            "input_received": input_data
        }
        
        if probability is not None:
            response["approval_confidence"] = float(probability)
            
        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "message": "Loan Eligibility API",
        "status": "Model loaded" if model is not None else "Model not loaded",
        "endpoints": {
            "/predict": "POST request with loan application data",
            "/health": "GET request to check API health"
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)