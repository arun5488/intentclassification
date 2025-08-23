from src.IntentClassification.entity import DataValidationConfig
from src.IntentClassification import logger
import pandas as pd
import os

class DataValidation:
    def __init__(self, config: DataValidationConfig):
        logger.info("Initialized DataValidation component")
        self.config = config

    def validate_ingested_data(self):
        logger.info("Inside validate_ingested_data method")
        try:
            loaded_data = pd.read_csv(self.config.dataset_file_name)
            logger.info(f"data loaded from {self.config.dataset_file_name}")
            schema = self.config.schema
            logger.info(f"Schema: {schema}")
            for column in schema:
                if column not in loaded_data.columns:
                    logger.info(f"Column '{column}' is missing from the ingested data.")
            logger.info("Columns are proper in the ingested data")
            if loaded_data.isnull().any(axis=1).sum() > 0:
                logger.info("Missing values found in the ingested data.")
                missing_data = loaded_data.loc[loaded_data.isnull().any(axis=1)]
                # save missing data file 
                missing_data_filepath = os.path.join(self.config.root_dir, "missing_data.csv")
                missing_data.to_csv(missing_data_filepath, index=False)
                logger.info(f"Missing data saved to {missing_data_filepath}")
            else:
                logger.info("No missing values found.")
                logger.info("Saving validated data.")
                validated_data_filepath = self.config.validated_file_name
                loaded_data.to_csv(validated_data_filepath, index=False)
                logger.info(f"Validated data saved to {validated_data_filepath}")

        except Exception as e:
            logger.error(f"Error in validate_ingested_data: {e}")
            raise e