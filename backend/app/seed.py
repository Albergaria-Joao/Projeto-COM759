from flask_pymongo import PyMongo
import os
import bcrypt
from bson.objectid import ObjectId
from app import app

mongo_uri = os.getenv("MONGO_URI")

mongodb_client = PyMongo(uri=mongo_uri)
db = mongodb_client.db

membro = db["membro"]

if db.membro.find_one({"login": "teste"}) is not None:
    db.membro.delete({"login": "teste"})

salt = bcrypt.gensalt()
def hashing(password, salt):
    bytes_password = password.encode('utf-8')  # Convert to bytes
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    return hashed_password

senha = "teste"
hashed = hashing(senha, salt)

membro_dados = {
    "login": "teste",
    "nome": "teste",
    "email": "teste@mail.com",
    "senha": hashed,
    "equipe_id": ObjectId(""),
    "auth": "admin"
}


membro.insert_one(membro_dados)