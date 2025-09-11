from src.IntentClassification.pipeline.prediction_pipeline import PredictionPipeline
from src.IntentClassification.pipeline.training_pipeline import TrainingPipeline
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
                TrainingPipeline().initiate_training_pipeline()
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