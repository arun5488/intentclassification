from src.IntentClassification.entity import DataTransformationConfig
from src.IntentClassification import logger
from src.IntentClassification import constants as const
from src.IntentClassification.utils.common import save_object
import requests
from zipfile import ZipFile
from sklearn.model_selection import train_test_split
import os
from pathlib import Path
from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import numpy as np
from nltk.tokenize import word_tokenize
import pickle


class DataTransformation: 
    def __init__(self, config = DataTransformationConfig):
        logger.info("Initialized DataTransformation component")
        self.config = config
        self.tfidf_vectorizer = TfidfVectorizer()
        self.df = pd.read_csv(self.config.dataset_file_name)
        self.corpus = self.df['preprocessed'].astype(str).tolist()

        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.corpus)
        self.idf_scores = dict(zip(self.tfidf_vectorizer.get_feature_names_out(),self.tfidf_vectorizer.idf_))
        # word to vec model
        self.tokenize_corpus = [word_tokenize(text) for text in self.corpus]
        self.word2vec_model = Word2Vec(sentences=self.tokenize_corpus, vector_size=100, window=5, min_count=1, workers=4)

    
    def download_glove_embeddings(self):
        logger.info("Inside download_glove_embeddings method")
        url = self.config.glove_url
        logger.info(f"Downloading glove embeddings from {url}")
        glove_folder = self.config.glove_dir
        logger.info(f"Glove folder: {glove_folder}")
        glove_zip_file = self.config.glove_zip_file
        logger.info(f"Glove zip file: {glove_zip_file}")

        if not os.path.exists(glove_folder):
            os.makedirs(glove_folder, exist_ok=True)
            response = requests.get(url, stream=True)
            with open(glove_zip_file, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            logger.info(f"Downloaded glove embeddings from {url}")
            with ZipFile(glove_zip_file, 'r') as zip:
                zip.extractall(glove_folder)
            logger.info(f"Unzipped glove embeddings to {glove_folder}")
        else:
            logger.info(f"Glove embeddings already exist in {glove_folder}")

    def load_glove_embeddings(self):
        logger.info("Inside load_glove_embeddings method")
        file_path = self.config.glove_file
        embeddings = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                word = parts[0]
                vector = np.array(parts[1:], dtype=np.float32)
                embeddings[word] = vector
        logger.info(f"Loaded {len(embeddings)} word vectors.")
        return embeddings
        
    def tokenize_corpus(self):
        logger.info("Inside tokenize_corpus method")
        return [word_tokenize(text) for text in self.corpus]
    


    def load_word2vec_model(self):
        logger.info("Inside load_word2vec_model method")
        return Word2Vec.load(self.config.word2vec_model)

    def save_transform_artifacts(self):
        logger.info("Inside save_transform_artifacts method")
        #save td-idf vectorizer
        with open(self.config.tfidf_vectorizer_path, 'wb') as f:
            pickle.dump(self.tfidf_vectorizer, f)
        #save idf_scores
        with open(self.config.idf_scores_path, 'wb') as f:
            pickle.dump(self.idf_scores, f)
        #save word2vec model
        self.word2vec_model.save(self.config.word2vec_model)

    

    def sentence_to_weighted_vectors(self, sentence, glove_embeddings, idf_scores, word2vec_model):
        logger.info("Inside sentence_to_weighted_vectors method")
        words = word_tokenize(sentence)
        vector = np.zeros(100)  # Assuming 100-dimensional GloVe embeddings
        total_weight = 0

        word_2_vec = word2vec_model

        for word in words:
            
            if word in glove_embeddings and word in idf_scores:
                weight = (idf_scores[word])
                vector += glove_embeddings[word]*weight
                total_weight += weight
            else:
                vector += word_2_vec.wv[word]
        return vector / total_weight if total_weight != 0 else vector
    
    def transform_data(self):
        logger.info("Inside transform_data method")
        self.download_glove_embeddings()
        embeddings = self.load_glove_embeddings()
        word2vec_model = self.word2vec_model
        vectors = []
        logger.info(f"transforming {len(self.corpus)} sentences into vectors.")
        for sentence in self.corpus:
            vector = self.sentence_to_weighted_vectors(sentence, embeddings, self.idf_scores, word2vec_model)
            
            vectors.append(vector)
        logger.info(f"Transformed {len(vectors)} sentences into vectors.")
        logger.info("Adding vectors as a column to the dataframe.")
        self.df['vectors'] = vectors
        logger.info("Added vectors as a column to the dataframe.")
        df_transformed_data = self.df[['vectors', 'predicted']]
        train_df, test_df = train_test_split(df_transformed_data, test_size=1 - self.config.train_test_ratio, random_state=42)
        logger.info(f"Train shape: {train_df.shape}, Test shape: {test_df.shape}")
        logger.info("saving the train_df and test_df")
        train_df.to_csv(self.config.train_file, index=False)
        logger.info(f"Saved train_df to {self.config.train_file}")
        test_df.to_csv(self.config.test_file, index=False)
        logger.info(f"Saved test_df to {self.config.test_file}")
        self.save_transform_artifacts()
        logger.info("Saved all transformation artifacts.")

        #save glove_embeddings
        save_object(const.GLOVE_EMBEDDINGS, embeddings)