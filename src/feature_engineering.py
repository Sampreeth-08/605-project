import os
import sys
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_selection import mutual_info_classif
from config.paths_config import PROCESSED_DATA_PATH, ENGINEERED_DATA_PATH, ENGINEERED_DIR
from src.logger import get_logger
from src.custom_exception import CustomException
from utils.helpers import label_encode

logger = get_logger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.data_path = PROCESSED_DATA_PATH
        self.df = None
        self.label_mappings = {}

    def load_data(self):
        try:
            logger.info("Loading processed data")
            self.df = pd.read_csv(self.data_path)
            logger.info(f"Data loaded successfully with shape: {self.df.shape}")
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise CustomException("Error loading data", sys)

    def feature_construction(self):
        try:
            logger.info("Starting feature construction")
            self.df['total_guests'] = self.df['adults'] + self.df['children'] + self.df['babies']
            logger.info("Feature construction completed")
        except Exception as e:
            logger.error(f"Error during feature construction: {e}")
            raise CustomException("Error during feature construction", sys)

    def handle_reservation_status_date(self):
        try:
            logger.info("Handling 'reservation_status_date' feature")
            self.df['reservation_status_date'] = pd.to_datetime(self.df['reservation_status_date'])

            self.df['year'] = self.df['reservation_status_date'].dt.year
            self.df['month'] = self.df['reservation_status_date'].dt.month
            self.df['day'] = self.df['reservation_status_date'].dt.day

            self.df = self.df.drop(columns=['reservation_status_date', 'arrival_date_month'])
            logger.info("Successfully processed 'reservation_status_date' feature")
        except Exception as e:
            logger.error(f"Error during 'reservation_status_date' processing: {e}")
            raise CustomException("Error during 'reservation_status_date' processing", sys)

    def encode_categorical_features(self):
        try:
            logger.info("Encoding categorical features using helper function")
            categorical_cols = ['hotel','meal', 'market_segment', 'distribution_channel', 'reserved_room_type', 'deposit_type', 'customer_type']
            if categorical_cols:
                self.df, self.label_mappings = label_encode(self.df, categorical_cols)
                logger.info(f"Categorical features encoded successfully: {categorical_cols}")
            else:
                logger.info("No categorical features to encode")
        except Exception as e:
            logger.error(f"Error encoding categorical features: {e}")
            raise CustomException("Error encoding categorical features", sys)

    def feature_selection(self):
        try:
            logger.info("Computing mutual information scores for all features")
            X = self.df.drop(columns='is_canceled')
            y = self.df['is_canceled']

            discrete_features = X.dtypes == int

            mutual_info = mutual_info_classif(X, y, discrete_features=discrete_features)

            mutual_info_df = pd.DataFrame({
                'Feature': X.columns,
                'Mutual Information': mutual_info
            }).sort_values(by='Mutual Information', ascending=False)

            logger.info(f"Mutual information scores:\n{mutual_info_df}")
        except Exception as e:
            logger.error(f"Error during feature selection: {e}")
            raise CustomException("Error during feature selection", sys)

    def save_data(self):
        try:
            logger.info("Saving engineered data")
            os.makedirs(ENGINEERED_DIR, exist_ok=True)
            self.df.to_csv(ENGINEERED_DATA_PATH, index=False)
            logger.info(f"Engineered data saved at {ENGINEERED_DATA_PATH}")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise CustomException("Error saving data", sys)

    def run(self):
        try:
            logger.info("Starting feature engineering pipeline")
            self.load_data()
            self.feature_construction()
            self.handle_reservation_status_date()
            self.encode_categorical_features()
            self.feature_selection()
            self.save_data()
            logger.info("Feature engineering pipeline completed successfully")
        except CustomException as ce:
            logger.error(f"Feature engineering pipeline failed: {ce}")
        finally:
            logger.info("End of feature engineering pipeline")

if __name__ == "__main__":
    engineer = FeatureEngineer()
    engineer.run()
