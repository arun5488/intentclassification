from src.IntentClassification.entity import (DataIngestionConfig, DataValidationConfig)
from src.IntentClassification import logger
from src.IntentClassification import constants as const
from src.IntentClassification.utils.common import *

class ConfigurationManager:
    def __init__(self, config_file_path= const.CONFIG_FILE_PATH,
                 param_file_path= const.PARAMS_FILE_PATH,
                 schema_file_path = const.SCHEMA_FILE_PATH):
        logger.info("Created Instance of ConfigurationManager")
        self.config = read_yaml(config_file_path)
        logger.info(f"Loaded config: {self.config}")
        self.params = read_yaml(param_file_path)
        logger.info(f"Loaded params: {self.params}")
        self.schema = read_yaml(schema_file_path)
        logger.info(f"Loaded schema: {self.schema}")

        create_directories([self.config.artifacts_root])
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        logger.info("Obtaining Data Ingestion Config")
        config = self.config.data_ingestion
        create_directories([Path(config.root_dir)])

        return DataIngestionConfig(
            root_dir = Path(config.root_dir),
            dataset_file_name = config.dataset_file_name,
            database_name = config.database_name,
            collection_name = config.collection_name,
            intents_file_name = config.intents_file_name,
            intent_column = config.intent_column
        )

    def get_data_validation_config(self) -> DataValidationConfig:
        logger.info("Obtaining Data Validation Config")
        config = self.config.data_validation
        schema = self.schema.columns
        logger.info(f"Schema: {schema}")
        create_directories([Path(config.root_dir)])

        return DataValidationConfig(
            root_dir = Path(config.root_dir),
            schema = schema,
            dataset_file_name = config.dataset_file_name,
            validated_file_name = config.validated_file_name
        )