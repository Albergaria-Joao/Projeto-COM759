from flask import json, request, jsonify, render_template, redirect, session
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId
import os
import bcrypt

salt = bcrypt.gensalt()
def hashing(password, salt):
    bytes_password = password.encode('utf-8')  # Convert to bytes
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    print(hashed_password)
    return hashed_password

@app.route('/')
@app.route('/index')
def index():
    if session.get("nome") == None:
        return redirect("/login")
    return render_template("dashboard.html", usuarios=db.membro.find().sort("_id", 1))
    #return flask.jsonify(json.loads(json_util.dumps(db.usuario.find({}).sort("_id", 1))))




@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template("login.html")
    
    json_data = request.form.to_dict()
    user = db.membro.find_one({"login": json_data["login"]})
    print(user["senha"])
    if (hashing(json_data["senha"], user["senha"]) == user["senha"]):
        session["nome"] = user["nome"]
        return redirect("/index")
    else:
        return redirect("/erro")
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop("nome", None)
    return jsonify(mensagem='logout realizado')

    
# @app.route('/erro', methods=['GET', 'POST'])
# def login():
#     print("ERRO")
#     return render_template("erro.html")




def criar_membro(dados):
    membro = db["membro"]

    password = dados["senha"]
    hashed_password = hashing(password, salt)
    dados["senha"] = hashed_password

    resultado = membro.insert_one(dados)
    #

@app.route('/create-membro', methods=['GET', 'POST'])
def create():
    #
    
    json_data = request.form.to_dict()
    #criar_membro()
    if request.method == 'GET':
        return render_template("create.html")
    if json_data is not None:
        #db.membro.insert_one(json_data)
        criar_membro(json_data)
        return jsonify(mensagem='usuario criado')
    else:
        return jsonify(mensagem='usuario não criado')
    
@app.route("/get-membro/<string:membroId>")
def getid(membroId):
    usuario = db.membro.find_one({"_id": ObjectId(membroId)})
    return flask.jsonify(json.loads(json_util.dumps(usuario)))

@app.route("/delete-membro/<string:membroId>", methods=['POST'])
def delete(membroId):
    result = db.membro.delete_one({"_id": ObjectId(membroId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='usuario removido')
    else:
        return jsonify(mensagem='usuario não removido')

@app.route('/update-membro', methods=['POST'])
def update():
    json_data = request.form.to_dict()
    if json_data is not None and db.usuario.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.usuario.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'email': json_data["email"]}})
        return jsonify(mensagem='usuario atualizado')
    else:
        return jsonify(mensagem='usuario não atualizado')