import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline, CustomData


st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #667eea, #764ba2);
    }
    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: bold;
        color: white;
        margin-bottom: 30px;
    }
    .stButton>button {
        background-color: #00c6ff;
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #0072ff;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-title">🌍 Climate Visibility Prediction</div>', unsafe_allow_html=True)

# Inputs
col1, col2 = st.columns(2)

with col1:
    temp = st.number_input("Temperature (F)")
    humidity = st.number_input("Humidity (%)")
    wind_speed = st.number_input("Wind Speed")

with col2:
    wind_dir = st.number_input("Wind Direction")
    pressure = st.number_input("Pressure")

date = st.date_input("Select Date")
time = st.time_input("Select Time")

# Prediction
if st.button("Predict"):
    try:
        data = CustomData(
            DRYBULBTEMPF=temp,
            RelativeHumidity=humidity,
            WindSpeed=wind_speed,
            WindDirection=wind_dir,
            SeaLevelPressure=pressure,
            year=date.year,
            month=date.month,
            day=date.day,
            hour=time.hour
        )

        df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        result = predict_pipeline.predict(df)

        pred = round(result[0], 2)

        # Simple output (no extra logic)
        st.success(f"Visibility: {pred} km")

    except Exception as e:
        st.error(f"Error: {e}")