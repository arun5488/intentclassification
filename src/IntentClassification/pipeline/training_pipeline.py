from src.IntentClassification.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.IntentClassification.pipeline.data_validation_pipeline import DataValidationPipeline
from src.IntentClassification.pipeline.data_preprocessing_pipeline import DataPreProcessingPipeline
from src.IntentClassification.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.IntentClassification.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.IntentClassification import logger
from src.IntentClassification import constants as const
from src.IntentClassification.cloud.s3_syncer import S3Sync
from src.IntentClassification.utils.common import read_yaml
import os

class TrainingPipeline:
    def __init__(self):
        logger.info("Instantiating TrainingPipeline Object")
        self.config = read_yaml(const.CONFIG_FILE_PATH)
        self.s3_sync = S3Sync()

        ## local artifact is going to s3 bucket    
    def sync_artifact_dir_to_s3(self):
        try:
            logger.info("inside sync_artifact_dir_to_s3 method")
            logger.info(f"TRAINING_BUCKET_NAME: {const.TRAINING_BUCKET_NAME}")
            logger.info(f"artifacts root: {self.config.artifacts_root}")
            aws_bucket_url = f"s3://{const.TRAINING_BUCKET_NAME}/artifact/{self.config.artifacts_root}"
            self.s3_sync.sync_folder_to_s3(folder = self.config.artifacts_root,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logger.error(f"error inside sync_artifact_dir_to_s3:{e}")
            raise e
        
    ## local final model is going to s3 bucket 
        
    def sync_saved_model_dir_to_s3(self):
        try:
            logger.info("Inside sync_saved_model_dir_to_s3 method")
            logger.info(f"TRAINING_BUCKET_NAME: {const.TRAINING_BUCKET_NAME}")
            logger.info(f"data folder:{const.DVC_FOLDER}")
            aws_bucket_url = f"s3://{const.TRAINING_BUCKET_NAME}/final_model/{const.DVC_FOLDER}"
            self.s3_sync.sync_folder_to_s3(folder = const.DVC_FOLDER,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logger.error(f"error inside sync_artifact_dir_to_s3:{e}")
            raise e
    def sync_s3_to_data_folder(self):
        try:
            logger.info("Inside sync_s3_to_data_folder method")
            logger.info(f"TRAINING_BUCKET_NAME: {const.TRAINING_BUCKET_NAME}")
            logger.info(f"data folder:{const.DVC_FOLDER}")
            aws_bucket_url = f"s3://{const.TRAINING_BUCKET_NAME}/final_model/{const.DVC_FOLDER}"
            self.s3_sync.sync_folder_from_s3(folder = const.DVC_FOLDER,aws_bucket_url=aws_bucket_url)
        except Exception as e:
            logger.error(f"error inside sync_s3_to_folder:{e}")
            raise e
    
    def sync_s3_to_artifacts_folder(self):
        try:
            logger.info("Inside sync_s3_to_folder method")
            logger.info(f"TRAINING_BUCKET_NAME: {const.TRAINING_BUCKET_NAME}")
            logger.info(f"artifacts_root:{self.config.artifacts_root}")
            aws_bucket_url = f"s3://{const.TRAINING_BUCKET_NAME}/artifact/{self.config.artifacts_root}"
            self.s3_sync.sync_folder_from_s3(folder = self.config.artifacts_root,aws_bucket_url=aws_bucket_url)
            logger.info(f"synced from s3 to local artifacts folder")
        except Exception as e:
            logger.error(f"error inside sync_s3_to_folder:{e}")
            raise e

    def initiate_training_pipeline(self):
        logger.info("Inside initiate_training_pipeline method")
        if not os.path.exists(self.config.artifacts_root):
            logger.info(f"artifacts_root doesnt folder exists, syncing from s3 to local: {self.config.artifacts_root}")
            self.sync_s3_to_artifacts_folder()
        else:
            logger.info(f"artifacts_root_folder doesnt exist, everything will be created from scratch")
        # logger.info("Data Ingestion Stage ")
        # DataIngestionPipeline().initiate_data_ingestion()
        # logger.info("Data Validation Stage ")
        # DataValidationPipeline().initiate_data_validation()
        # logger.info("Data Preprocessing Stage ")
        # DataPreProcessingPipeline().initiate_data_preprocessing()
        # logger.info("Data Transformation Stage ")
        # DataTransformationPipeline().initiate_data_transformation()
        logger.info("Model Trainer stage ")
        ModelTrainerPipeline().initiate_model_trainer_pipeline()

        logger.info(f"Syncing local artifacts to s3 bucket")
        self.sync_artifact_dir_to_s3()
        self.sync_saved_model_dir_to_s3()