import os

####################### DATA INGESTION PATH ################

RAW_DIR = "artifacts/raw"
RAW_FILE_PATH = os.path.join(RAW_DIR, "raw.csv")
TRAIN_FILE_PATH = os.path.join(RAW_DIR, "train.csv")
TEST_FILE_PATH = os.path.join(RAW_DIR, "test.csv")

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config', 'config.yaml'))

###################### PROCESSED DATA PATHS ################
PROCESSED_DIR = "artifacts/processed"
PROCESSED_TRAIN_FILE_PATH = os.path.join(PROCESSED_DIR, "processed_train.csv")
PROCESSED_TEST_FILE_PATH = os.path.join(PROCESSED_DIR, "processed_test.csv")


###################### MODEL TRAINING ######################
MODEL_OUTPUT_PATH = "artifacts/models/lgbm_model.pkl"
