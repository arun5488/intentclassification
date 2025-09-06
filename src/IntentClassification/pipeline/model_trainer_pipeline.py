from src.IntentClassification.components.model_trainer import ModelTrainer
from src.IntentClassification import logger
from src.IntentClassification.config.configuration import ConfigurationManager

class ModelTrainerPipeline:
    def __init__(self):
        logger.info("Initiated Model Trainer pipeline")
    
    def initiate_model_trainer_pipeline(self):
        logger.info("Inside initiate_model_trainer_pipeline method")
        config_manager = ConfigurationManager()
        model_trainer_config = config_manager.get_model_trainer_config()
        model_trainer = ModelTrainer(model_trainer_config)
        model_trainer.initiate_model_trainer()
        logger.info("model training completed")
