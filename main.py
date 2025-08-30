from src.IntentClassification.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.IntentClassification.pipeline.data_validation_pipeline import DataValidationPipeline
from src.IntentClassification.pipeline.data_preprocessing_pipeline import DataPreProcessingPipeline
from src.IntentClassification.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.IntentClassification import logger

# STAGE_NAME = "Data Ingestion Pipeline"

# try:
#     logger.info(f"Starting {STAGE_NAME}")
#     data_ingestion = DataIngestionPipeline()
#     data_ingestion.initiate_data_ingestion()
#     logger.info(f"completed {STAGE_NAME} successfully")
# except Exception as e:
#     logger.error(f"Error occurred in {STAGE_NAME}: {e}")
#     raise e

# STAGE_NAME = "Data Validation Pipeline"

# try:
#     logger.info(f"Starting {STAGE_NAME}")
#     data_validation = DataValidationPipeline()
#     data_validation.initiate_data_validation()
#     logger.info(f"completed {STAGE_NAME} successfully")
# except Exception as e:
#     logger.error(f"Error occurred in {STAGE_NAME}: {e}")
#     raise e

# STAGE_NAME = "Data Preprocessing Pipeline"

# try:
#     logger.info(f"Starting {STAGE_NAME}")
#     data_preprocessing = DataPreProcessingPipeline()
#     data_preprocessing.initiate_data_preprocessing()
#     logger.info(f"completed {STAGE_NAME} successfully")
# except Exception as e:
#     logger.error(f"Error occurred in {STAGE_NAME}: {e}")
#     raise e

STAGE_NAME = "Data Transformation Pipeline"

try:
    logger.info(f"Starting {STAGE_NAME}")
    data_transformation = DataTransformationPipeline()
    data_transformation.initiate_data_transformation()
    logger.info(f"completed {STAGE_NAME} successfully")
except Exception as e:
    logger.error(f"Error occurred in {STAGE_NAME}: {e}")
    raise e

