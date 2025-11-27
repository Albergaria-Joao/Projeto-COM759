from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent  # vai para 'backend'
template_dir = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(template_dir))
app.config.from_object(Config)

load_dotenv("../../.env")

mongo_uri = os.getenv("MONGO_URI")

# CORS(app, supports_credentials=True)
app.config["SESSION_COOKIE_SAMESITE"] = "None"
app.config["SESSION_COOKIE_SECURE"] = False  # true se usar HTTPS

CORS(app, resources={r"/*": {"origins": ["http://localhost:8081"]}}, supports_credentials=True, allow_headers="*")

mongodb_client = PyMongo(app, 
                         uri=mongo_uri)
db = mongodb_client.db

from app import routes