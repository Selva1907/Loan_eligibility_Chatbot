
# 💬 Loan Approval Prediction Chatbot (Full Stack)

This project is a full-stack chatbot application that predicts **loan approval status** based on user inputs. It uses a **Logistic Regression ML model** in the Flask backend and provides a **conversational chatbot interface** via React in the frontend.

---

## 🗂️ Project Structure

```
chatbot/
├── backend/
│   ├── Appi.py                # Flask API server (main backend entry)
│   ├── model.py               # Model training and prediction logic
│   ├── loan_model.pkl         # Trained logistic regression model
│   ├── scaler.pkl             # Scaler for standardizing features
│   ├── label_encoders.pkl     # Encoders for categorical variables
├── node_modules/              # Node.js dependencies (auto-generated)
├── public/
│   └── index.html             # HTML entry point for React app
├── src/
│   ├── components/
│   │   ├── Chatbot.js         # Chatbot React component
│   │   └── Chatbot.css        # Styling for chatbot UI
│   ├── App.js                 # Main React App component
│   └── App.css                # App-wide CSS
```

---

## 🚀 Getting Started

### 🧠 1. Train the Model

Navigate to the backend folder and run `model.py` to train and save the model:

```bash
cd backend
python model.py
```

Update the path to your dataset in the script:

```python
data_path = r"path_to_your_dataset.csv"
```

---

### 🔌 2. Start the Flask Backend API

```bash
python Appi.py
```

- Server runs on: `http://localhost:5000`
- Endpoint: `POST /predict`

---

### 🌐 3. Start the React Frontend

In the project root (where `package.json` is located), run:

```bash
npm install
npm start
```

Frontend runs on: `http://localhost:3000`

---

## 🔄 API Endpoint

- **URL:** `http://localhost:5000/predict`
- **Method:** `POST`
- **Expected JSON Input:**

```json
{
  "no_of_dependents": 2,
  "income_annum": 500000,
  "loan_amount": 200000,
  "loan_term": 360,
  "cibil_score": 750,
  "residential_assets_value": 1000000,
  "commercial_assets_value": 500000
}
```

- **Response:**

```json
{
  "loan_status": "Approved"
}
```

---

## 💬 Chatbot Flow Example

1. **Bot:** How many dependents do you have?  
2. **User:** 2  
3. **Bot:** What is your annual income?  
4. *(continues through inputs)*  
5. **Bot (final):** ✅ Your loan is **Approved**

---

## 🧰 Tech Stack

- **Frontend:** React, JavaScript, Axios
- **Backend:** Flask (Python)
- **ML Model:** Logistic Regression (`scikit-learn`)
- **Others:** Joblib, Pandas, Numpy, Label Encoding

---

## 📦 Dependencies

### Python

```bash
pip install flask flask-cors pandas numpy scikit-learn joblib
```

### React

```bash
npm install
```

---

## 📌 Notes

- Make sure CORS is enabled in Flask to allow requests from React.
- Update `Appi.py` if running backend on a different port.

---

## 🧪 To Test

Use this sample input to test:

```json
{
  "no_of_dependents": 1,
  "income_annum": 600000,
  "loan_amount": 150000,
  "loan_term": 180,
  "cibil_score": 720,
  "residential_assets_value": 800000,
  "commercial_assets_value": 200000
}
```
