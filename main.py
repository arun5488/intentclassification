from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

if __name__=="__main__":
    MONGO_DB_CLIENT = os.getenv("MONGO_DB_URL")
    print(MONGO_DB_CLIENT)
    # Create a new client and connect to the server
    client = MongoClient(MONGO_DB_CLIENT, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

