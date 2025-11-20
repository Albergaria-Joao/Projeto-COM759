from flask import json, request, jsonify, render_template, redirect, session
import flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId
import os
import bcrypt
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    if session.get("nome") == None:
        return redirect("/login")
    
    tarefas = list(db.tarefa.aggregate([
        {
            "$lookup": {
                "from": "membro",
                "localField": "membro_id",
                "foreignField": "_id",
                "as": "membro_info"
            }
        },
        {
            "$unwind": {
                "path": "$membro_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "nome": 1,
                "descricao": 1,
                "membro_login": "$membro_info.login",
                "prazo": 1,
                "criacao": 1,
            }
        }
    ]))


    return render_template("dashboard.html", membros=db.membro.find().sort("_id", 1), tarefas=tarefas)
    #return flask.jsonify(json.loads(json_util.dumps(db.membro.find({}).sort("_id", 1))))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'GET'):
        return render_template("login.html")
    
    json_data = request.form.to_dict()
    print(json_data)
    user = db.membro.find_one({"login": json_data["login"]})
    print(user)
    #print(user["senha"])
    if (hashing(json_data["senha"], user["senha"]) == user["senha"]):
        session["nome"] = user["nome"]
        return redirect("/index")
    else:
        return redirect("/erro")
    
@app.route('/logout', methods=['POST'])
def logout():
    session.pop("nome", None)
    return jsonify(mensagem='logout realizado')

    

salt = bcrypt.gensalt()
def hashing(password, salt):
    bytes_password = password.encode('utf-8')  # Convert to bytes
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    print(hashed_password)
    return hashed_password

def criar_membro_db(dados):
    membro = db["membro"]

    password = dados["senha"]
    hashed_password = hashing(password, salt)
    dados["senha"] = hashed_password

    resultado = membro.insert_one(dados)
    #

@app.route('/create-membro', methods=['GET', 'POST'])
def create_membro():
    json_data = request.form.to_dict()
    #criar_membro()
    if request.method == 'GET':
        return render_template("create_membro.html")
    if json_data is not None:
        #db.membro.insert_one(json_data)
        if db.membro.find_one({"login": json_data["login"]}) is not None:
            return jsonify(mensagem='membro já existe')
        criar_membro_db(json_data)
        return jsonify(mensagem='membro criado')
    else:
        return jsonify(mensagem='membro não criado')
    


    #

@app.route('/create-tarefa', methods=['GET', 'POST'])
def create_tarefa():
    
    #criar_membro()
    if request.method == 'GET':
        return render_template("create_tarefa.html")
    
    json_data = request.form.to_dict()
    json_data["membro_id"] = ObjectId(json_data["membro_id"]) 
    now = datetime.now()
    json_data["criacao"] = now.strftime("%Y-%m-%dT%H:%M")
    #json_data["criacao"] = now
    print(json_data)
    if json_data is not None:
        db.tarefa.insert_one(json_data)
        return jsonify(mensagem='tarefa criada')
    else:
        return jsonify(mensagem='tarefa não criada')
    
@app.route('/get-membros', methods=['POST'])
def get_membros():
    return flask.jsonify(json.loads(json_util.dumps(db.membro.find({}).sort("_id", 1))))
    
# @app.route("/get-membro/<string:membroId>")
# def getid(membroId):
#     membro = db.membro.find_one({"_id": ObjectId(membroId)})
#     return flask.jsonify(json.loads(json_util.dumps(membro)))


@app.route('/get-tarefas', methods=['POST'])
def get_tarefas():
    tarefas = list(db.tarefa.aggregate([
        {
            "$lookup": {
                "from": "membro",
                "localField": "membro_id",
                "foreignField": "_id",
                "as": "membro_info"
            }
        },
        {
            "$unwind": {
                "path": "$membro_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "nome": 1,
                "descricao": 1,
                "membro_login": "$membro_info.login",
                "prazo": 1,
                "criacao": 1,
            }
        }
    ]))

    return jsonify(json.loads(json_util.dumps(tarefas)))


@app.route('/update-membro', methods=['GET', 'POST'])
def update_membro():
    if request.method == 'GET':
        return render_template("update_membro.html")

    json_data = request.form.to_dict()
    print(json_data)
    if json_data is not None and db.membro.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.membro.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'email': json_data["email"]}})
        return jsonify(mensagem='membro atualizado')
    else:
        return jsonify(mensagem='membro não atualizado')
    
@app.route('/update-tarefa', methods=['GET', 'POST'])
def update_tarefa():
    if request.method == 'GET':
        return render_template("update_tarefa.html")

    json_data = request.form.to_dict()
    json_data["membro_id"] = ObjectId(json_data["membro_id"]) 
    print(json_data)
    if json_data is not None and db.tarefa.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.tarefa.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'descricao': json_data["descricao"], 'prazo': json_data["prazo"], 'membro_id': json_data["membro_id"]}})
        print("atualizou!!!")
        return jsonify(mensagem='tarefa atualizado')
    else:
        return jsonify(mensagem='tarefa não atualizado')


@app.route("/delete-membro/<string:membroId>", methods=['POST'])
def delete_membro(membroId):
    result = db.membro.delete_one({"_id": ObjectId(membroId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='membro removido')
    else:
        return jsonify(mensagem='membro não removido')

@app.route("/delete-tarefa/<string:tarefaId>", methods=['POST'])
def tarefa_membro(tarefaId):
    result = db.tarefa.delete_one({"_id": ObjectId(tarefaId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='tarefa removido')
    else:
        return jsonify(mensagem='tarefa não removido')
