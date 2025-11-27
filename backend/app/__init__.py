from config import Config
from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS 
from dotenv import load_dotenv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent 
template_dir = BASE_DIR / "templates"

app = Flask(__name__, template_folder=str(template_dir))
app.config.from_object(Config)

app.secret_key = "minha_chave_secreta_fixa_para_teste"


load_dotenv("../../.env")

mongo_uri = os.getenv("MONGO_URI")

app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False 

CORS(app, resources={r"/*": {"origins": ["http://localhost:8081", "http://127.0.0.1:8081"]}}, supports_credentials=True)

mongodb_client = PyMongo(app, uri=mongo_uri)
db = mongodb_client.db

from app import routes