from src.IntentClassification.entity import ModelTrainerConfig
from src.IntentClassification import logger
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
import pandas as pd
import pickle
import os
import numpy as np
import mlflow, dagshub, tempfile
from dotenv import load_dotenv
from src.IntentClassification import constants as const
from src.IntentClassification.utils.common import create_directories, save_object, load_object
from pathlib import Path

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        logger.info("Initialized ModelTrainer component")
        self.config = config
        self.train_data = pd.read_csv(self.config.train_file)
        self.test_data = pd.read_csv(self.config.test_file)
        
    def convert_to_ndarray(self, X):
        try:
            logger.info("Inside convert_to_ndarray")
            X['vectors'] = X['vectors'].apply(lambda x: x.strip('[]').replace("\n",""))
            X['vectors'] = X['vectors'].apply(lambda x: np.fromstring(x, sep= ' '))
            return np.stack(X['vectors'].values)
        except Exception as e:
            logger.error(f"error occured: {e}")
            raise e

    def track_mlflow(self, gs: GridSearchCV):

        try:
            logger.info("Inside track_mlflow method")
            load_dotenv()
            dagshub.init(repo_owner='bsaarun54', repo_name='IntentClassification', mlflow=True)
            mlflow.set_tracking_uri(os.environ['MLFLOW_TRACKING_URI'])
            mlflow.set_experiment("intent_classification_experiments")
            with mlflow.start_run():
                best_model = type(gs.best_estimator_).__name__
                best_param = gs.best_params_
                best_score = gs.best_score_
                
                mlflow.log_param("Best model:", best_model)
                mlflow.log_params(best_param)
                mlflow.log_metric("best score:", best_score)
               # mlflow.sklearn.log_model(best_model, artifact_path="models")

                cv_df = pd.DataFrame(gs.cv_results_)
                temp_dir = tempfile.mkdtemp()
                cv_path = os.path.join(temp_dir, "cv_results.csv")
                cv_df.to_csv(cv_path, index=False)
                mlflow.log_artifact(cv_path, artifact_path="cv_results")

        except Exception as e:
            logger.error(f"Error occured inside track_mlflow:{e}")
            raise e


    def evaluate_model(self, X_train, y_train, X_test, y_test, models: dict, params: dict) -> dict:
        try:
            logger.info("Inside evaluate_model method")
            logger.info(f"len of models: {len(list(models))}")
            report = {}
            for i in range(len(list(models))):
                model = list(models.values())[i]
                logger.info(f"model: {type(model)}")
                param = list(params.values())[i]
                logger.info(f"param: {param}")

                gs = GridSearchCV(model, param, cv=3)
                gs.fit(X_train, y_train)

                best_params = gs.best_params_
                logger.info(f"Best parameters for {model}: {best_params}")
                model.set_params(**best_params)
                model.fit(X_train, y_train)

                y_pred = model.predict(X_test)

                test_model_score = accuracy_score(y_test, y_pred)
                #MLFLOW tracking
                self.track_mlflow(gs)

                report[list(models.keys())[i]] = [test_model_score, best_params]

            return report

        except Exception as e:
            logger.error(f"Error in evaluate_model: {e}")
            raise e

    def train_model(self, X_train, X_test, y_train, y_test):
        logger.info("Inside train_model method")
        try:
            models = {
                "random_forest": RandomForestClassifier(verbose=1)
                ,
                "decision_tree": DecisionTreeClassifier()
            }
            params = {
                "random_forest": self.config.rf_params
                ,
                "decision_tree": self.config.decision_tree_parameters
            }
            logger.info(f"models being sent to evaluate_model: {models}")
            logger.info(f"params being sent to evaluate_method: {params}")
            model_report: dict=self.evaluate_model(X_train,y_train, X_test, y_test, models= models, params = params)
            logger.info(f" model_report: {model_report}")
            best_model_score = max(sorted(model_report.values()))
            logger.info(f"Best model score: {best_model_score}")

            # getting best model name
            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            logger.info(f"Best model name: {best_model_name}")

            best_model_params = model_report.get(best_model_name)[1]
            logger.info(f"Best model params: {best_model_params}")

            best_model = models[best_model_name]
            best_model.set_params(**best_model_params)
            best_model.fit(X_train, y_train)

            
            y_pred = best_model.predict(X_test)
            best_model_score = accuracy_score(y_test, y_pred)
            logger.info(f"Test model score: {best_model_score}")
            
            # # ML Flow tracking 
            # self.track_mlflow(best_model, best_model_score)

            # save the model
            with open(self.config.trained_model_file, 'wb') as f:
                pickle.dump(best_model, f)
            logger.info(f"model saved at: {self.config.trained_model_file}")

            save_object(const.DVC_TRAINED_MODEL, best_model)
            

        except Exception as e:
            logger.error(f"Error in train_model: {e}")
            raise e

    def initiate_model_trainer(self):
        try:
            logger.info("Inside initiate_model_trainer method")
            X_train = self.convert_to_ndarray(self.train_data.drop(columns=['predicted']))
            y_train = self.train_data['predicted']
            X_test = self.convert_to_ndarray((self.test_data.drop(columns=['predicted'])))
            y_test = self.test_data['predicted']

            logger.info("Creating data folder for dvc")
            create_directories([Path(const.DVC_FOLDER)])
            logger.info("saving X files for dvc")
            np.save(const.DVC_X_TRAIN, X_train)
            np.save(const.DVC_X_TEST, X_test)
            logger.info("saving y files")
            y_train.to_csv(const.DVC_Y_TRAIN, index=False)
            y_test.to_csv(const.DVC_Y_TEST, index=False)

            idf_scores = load_object('artifacts/data_transformation/idf_scores.pkl')
            save_object(const.DVC_IDF_SCORES, idf_scores)
            tfidf = load_object('artifacts/data_transformation/tfidf_vectorizer.pkl')
            save_object(const.DVC_TFIDF_VECTORIZER, tfidf)

            self.train_model(X_train, X_test, y_train, y_test)
            
        except Exception as e:
            logger.error(f"error occured inside initiate_model_trainer:{e}")
            raise e
