import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline, CustomData

st.title("Climate Visibility Prediction")

# Inputs
temp = st.number_input("Temperature (F)")
humidity = st.number_input("Relative Humidity (%)")
wind_speed = st.number_input("Wind Speed")
wind_dir = st.number_input("Wind Direction")
pressure = st.number_input("Sea Level Pressure")

date = st.date_input("Select Date")
time = st.time_input("Select Time")

if st.button("Predict"):
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

    st.success(f"Visibility: {round(result[0],2)} km")