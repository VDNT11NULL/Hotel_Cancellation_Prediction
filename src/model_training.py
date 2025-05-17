import os
import pandas as pd 
import numpy as np
import joblib
import lightgbm as lgbm
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score
from src.logger import get_logger
from utils.common_functions import read_yaml, load_data
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
import mlflow

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_op_path = model_output_path

        self.params_dict = LIGHTGBM_PARAMS
        self.random_search_params  = RANDOM_SEARCH_PARAMS

        
    def load_and_split_data(self):
        try:
            logger.info(f"Loading data (ML) from {self.train_path}")

            train_df = load_data(self.train_path)
            test_df = load_data(self.test_path)

            X_train, Y_train = train_df.drop(columns=['booking_status']), train_df['booking_status']
            X_test, Y_test = test_df.drop(columns=['booking_status']), test_df['booking_status']

            logger.info("Data Loading and spliting for model training Done!!")

            return X_train, Y_train, X_test, Y_test
        
        except Exception as e:
            logger.error(f"Error at load and split {e}")
            raise CustomException("Failed at load and split stage", e)
    
    def train_lgbm(self, X_train, Y_train):
        try:
            logger.info("Started LGBM model training")
            lgbm_model = lgbm.LGBMClassifier(random_state=self.random_search_params["random_state"])
            logger.info("Starting HP Tuning")

            # Optimized params
            self.random_search_params["n_iter"] = 5  # Fewer iterations
            self.random_search_params["cv"] = 3      # Fewer folds
            self.random_search_params["n_jobs"] = 2  # Limit parallelism

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.params_dict,
                n_iter=self.random_search_params["n_iter"],
                cv=self.random_search_params["cv"],
                n_jobs=self.random_search_params["n_jobs"],
                verbose=self.random_search_params["verbose"],
                scoring=self.random_search_params["scoring"]
            )

            logger.info("Starting our Model Training")
            random_search.fit(X_train, Y_train)

            logger.info("Hyperparameter Tuning Completed")

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best params are: {best_params}")
            return best_lgbm_model
            
        except Exception as e:
            logger.error(f"Error at training stage: {e}")
            raise CustomException("Failed at Training fn", e)
        
    def eval_model(self, model, X_test, Y_test):
        try:
            logger.info("Evaluating the model")
            Y_pred = model.predict(X_test)            

            accuracy = accuracy_score(Y_test, Y_pred)
            precision = precision_score(Y_test, Y_pred)
            recall = recall_score(Y_test, Y_pred)
            f1 = f1_score(Y_test, Y_pred)

            logger.info(f"Accuracy: {accuracy}")
            logger.info(f"Precision: {precision}")
            logger.info(f"Recall: {recall}")
            logger.info(f"F1 Score: {f1}")
            logger.info("Model evaluation completed")

            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1_score": f1
            }
        
        except Exception as e:
            logger.error(f"Error at model evaluation stage: {e}")
            raise CustomException("Failed at Model Evaluation stage", e)
        
    def save_model(self, model):
        try:
            logger.info("Saving the model")
            os.makedirs(os.path.dirname(self.model_op_path), exist_ok=True)
            joblib.dump(model, self.model_op_path)
            logger.info(f"Model saved at {self.model_op_path}")
        
        except Exception as e:
            logger.error(f"Error at model saving stage: {e}")
            raise CustomException("Failed at Model Saving stage", e)
        
    def run(self):
        try:
            logger.info("Started ML pipeline")
            
            with mlflow.start_run():
                logger.info("Starting with MLFlow experimentation")

                logger.info("Logging the training and testing dataset to MLFlow")
                X_train, Y_train, X_test, Y_test = self.load_and_split_data()
                mlflow.log_artifact(self.train_path, artifact_path = "datasets")
                mlflow.log_artifact(self.test_path, artifact_path = "datasets")

                best_lgbm_model = self.train_lgbm(X_train, Y_train)
                metrics = self.eval_model(best_lgbm_model, X_test, Y_test)
                self.save_model(best_lgbm_model)
                logger.info("Logging model in MLFlow")
                mlflow.log_artifact(self.model_op_path)

                logger.info("Logging param and metrics in MLFLow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)

                logger.info("Model Training Successfully Done!")

        except Exception as e:
            logger.error(f"Error at model training pipeline: {e}")
            raise CustomException("Failed at Model training pipeline", e)
        
if __name__=="__main__":
    model_trainer = ModelTraining(PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH, MODEL_OUTPUT_PATH)
    model_trainer.run()
