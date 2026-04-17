import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object

class PredictPipeline():
    def __init__(self):
        pass

    def predict(self,features):
        try:
            model_path = 'artifacts/model.pkl'
            preprocessor_path = 'artifacts/preprocessor.pkl'

            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)

            
            print("========== INPUT ==========")
            print(features)
            print("Columns:", features.columns)

            data_scaled  = preprocessor.transform(features)

            print("========== SCALED ==========")
            print(data_scaled)
            

            preds = model.predict(data_scaled)

            print("========== PREDICTION ==========")
            print(preds)

            return preds

        except Exception as e:
            raise CustomException(e,sys)

class CustomData():
    def __init__(self,
            DRYBULBTEMPF: float ,
            RelativeHumidity: float, WindSpeed: float, WindDirection: float,
            SeaLevelPressure: float, year: int, month: int, day: int, hour: int):
        
            self.Dry_Bulb_Tempf = DRYBULBTEMPF
            self.Relative_Humidity = RelativeHumidity

            self.Wind_Speed = WindSpeed
            self.Wind_Direction = WindDirection
            self.SeaLevel_Pressure =  SeaLevelPressure
            self.year = year
            self.month = month
            self.day = day
            self.hour = hour

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "DRYBULBTEMPF": [self.Dry_Bulb_Tempf],
                "RelativeHumidity" : [self.Relative_Humidity],
                "WindSpeed": [self.Wind_Speed],
                "WindDirection": [self.Wind_Direction],
                "SeaLevelPressure": [self.SeaLevel_Pressure],
                "year": [self.year],
                "month": [self.month],
                "day": [self.day],
                "hour": [self.hour]
            }

            return pd.DataFrame(custom_data_input_dict)
        except Exception as e:
             raise CustomException(e,sys)
        

