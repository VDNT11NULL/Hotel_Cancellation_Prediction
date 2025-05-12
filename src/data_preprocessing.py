import os 
import pandas as pd 
import numpy as np
from utils.common_functions import *
from config.paths_config import *
from src.logger import get_logger
from src.custom_exception import CustomException
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from collections import Counter
from imblearn.over_sampling import SMOTE

logger = get_logger(__name__)

class Data_processor:
    def __init__(self, train_path, test_path, processed_dir, config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        self.config = read_yaml(config_path)

        os.makedirs(processed_dir, exist_ok=True)


    def preprocess_data(self, df):
        try:
            logger.info(f"Preprocessing started")
            cols = df.columns
            if 'Unnamed: 0' in cols:
                df.drop(columns=['Unnamed: 0'], inplace=True)
            if 'Booking_ID' in cols:
                df.drop(columns=['Booking_ID'], inplace=True)
            
            df.drop_duplicates(inplace=True)
            
            tot_cat_cols = self.config['data_processing']['categorical_features'] 
            num_cols = self.config['data_processing']['numerical_features']
            
            LE = LabelEncoder()

            mapping = {}
            logger.info("Label mappings are:")
            for col in tot_cat_cols:
                df[col] = LE.fit_transform(df[col])

                mapping[col] = {label:code for label, code in zip(LE.classes_, LE.fit_transform(LE.classes_))}
                logger.info(f'Mapping[{col}] : {mapping[col]}')

            skew_thresh = self.config['data_processing']['skew_threshold']

            skewness = df.skew()
            for col in df.columns:
                if(skewness[col] > skew_thresh):
                    # Log Transform 
                    df[col] = np.log1p(df[col])

            ## Perform Oversampling (I think i should add a verification stage before this to verify class imbalance)
            ## or is it unharmful , but SMOTE is harmful
            
            class_counter = Counter(df['booking_status'])
            imbalance_thresh = self.config['data_processing']['class_imbalance_threshold']
            logger.info(f"Class Counter: {class_counter}")

            X, Y = df.drop(columns=['booking_status']), df['booking_status']
            majority = max(class_counter.values())
            
            if any(v < majority - imbalance_thresh for v in class_counter.values()):
                print("Imbalance detected. Applying SMOTE...")
                smote = SMOTE(random_state=11)
                logger.info("Done with SMOTE oversampling")
                X_res, y_res = smote.fit_resample(X, Y)
            else:
                print("No significant imbalance. Skipping SMOTE.")
                X_res, y_res = X, Y
                logger.info("No requirement of Oversampling")

            balanced_df = pd.DataFrame(X_res)
            balanced_df['booking_status'] = y_res

            return balanced_df

        except Exception as e:
            logger.error(f"Error while preprocessing {e}")
            raise CustomException(f"Failed at Preprocessing stage", e)

    def select_features(self, df):
        try:
            X = df.drop(columns=["booking_status"])
            Y = df["booking_status"]

            rf = RandomForestClassifier(random_state=11)
            rf.fit(X, Y)

            importance = rf.feature_importances_
            feature_importance_df = pd.DataFrame({
                'Feature' : X.columns,
                'Importance': importance
            }).sort_values(by="Importance", ascending=False)

            num_features_to_select = self.config['data_processing']['num_of_selected_features']

            selected_features = feature_importance_df["Feature"].head(num_features_to_select).values.tolist()

            logger.info(f"Selected features: {selected_features}")

            selected_df = df[selected_features + ["booking_status"]]

            logger.info("Feature selection done!")

            return selected_df

        except Exception as e:
            logger.error(f"Error at feature selection {e}")
            raise CustomException(f"Failed at feature selection stage", e)

    def save_data(self, df, fpath):
        try:
            logger.info("saving prepocessed data : 0")
            df.to_csv(fpath, index=False)
            logger.info(f"Saved data at {fpath} : 1")

        except Exception as e:
            logger.error(f"Error at data saving {e}")
            raise CustomException(f"Failed at data saving stage", e)

    def run_data_process_pipeline(self):
        try:
            logger.info("Loading df from RAW dir")
            
            train_df = pd.read_csv(self.train_path)        
            test_df = pd.read_csv(self.test_path) 

            train_df = self.preprocess_data(train_df)       
            test_df = self.preprocess_data(test_df)       

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_FILE_PATH)
            self.save_data(test_df, PROCESSED_TEST_FILE_PATH)

            logger.info("Data Processing pipeline successfully exec")

        except Exception as e:
            logger.error(f"Error at data processing {e}")
            raise CustomException("Failed at data processing stage", e)

if __name__=="__main__":

    data_processor = Data_processor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    
    data_processor.run_data_process_pipeline()
