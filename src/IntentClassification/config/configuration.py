from src.IntentClassification.entity import (DataIngestionConfig, DataValidationConfig, DataPreProcessingConfig, DataTransformationConfig, ModelTrainerConfig)
from src.IntentClassification import logger
from src.IntentClassification import constants as const
from src.IntentClassification.utils.common import *

class ConfigurationManager:
    def __init__(self, config_file_path= const.CONFIG_FILE_PATH,
                 param_file_path= const.PARAMS_FILE_PATH,
                 schema_file_path = const.SCHEMA_FILE_PATH):
        logger.info("Created Instance of ConfigurationManager")
        self.config = read_yaml(config_file_path)
        self.params = read_yaml(param_file_path)
        self.schema = read_yaml(schema_file_path)

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
    
    def get_data_preprocessing_config(self) -> DataPreProcessingConfig:
        logger.info("Obtaining Data Preprocessing Config")
        config = self.config.data_preprocessing
        named_entities = self.params
        logger.info(f"Named entities: {named_entities}")

        create_directories([Path(config.root_dir)])
        return DataPreProcessingConfig(
            root_dir = Path(config.root_dir),
            dataset_file_name = config.dataset_file_name,
            preprocessed_file_name = config.preprocessed_file_name,
            named_entities = named_entities
        )
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        logger.info("Obtaining Data Transformation Config")
        config = self.config.data_transformation
        create_directories([Path(config.root_dir)])
        create_directories([Path(const.DVC_FOLDER)])

        return DataTransformationConfig(
            root_dir = Path(config.root_dir),
            glove_url = config.glove_url,
            glove_zip_file = config.glove_zip_file,
            glove_dir = Path(config.glove_dir),
            dataset_file_name = config.dataset_file_name,
            train_file = config.train_file,
            test_file = config.test_file,
            train_test_ratio = config.train_test_ratio,
            glove_file = config.glove_file,
            word2vec_model = config.word2vec_model,
            tfidf_vectorizer_path = config.tfidf_vectorizer_path,
            idf_scores_path = config.idf_scores_path,
            trained_word2vec_model_path = config.trained_word2vec_model_path
        )
    
    def get_model_trainer_config(self) -> ModelTrainerConfig:
        logger.info("Obtaining Model Trainer Config")
        config = self.config.model_trainer
        params = self.params

        create_directories([Path(config.root_dir)])

        return ModelTrainerConfig(
            root_dir = Path(config.root_dir),
            trained_model_file = config.trained_model_file,
            word2vec_model = config.word2vec_model,
            tfidf_vectorizer_path = config.tfidf_vectorizer_path,
            idf_scores_path = config.idf_scores_path,
            train_file = config.train_file,
            test_file = config.test_file,
            model_accuracy_baseline = config.model_accuracy_baseline,
            decision_tree_parameters = params.decision_tree,
            rf_params = params.random_forest
        )