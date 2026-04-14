import sys
from dataclasses import dataclass
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.exception import CustomException
from src.logger import logging
import os

from src.utils import save_object


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('artifacts', "preprocessor.pkl")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformer_object(self, numerical_columns):
        try:
            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler())
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num_pipeline", num_pipeline, numerical_columns)
                ]
            )

            return preprocessor

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self, train_path, test_path):

        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Data loaded successfully")

            
            train_df.columns = train_df.columns.str.strip()
            test_df.columns = test_df.columns.str.strip()

           
            for df in [train_df, test_df]:
                df['DATE'] = pd.to_datetime(df['DATE'])

                df['year'] = df['DATE'].dt.year
                df['month'] = df['DATE'].dt.month
                df['day'] = df['DATE'].dt.day
                df['hour'] = df['DATE'].dt.hour

            
            train_df.drop(columns=['DATE'], inplace=True)
            test_df.drop(columns=['DATE'], inplace=True)

            target_column_name = "VISIBILITY"

            
            if target_column_name not in train_df.columns:
                raise Exception(f"{target_column_name} not found in dataframe")

            
            numerical_columns = [
                'DRYBULBTEMPF', 'RelativeHumidity',
                'WindSpeed', 'WindDirection',
                'SeaLevelPressure',
                'year', 'month', 'day', 'hour'
            ]

           
            for col in numerical_columns:
                if col not in train_df.columns:
                    raise Exception(f"Column missing: {col}")

            preprocessing_obj = self.get_data_transformer_object(numerical_columns)

            # Split input & target
            input_feature_train_df = train_df.drop(columns=[target_column_name])
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=[target_column_name])
            target_feature_test_df = test_df[target_column_name]

            logging.info("Applying preprocessing")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, target_feature_train_df.values]
            test_arr = np.c_[input_feature_test_arr, target_feature_test_df.values]

            # Save preprocessor
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Preprocessing completed successfully")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)