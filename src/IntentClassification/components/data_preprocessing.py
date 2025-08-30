from src.IntentClassification.entity import DataPreProcessingConfig
from src.IntentClassification import logger
import pandas as pd
import nltk
import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer
import string
nltk.download("stopwords")
nltk.download("punkt_tab")
nltk.download("wordnet")

class DataPreProcessing:
    def __init__(self, config = DataPreProcessingConfig):
        logger.info("Initialized DataPreProcessing component")
        self.config = config
        logger.info("Loading the validated data file for preprocessing")
        self.validated_data = pd.read_csv(self.config.dataset_file_name)
        logger.info("Loaded validated data for preprocessing")
        self.lemmatizer = WordNetLemmatizer()

    def named_entities(self, sentence):
        logger.info("inside named_entities method")
        named_entities = self.config.named_entities.named_entities
        for param in named_entities:
            if param in sentence:
                sentence = sentence.replace(param, named_entities[param])
        return sentence

    def replace_words(self,sentence):
        logger.info("inside replace_words method")
        replace_words = self.config.named_entities.replace_words
        for param in replace_words:
            if param in sentence:
                sentence = sentence.replace(param, replace_words[param])
                print(sentence)
        return sentence

    def remove_punctuation(self, word):
        logger.info("inside remove_punctuation method")
        regular_punct = string.punctuation
        regular_punct = regular_punct.replace('_','')
        logger.info(f"punctuations to be removed: {regular_punct}")
        for punct in regular_punct:
            word = word.replace(punct, '')
        return word
    
    def remove_numeric_values(self, sentence):
        logger.info("inside remove_numeric_values method")
        return re.sub(r'\d+', '', sentence).strip()
    
    def remove_html_tags(self, sentence):
        logger.info("inside remove_html_tags method")
        return BeautifulSoup(sentence, "html.parser").get_text()

    def lemmatize_words(self, sentence):
        logger.info("inside lemmatize_words method")
        words = word_tokenize(sentence)
        return ' '.join([self.lemmatizer.lemmatize(word) for word in words])
    
    def remove_extra_whitespace(self,sentence):
        logger.info("inside remove_extra_whitespace method")
        return ' '.join(sentence.split())

    def step_processing(self, teststep):
        logger.info("inside step_processing method")
        logger.info("proces the test step by removing punctuation, stop words and lemmatizing the words")
        teststep = teststep.lower()
        teststep = self.remove_html_tags(teststep)
        teststep = self.remove_numeric_values(teststep)
        teststep = self.remove_punctuation(teststep)
        teststep = self.replace_words(teststep)
        teststep = self.named_entities(teststep)
        ts = word_tokenize(teststep)
        stops = set(stopwords.words("english"))
        steps = []
        for word in ts:
            if word not in stops:
                steps.append(word)
        
        return ' '.join(steps)

    def preprocess(self):
        logger.info("Inside preprocess method")
        try:
            dataset = self.validated_data
            logger.info("removing the step numbers like 1., 2., 3.")
            dataset['preprocessed'] = dataset['Steps'].str.replace(r'\d+\.','',regex=True)
            logger.info("applying the step_processing method to preprocess the steps")
            dataset['preprocessed'] = dataset['preprocessed'].apply(lambda x: self.step_processing(x))
            logger.info("replacing the dp... words with web service")
            dataset['preprocessed'] = dataset['preprocessed'].str.replace(r'\bdp\w+','web service',regex=True)            
            logger.info(f"saving the preprocessed data in : {self.config.preprocessed_file_name}")
            dataset.to_csv(self.config.preprocessed_file_name, index=False)
            logger.info("saved the preprocessed data")
        except Exception as e:
            logger.error(f"Error in preprocess: {e}")
            raise e

