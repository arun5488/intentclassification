LOCAL_DATASET_PATH = "local_data/dataset.csv"
MONGO_DB_DATABASE = "intent_classification"
MONGO_DB_COLLECTION = "intents"

# yaml file names
SCHEMA_FILE_PATH = "schema.yaml"
CONFIG_FILE_PATH = "config/config.yaml"
PARAMS_FILE_PATH = "params.yaml"


# feature store and artificats  for dvc
DVC_FOLDER = "data"
DVC_X_TRAIN = "data/X_train.npy"
DVC_X_TEST = "data/X_test.npy"
DVC_Y_TRAIN = "data/y_train.csv"
DVC_Y_TEST = "data/y_test.csv"
DVC_IDF_SCORES = "data/idf_scores.pkl"
DVC_TFIDF_VECTORIZER = "data/tfidf_vectorizer.pkl"
DVC_TRAINED_MODEL = "data/trained_model.pkl"
WORD2VEC_MODEL = "artifacts/data_transformation/word2vec.model"
GLOVE_EMBEDDINGS = "data/glove_embeddings.pkl"

#.env filepath
FLASK_ENV = '.flaskenv'
ENV = '.env'