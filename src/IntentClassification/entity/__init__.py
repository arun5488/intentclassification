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