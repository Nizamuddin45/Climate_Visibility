from flask import Flask, render_template, request
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from datetime import datetime

application = Flask(__name__)
app=application

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/predict_page")
def predict_page():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        temp = float(request.form["temp"])
        humidity = float(request.form["humidity"])
        wind_speed = float(request.form["wind_speed"])
        wind_direction = float(request.form["wind_direction"])
        pressure = float(request.form["pressure"])

        dt = request.form["datetime"]
        dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M")

        data = CustomData(
            DRYBULBTEMPF=temp,
            RelativeHumidity=humidity,
            WindSpeed=wind_speed,
            WindDirection=wind_direction,
            SeaLevelPressure=pressure,
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour
        )

        pred_df = data.get_data_as_data_frame()

        pipeline = PredictPipeline()
        result = pipeline.predict(pred_df)

        return render_template("index.html",
                               prediction_text=f"Visibility: {round(result[0],2)}")

    except Exception as e:
        return render_template("index.html",
                               prediction_text=f"Error: {str(e)}")


if __name__ == "__main__":
    app.run(debug=True)