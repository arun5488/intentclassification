## Intent Classification

This project classifies the user entered sentence into a set of predefined intents. The project utilizes Machine Learning algorithms like "Decision Trees" and "Random Forest Classification" to classify the user entered sentence. The intention of the project is to develope an End-End ML Training and Prediction Pipeline in Python, serve these pipelines in UI using Flask and deploy this application in a cloud service.

## Training data: Source, Nature and storage
    Training data is custom dataset of test cases from Retail Banking domain. The dataset consists of around 7500 test steps which were manually categorized into a set of predefined intents. Upon manual classification of the test steps around 100+ unique intents were identified.

    This data is not uniformly distributed, skewed towards a few intents actually. However, no data augmentation/synthetic data creation was tried to balance the data. 

    This data is stored in MongoDB Atlas as a collection. 

## Training Pipeline
    Pipeline consits of following stages - 
    1. Data Ingestion stage:
        Raw data is consumed from MongoDB and stored as a csv file. 
        code present in: src > intentclassification > components > data_ingestion
    2. Data Validation Stage and Data Preprocessing Stage:
        The ingested data is validated for the structural conformity in the data validation stage and then Several data cleaning and preprocessing steps are performed on this raw ingested data.
        code present in: src > intentclassification > components > data_validation / data_prepocessing
    3. Data Transformation Stage:
        The preprocessed data is transformed into 100 dimensional ndarrays to be fed as input to ML algorithms. Embedding for each word in the sentence is generated using the Glove embeddings, for those words which are not present in Glove, embeddings are generated using Word2Vec model. 
        Code handles the downloading of embeddings from the Stanford website, unzipping it and using the downloaded embedding files on data is fully automated. 
        This data is then fed as input to next stage of pipeline
        Code present in: src > intentclassification > components > data_transformation
    4. Model Training Stage: 
        The transformed data is then split into training and test data and then fed to Decision Tree and RandomForest Classification models. The models are evaluated using GridSearchCV and the best model is saved. Accuracy_score is the parameter used to evaluate these models. The scores of the best models of each algorithm is logged in MLFlow for easy reference.
        
        Best model, embeddings, weights and Word2Vec models are stored as Pickle files at the end of this stage to be used in prediction pipeline

        These pickle files are stored in AWS S3 bucket to be used for prediction from AWS EC2 instance.
        Code present in: src > intentclassification > components > model_trainer
    
## Prediction Pipeline: 
    Pipeline utilizes Data Preprocessing and Data Transformation Stages of Training Pipeline to process the user inputs and then does the prediction by calling the best model.

## UI 
    Simple UI was created using Flask to trigger the Training and Prediction pipelines. 

## Deployment in AWS EC2 instance

    A Docker image is created which is then deployed into AWS EC2 instance using Github actions. This deployment was successfully done. Both the pipelines were tested in the EC2 instance and found to be working fine.

# Project Structure

```
.env
.env.template
.flaskenv
.gitignore
app.py
Dockerfile
main.py
params.yaml
README.md
requirements.txt
research.ipynb
schema.yaml
setup.py
.dvc/
    .gitignore
    config
.github/
    workflows/
artifacts/
    data_ingestion/
    data_preprocessing/
    data_transformation/
    data_validation/
    model_trainer/
config/
    config.yaml
data/
    .gitignore
    glove_embeddings.pkl
    glove_embeddings.pkl.dvc
    idf_scores.pkl
    idf_scores.pkl.dvc
    tfidf_vectorizer.pkl
    tfidf_vectorizer.pkl.dvc
    ...
logs/
src/
    IntentClassification/
        components/
        config/
        constants/
        entity/
        pipeline/
        utils/
static/
    css/
    js/
    vendor/
templates/
    index.html
    predict.html
    train_success.html
```



    