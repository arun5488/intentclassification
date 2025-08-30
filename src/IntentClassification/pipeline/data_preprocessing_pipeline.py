from src.IntentClassification.components.data_preprocessing import DataPreProcessing
from src.IntentClassification.config.configuration import ConfigurationManager
from src.IntentClassification import logger

class DataPreProcessingPipeline:
    def __init__(self):
        logger.info("Initialized DataPreProcessingPipeline")

    def initiate_data_preprocessing(self):
        try:
            logger.info("Inside initiate_data_preprocessing pipeline")
            config_manager = ConfigurationManager()
            data_preprocessing_config = config_manager.get_data_preprocessing_config()
            data_preprocessing = DataPreProcessing(data_preprocessing_config)
            data_preprocessing.preprocess()
            logger.info("Completed data preprocessing")
        
        except Exception as e:
            logger.error(f"Error occurred in Data PreProcessing Pipeline: {e}")
            raise e