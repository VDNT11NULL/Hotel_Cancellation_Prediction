import os 
import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File is not in {file_path}")
        
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML CONFIG file")
            return config

    except Exception as e:
        logger.error("Error while reading YAML file")
        raise CustomException(f"Failed to read YAML, ", e)

def load_data(csv_path):
    try:
        logger.info(f"Reading csv at {csv_path}")
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        logger.error("Error while laoding csv data")
        raise CustomException(f"Failed loading {csv_path}", e)