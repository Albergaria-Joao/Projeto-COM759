from flask import json, request, jsonify, render_template, redirect, session
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId
import os
import bcrypt


@app.route('/')
@app.route('/index')
def index():
    if session.get("nome") == None:
        return redirect("/login")

    return flask.jsonify(json.loads(json_util.dumps(db.usuario.find({}).sort("_id", 1))))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html")


def criar_membro():
    membro = db["membro"]

    password = "joao"
    bytes_password = password.encode('utf-8')  # Convert to bytes
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    print(hashed_password)


    novo_usuario = {
        "nome": "João",
        "login": "joao",
        "email": "joao@gmail.com",
        "senha": hashed_password
    }

    resultado = membro.insert_one(novo_usuario)
    #

@app.route('/create', methods=['GET', 'POST'])
def create():
    #
    
    json_data = request.form.to_dict()
    if request.method == 'GET':
        return render_template("create.html")
    if json_data is not None:
        db.usuario.insert_one(json_data)
        return jsonify(mensagem='usuario criado')
    else:
        return jsonify(mensagem='usuario não criado')
    
@app.route("/getid/<string:userId>")
def getid(userId):
    usuario = db.usuario.find_one({"_id": ObjectId(userId)})
    return flask.jsonify(json.loads(json_util.dumps(usuario)))

@app.route("/delete/<string:userId>")
def delete(userId):
    result = db.usuario.delete_one({"_id": ObjectId(userId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='usuario removido')
    else:
        return jsonify(mensagem='usuario não removido')

@app.route('/update', methods=['POST'])
def update():
    json_data = request.form.to_dict()
    if json_data is not None and db.usuario.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.usuario.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'email': json_data["email"]}})
        return jsonify(mensagem='usuario atualizado')
    else:
        return jsonify(mensagem='usuario não atualizado')