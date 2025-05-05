import pandas as pd
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
import sys

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
        self.train_path = TRAIN_DATA_PATH
        self.processed_data_path = PROCESSED_DATA_PATH

    def load_data(self):
        try:
            logger.info("Data Processing started")
            df = pd.read_csv(self.train_path)
            logger.info(f"Data read successful | Data shape: {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while loading data")
            raise CustomException("Error while loading data: ", sys)
        
    def clean_data(self, df):
        try:
            logger.info("Data Cleaning started")
            # Example cleaning: drop rows with missing values
            df = df.fillna(0)
            filter = (df.children == 0) & (df.adults == 0) & (df.babies == 0)
            df = df[~filter]
            useless_col = ['days_in_waiting_list', 'arrival_date_year', 'arrival_date_year', 'assigned_room_type', 'booking_changes', 'reservation_status', 'country', 'days_in_waiting_list']

            df = df.drop(useless_col, axis = 1)
            logger.info(f"Data cleaned | Cleaned data shape: {df.shape}")
            return df
        except Exception as e:
            logger.error("Problem while cleaning data")
            raise CustomException("Error while cleaning data: ", sys)
        
    def save_data(self, df):
        try:
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            df.to_csv(self.processed_data_path, index=False)
            logger.info("Processed data saved successfully")
        except Exception as e:
            logger.error("Problem while saving data")
            raise CustomException("Error while saving data: ", sys)
        
    def run(self):
        try:
            logger.info("Starting the pipeline of Data Processing")
            df = self.load_data()
            df = self.clean_data(df)
            self.save_data(df)
            logger.info("Data Processing Pipeline completed successfully")
        except Exception as ce:
            logger.error(f"Error in Data Processing Pipeline: {str(ce)}")
            # raise CustomException("Error in Data Processing Pipeline: ", sys)


if __name__ == "__main__":
    data_processor = DataProcessor()
    data_processor.run()