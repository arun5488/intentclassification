from src.IntentClassification.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.IntentClassification.pipeline.data_validation_pipeline import DataValidationPipeline
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

STAGE_NAME = "Data Validation Pipeline"

try:
    logger.info(f"Starting {STAGE_NAME}")
    data_validation = DataValidationPipeline()
    data_validation.initiate_data_validation()
    logger.info(f"completed {STAGE_NAME} successfully")
except Exception as e:
    logger.error(f"Error occurred in {STAGE_NAME}: {e}")
    raise e