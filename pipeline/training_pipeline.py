from src.data_injestion import *
from src.data_preprocessing import *
from src.model_training import *

if __name__=="__main__":
    #### 1. Data Ingestion
    config = read_yaml(CONFIG_PATH)
    Data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    Data_ingestion.run()

    #### 2. Data  Processing
    data_processor = Data_processor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    data_processor.run_data_process_pipeline()

    #### 3. Model Training
    model_trainer = ModelTraining(PROCESSED_TRAIN_FILE_PATH, PROCESSED_TEST_FILE_PATH, MODEL_OUTPUT_PATH)
    model_trainer.run()
