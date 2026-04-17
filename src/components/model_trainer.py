import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Splitting training and test data")

            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(random_state=42),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoost": CatBoostRegressor(verbose=False),
                "AdaBoost": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error']
                },
                "Random Forest": {
                    'n_estimators': [100, 200,300],
                    'max_depth':[5,10,15],
                    'min_samples_split':[2,5,10]
                },
                "Gradient Boosting": {
                    'learning_rate': [0.1, 0.05],
                    'n_estimators': [50, 100],
                    'subsample': [0.8, 1.0]
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    'learning_rate': [0.1, 0.05],
                    'n_estimators': [100,200]
                },
                "CatBoost": {
                    'depth': [6, 8],
                    'learning_rate': [0.01, 0.05],
                    'iterations': [100,200]
                },
                "AdaBoost": {
                    'learning_rate': [0.1, 0.05],
                    'n_estimators': [50, 100]
                }
            }

            best_model = None
            best_score = -1
            best_model_name = ""

            #Training + Hyperparameter Tuning
            for model_name, model in models.items():
                logging.info(f"Training {model_name}")

                param_grid = params[model_name]

                if param_grid:
                    grid = GridSearchCV(model, param_grid, cv=3, scoring='r2', n_jobs=-1,verbose=2)
                    grid.fit(X_train, y_train)
                    trained_model = grid.best_estimator_
                else:
                    model.fit(X_train, y_train)
                    trained_model = model

                # Evaluate
                y_pred = trained_model.predict(X_test)
                score = r2_score(y_test, y_pred)

                logging.info(f"{model_name} R2 Score: {score}")

                if score > best_score:
                    best_score = score
                    best_model = trained_model
                    best_model_name = model_name

            if best_score < 0.6:
                raise CustomException("No good model found", sys)

            logging.info(f"Best Model: {best_model_name} with score {best_score}")

            
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            return best_score

        except Exception as e:
            raise CustomException(e, sys)
