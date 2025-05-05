import os
import pickle
import numpy as np
import pandas as pd
from flask import Flask, request, render_template
from utils.helpers import label_encode
import joblib
from config.paths_config import *
from datetime import datetime

app = Flask(__name__)

model = joblib.load(MODEL_SAVE_PATH)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get form data
        form = request.form
        input_data = {
            "hotel": form["hotel"],
            "lead_time": int(form["lead_time"]),
            "arrival_date_month": int(form["arrival_date_month"]),
            "arrival_date_week_number": int(form["arrival_date_week_number"]),
            "arrival_date_day_of_month": int(form["arrival_date_day_of_month"]),
            "stays_in_weekend_nights": int(form["stays_in_weekend_nights"]),
            "stays_in_week_nights": int(form["stays_in_week_nights"]),
            "adults": int(form["adults"]),
            "children": int(form["children"]),
            "babies": int(form["babies"]),
            "meal": form["meal"],
            "market_segment": form["market_segment"],
            "distribution_channel": form["distribution_channel"],
            "is_repeated_guest": int(form["is_repeated_guest"]),
            "previous_cancellations": int(form["previous_cancellations"]),
            "previous_bookings_not_canceled": int(form["previous_bookings_not_canceled"]),
            "reserved_room_type": form["reserved_room_type"],
            "deposit_type": form["deposit_type"],
            "agent": int(form["agent"]),
            "company": int(form["company"]),
            "customer_type": form["customer_type"],
            "adr": float(form["adr"]),
            "required_car_parking_spaces": int(form["required_car_parking_spaces"]),
            "total_of_special_requests": int(form["total_of_special_requests"])
        }
        
        # Handle reservation_status_date (assuming it comes in YYYY-MM-DD format)
        reservation_status_date = form["reservation_status_date"]
        input_data["reservation_status_date"] = pd.to_datetime(reservation_status_date)

        # Add columns for year, month, day (based on reservation_status_date)
        input_data["year"] = input_data["reservation_status_date"].year
        input_data["month"] = input_data["reservation_status_date"].month
        input_data["day"] = input_data["reservation_status_date"].day

        # Compute total_guests
        input_data["total_guests"] = input_data["adults"] + input_data["children"] + input_data["babies"]

        # Convert input data to DataFrame
        df = pd.DataFrame([input_data])

        # Identify categorical columns to encode (from feature_engineering.py)
        categorical_cols = ['hotel', 'meal', 'market_segment', 'distribution_channel', 'reserved_room_type', 'deposit_type', 'customer_type']
        df, _ = label_encode(df, categorical_cols)  # Apply same label encoding logic

        # Ensure columns are in correct order (matching training)
        model_features = model.feature_names_in_
        df = df.reindex(columns=model_features)

        # Prediction
        prediction = model.predict(df)[0]
        result = "Booking will be Canceled" if prediction == 1 else "Booking will NOT be Canceled"

        return render_template("index.html", prediction=result)

    except Exception as e:
        return render_template("index.html", prediction=f"Error: {e}")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)