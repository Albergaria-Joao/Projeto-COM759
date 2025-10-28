from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config.from_object(Config)

load_dotenv("../../.env")

mongo_uri = os.getenv("MONGO_URI")

CORS(app, resources={r'/*': {'origins': '*'}})
mongodb_client = PyMongo(app, 
                         uri=mongo_uri)
db = mongodb_client.db
from app import routes