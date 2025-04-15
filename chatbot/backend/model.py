# train_model.py - Run this first to train and save the model
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report

# Define features used by the model
features = [
    "no_of_dependents",
    "income_annum",
    "loan_amount",
    "loan_term",
    "cibil_score",
    "residential_assets_value",
    "commercial_assets_value",
]


def train_and_save_model(data_path):
    print(f"Loading data from {data_path}")
    # Load dataset
    df = pd.read_csv(data_path)

    # Encode categorical variables
    label_encoders = {}
    for col in ["education", "self_employed", "loan_status"]:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le  # Save encoders for future use

    # Drop unnecessary columns
    df.drop(columns=["loan_id"], inplace=True)

    # Check for missing values
    if df.isnull().sum().sum() > 0:
        df.fillna(df.median(), inplace=True)  # Handle missing values

    # Separate features and target
    X = df[features]
    y = df["loan_status"]





    # Standardize numerical features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # Train model
    model = LogisticRegression(class_weight="balanced")
    model.fit(X_train, y_train)

    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Save model and encoders
    joblib.dump(model, "loan_model.pkl")
    joblib.dump(scaler, "scaler.pkl")
    joblib.dump(label_encoders, "label_encoders.pkl")

    print("Model, scaler, and encoders saved successfully")
    return model, scaler, label_encoders


def load_model_and_predict(input_data):
    """
    Load the saved model, scaler, and encoders, and make predictions.

    Args:
        input_data (dict): A dictionary containing the input features.

    Returns:
        dict: A dictionary containing the prediction and probabilities.
    """
    # Load the saved model, scaler, and encoders
    model = joblib.load("loan_model.pkl")
    scaler = joblib.load("scaler.pkl")
    label_encoders = joblib.load("label_encoders.pkl")

    # Prepare input data
    input_df = pd.DataFrame([input_data])
    input_df = input_df[features]  # Ensure correct feature order
    input_scaled = scaler.transform(input_df)

    # Make prediction
    prediction = model.predict(input_scaled)[0]
    prediction_proba = model.predict_proba(input_scaled)[0]

    # Decode prediction if necessary
    loan_status_encoder = label_encoders.get("loan_status")
    if loan_status_encoder:
        prediction = loan_status_encoder.inverse_transform([prediction])[0]

    return {
        "prediction": prediction,
        "probability": {
            "approved": prediction_proba[1],
            "rejected": prediction_proba[0],
        },
    }

# Example usage:
# input_data = {
#     "no_of_dependents": 2,
#     "income_annum": 500000,
#     "loan_amount": 200000,
#     "loan_term": 360,
#     "cibil_score": 750,
#     "residential_assets_value": 1000000,
#     "commercial_assets_value": 500000,
# }
# result = load_model_and_predict(input_data)
# print(result)


if __name__ == "__main__":
    # Update this path to your dataset location
    data_path = r"C:\Users\selva\Downloads\archive (1)\loan_approval_dataset.csv"
    train_and_save_model(data_path)
