from src.IntentClassification.components.data_transformation import DataTransformation
from src.IntentClassification.config.configuration import ConfigurationManager
from src.IntentClassification import logger

class DataTransformationPipeline:
    def __init__(self):
        logger.info("Initialized DataTransformationPipeline")
        

    def initiate_data_transformation(self):
        try:
            config_manager = ConfigurationManager()
            data_transformation_config = config_manager.get_data_transformation_config()
            data_transformation = DataTransformation(data_transformation_config)
            data_transformation.transform_data()
        except Exception as e:
            logger.error(f"Error occurred during data transformation: {e}")
            raise e
