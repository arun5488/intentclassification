from src.IntentClassification import logger
from src.IntentClassification import constants as const
from src.IntentClassification.config.configuration import ConfigurationManager
from src.IntentClassification.components.data_preprocessing import DataPreProcessing
from src.IntentClassification.components.data_transformation import DataTransformation
from src.IntentClassification.utils.common import load_object
import re


class PredictionPipeline():
    def __init__(self):
        logger.info("Instantiated Prediction Pipline")
        self.idf_scores = load_object(const.DVC_IDF_SCORES)
        self.tokenizer = load_object(const.DVC_TFIDF_VECTORIZER)
        self.model = load_object(const.DVC_TRAINED_MODEL)
        self.transform_statement = DataTransformation(ConfigurationManager().get_data_transformation_config())
        self.glove_embeddings = load_object(const.GLOVE_EMBEDDINGS)
        self.word2vec_model = load_object(const.WORD2VEC_MODEL)

    def preprocess(self, statement):
        logger.info("Inside prediction pipeline preprocess method")
        try:
            config_manager = ConfigurationManager()
            preprocessing_config = config_manager.get_data_preprocessing_config()
            preprocessing = DataPreProcessing(preprocessing_config)
            logger.info(f"received input:{statement}")
            statement = re.sub(r'\d+\.','',statement)
            statement = preprocessing.step_processing(statement)
            statement = re.sub(r'\bdp\w+','web service',statement)           
            logger.info(f"processed input:{statement}")
            return statement
        except Exception as e:
            logger.error(f"Error in preprocess: {e}")
            raise e
    
    def ensure_2d(self, array):
        return array.reshape(1, -1) if array.ndim == 1 else array
    
    def predict_class(self,statement):
        logger.info("Inside predict method")
        try:
            
            processed_statement = self.preprocess(statement)
            logger.info(f"Processed statement: {processed_statement}")
            vector = self.transform_statement.sentence_to_weighted_vectors(processed_statement, self.glove_embeddings, self.idf_scores, self.word2vec_model)
            logger.info(type(vector))
            logger.info(vector.shape)
           
            predicted = self.model.predict(self.ensure_2d(vector))

            logger.info(f"Predicted class: {predicted}")
            return predicted




        except Exception as e:
            logger.error(f"error occured inside predict method: {e}")
            raise e