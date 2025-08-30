from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    dataset_file_name: str
    database_name: str
    collection_name: str
    intents_file_name: str
    intent_column: str

@dataclass
class DataValidationConfig:
    root_dir :Path
    schema: list
    dataset_file_name: str
    validated_file_name: str

@dataclass
class DataPreProcessingConfig:
    root_dir: Path
    dataset_file_name: str
    preprocessed_file_name: str
    named_entities: dict

@dataclass
class DataTransformationConfig:
    root_dir: Path
    glove_url: str
    glove_zip_file: str
    glove_dir: Path
    dataset_file_name: str
    train_file: str
    test_file: str
    train_test_ratio: float
    glove_file: str
    word2vec_model: str