from src.IntentClassification.pipeline.prediction_pipeline import PredictionPipeline
from src.IntentClassification.pipeline.data_ingestion_pipeline import DataIngestionPipeline
from src.IntentClassification.pipeline.data_validation_pipeline import DataValidationPipeline
from src.IntentClassification.pipeline.data_preprocessing_pipeline import DataPreProcessingPipeline
from src.IntentClassification.pipeline.data_transformation_pipeline import DataTransformationPipeline
from src.IntentClassification.pipeline.model_trainer_pipeline import ModelTrainerPipeline
from src.IntentClassification import logger
from flask import Flask, render_template, url_for, request
from dotenv import load_dotenv
from src.IntentClassification import constants as const
import os
import subprocess
app = Flask(__name__)

@app.route('/')
def index(): 
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error occured in index method:{e}")
        raise e

@app.route('/handle-action', methods=['POST'])
def handle_action(): 
    try:
        if request.method == 'POST':
            if request.form.get('action') == 'train':
                logger.info("Inside trainining of method POST")
                logger.info("Data Ingestion Stage from app.py")
                DataIngestionPipeline().initiate_data_ingestion()
                logger.info("Data Validation Stage from app.py")
                DataValidationPipeline().initiate_data_validation()
                logger.info("Data Preprocessing Stage from app.py")
                DataPreProcessingPipeline().initiate_data_preprocessing()
                logger.info("Data Transformation Stage from app.py")
                DataTransformationPipeline().initiate_data_transformation()
                logger.info("Model Trainer stage from app.py")
                ModelTrainerPipeline().initiate_model_trainer_pipeline()
                return render_template('train_success.html')
            elif request.form.get('action') == 'predict':
                logger.info("loading page to capture sentence for prediction")
                return render_template('predict.html')
        else:
            return render_template('index.html')
    except Exception as e:
        logger.error(f"Error occured in index method:{e}")
        raise e

@app.route('/predict', methods=['GET','POST'])
def predict_class():
    logger.info("Inside predict_class method in app.py")
    logger.info({request.method})
    try:
        if request.method == 'POST':
            logger.info("Inside POST method")
            pred = PredictionPipeline()
            sentence = request.form.get('sentence')
            logger.info(f"sentence received as input:{sentence}")
            predictedvalue = (pred.predict_class(sentence))[0]
            return render_template('predict.html', sentence = sentence, predictedvalue = predictedvalue)
        else:
            logger.info("Inside GET method of predict_class")
            return render_template('predict.html', sentence = None, predictedvalue = None)
    except Exception as e:
        logger.error(f"Error occured in predict_class: {e}")
        raise e

if __name__ == '__main__':
    load_dotenv(dotenv_path=const.FLASK_ENV)
    host = os.getenv('FLASK_RUN_HOST')
    logger.info(f"Host:{host}")
    port = os.getenv('FLASK_RUN_PORT')
    logger.info(f"Port:{port}")
    app.run(host=host, port=port, debug=True)