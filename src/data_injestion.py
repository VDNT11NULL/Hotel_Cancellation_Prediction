import os
import pandas as pd
from sklearn.model_selection import train_test_split
from google.cloud import storage
from src.custom_exception import CustomException
from src.logger import get_logger
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_test_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
        
        logger.info(f"Data Ingestion started with {self.bucket_name} on {self.file_name}")

    def download_csv_from_GCP(self):
        try:
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            with open(RAW_FILE_PATH, 'wb') as f:
                blob.download_to_file(f)

            logger.info(f"Raw file successfully downloaded to {RAW_FILE_PATH}")

        except Exception as e:
            logger.error(f"Error while downloading csv file")
            raise CustomException("Failed to download csv", e)
        
    def split_data(self):
        try:
            logger.info("Starting the spliting process")
            data = pd.read_csv(RAW_FILE_PATH)

            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=11)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"Train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"Test data saved to {TEST_FILE_PATH}")
        
        except Exception as e:
            logger.error(f"Error while spliting data")
            raise CustomException("Failed to split data into train-test", e)
        
    def run(self):
        try:
            logger.info(f"Starting data ingestion process")

            self.download_csv_from_GCP()
            self.split_data()

            logger.info("Data Ingestion successfull")

        except CustomException as ce:
            logger.error(f"Custom Exception :{str(ce)}")

        finally:
            logger.info("Data Ingestion completed")

if __name__=="__main__":
    config = read_yaml(CONFIG_PATH)
    print("Loaded config:", config)  # Debug line
    Data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    Data_ingestion.run()
