from flask import json, request, jsonify, render_template, redirect, session
import flask
from flask import Flask
from bson import json_util
from app import app
from app import db
from bson.objectid import ObjectId
import os
import bcrypt
from datetime import datetime
from functools import wraps
import random
 

# OS TEMPLATES AQUI NO BACKEND SÃO SÓ TESTES. O FRONTEND É NO VUE



def admin_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(dict(session))
        if "auth" not in session or session["auth"] != "admin":
            return jsonify(mensagem="Acao nao autorizada")
        return f(*args, **kwargs)
    return wrapper

def gerente_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        print(dict(session))
        if "auth" not in session or (session["auth"] != "gerente" and session["auth"] != "admin"):
            return jsonify(mensagem="Acao nao autorizada")
        return f(*args, **kwargs)
    return wrapper

@app.route('/debug-session')
def debug_session():
    return jsonify(dict(session))

@app.route('/')
@app.route('/index')
def index():
    
    tarefas = join_tarefas()

    membros = join_membros()

    return render_template("dashboard.html", membros=membros, tarefas=tarefas, equipes=db.equipe.find().sort("_id", 1))

@app.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    print("dados: ", json_data)
    user = db.membro.find_one({"login": json_data["login"]})
    if not user:
        return jsonify(status=403, mensagem="login falhou")
    if (hashing(json_data["senha"], user["senha"]) == user["senha"]):
        session["username"] = user["login"]
        session["nome"] = user["nome"]
        session["auth"] = user["auth"]
        session["equipe_id"] = user["equipe_id"]
        print(user["equipe_id"])
        print("tentou logar")
        return jsonify(status=200, username=user["login"], nome=user["nome"], auth=user["auth"], equipe_id=user["equipe_id"])
    else:
        return jsonify(status=403,mensagem='login falhou')
            
    

    
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify(mensagem='logout realizado')

    

salt = bcrypt.gensalt()
def hashing(password, salt):
    bytes_password = password.encode('utf-8')  # Convert to bytes
    hashed_password = bcrypt.hashpw(bytes_password, salt)
    return hashed_password

def criar_membro_db(dados):
    membro = db["membro"]

    senha = dados["senha"]
    hashed = hashing(senha, salt)

    membro_dados = {
        "login": dados["login"],
        "nome": dados["nome"],
        "email": dados["email"],
        "senha": hashed,
        "equipe_id": dados["equipe_id"],
        "auth": dados["auth"]
    }

    membro.insert_one(membro_dados)
    

@app.route('/create-membro', methods=['POST'])
@gerente_auth
def create_membro():
    json_data = request.get_json()
    #criar_membro()
    if request.method == 'GET':
        return render_template("create_membro.html")

    if json_data is not None:
        if db.membro.find_one({"login": json_data["login"]}) is not None:
            return jsonify(mensagem='membro já existe')

        json_data["equipe_id"] = ObjectId(json_data["equipe_id"]) 
        criar_membro_db(json_data)
        return jsonify(mensagem='membro criado')
    else:
        return jsonify(mensagem='membro não criado')
    
def join_membros():
    membros = list(db.membro.aggregate([
        {
            "$lookup": {
                "from": "equipe",
                "localField": "equipe_id",
                "foreignField": "_id",
                "as": "equipe_info"
            }
        },
        {
            "$unwind": {
                "path": "$equipe_info",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 1,
                "login": 1,
                "nome": 1,
                "email": 1,
                "senha": 1,
                "equipe_nome": "$equipe_info.nome",
                "auth": 1
            }
        }
    ]))

    return membros

@app.route('/get-membros', methods=['POST'])
@app.route('/get-membros/<string:membroId>', methods=['POST'])
def get_membros(membroId=None):

    if membroId is not None:
        membro = db.membro.find_one({"_id": ObjectId(membroId)})
        return jsonify(json.loads(json_util.dumps(membro)))

    membros = join_membros()

    json_data = request.get_json()

    if json_data.get("equipe_id") is None: # Se quiser pegar todos os membros, não passar id da equipe
        return jsonify(json.loads(json_util.dumps(membros)))

    if json_data.get("equipe_id") is not None and db.equipe.find_one({"_id": ObjectId(json_data["equipe_id"])}) is not None:
        membros = db.membro.find({"equipe_id": ObjectId(json_data["equipe_id"])}).sort("_id", 1)
        

    return jsonify(json.loads(json_util.dumps(membros)))


@app.route('/update-membro', methods=['POST'])
@gerente_auth
def update_membro():
    if request.method == 'GET':
        return render_template("update_membro.html")

    json_data = request.get_json()
    json_data["equipe_id"] = ObjectId(json_data["equipe_id"]) 
    if json_data is not None and db.membro.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.membro.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'email': json_data["email"], 'equipe_id': json_data["equipe_id"], 'auth': json_data["auth"]}})
        return jsonify(mensagem='membro atualizado')
    else:
        return jsonify(mensagem='membro não atualizado')
    
@app.route("/reset-senha/<string:membroId>", methods=['POST'])
@admin_auth
def reset_senha(membroId):

    senha = str(random.randint(100000, 999999))
    hashed = hashing(senha, salt)

    if db.membro.find_one({"_id": ObjectId(membroId)}) is not None:
        db.membro.update_one({'_id': ObjectId(membroId)}, 
                              {"$set": {'senha': hashed }})
        return jsonify(mensagem=f'NOVA SENHA: {senha}')
    else:
        return jsonify(mensagem='Senha NÃO resetada')
    


@app.route("/delete-membro/<string:membroId>", methods=['POST'])
@gerente_auth
def delete_membro(membroId):

    
    result = db.membro.delete_one({"_id": ObjectId(membroId)})
    
    if(result.deleted_count > 0):
        return jsonify(mensagem='membro removido')
    else:
        return jsonify(mensagem='membro não removido')


# TAREFA


@app.route('/create-tarefa', methods=['POST'])
@gerente_auth
def create_tarefa():

    if request.method == 'GET':
        return render_template("create_tarefa.html")

    json_data = request.get_json()
    if json_data is not None:
        
        now = datetime.now()
        tarefa_dados = {
            "nome": json_data["nome"],
            "descricao": json_data["descricao"],
            "membro_id": ObjectId(json_data["membro_id"]),
            "equipe_id": ObjectId(json_data["equipe_id"]),
            "prazo": json_data["prazo"],
            "criacao": now.strftime("%Y-%m-%dT%H:%M"),
            "status": "A fazer"
        }
    
        db.tarefa.insert_one(tarefa_dados)
        return jsonify(mensagem='tarefa criada')
    else:
        return jsonify(mensagem='tarefa não criada')

def join_tarefas():
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
            "$lookup": {
                "from": "equipe",
                "localField": "equipe_id",
                "foreignField": "_id",
                "as": "equipe_info"
            }
        },
        {
            "$unwind": {
                "path": "$equipe_info",
                "preserveNullAndEmptyArrays": True
            }
        },

        {
            "$project": {
                "nome": 1,
                "descricao": 1,
                "membro_login": "$membro_info.login",
                "equipe_nome": "$equipe_info.nome",
                "prazo": 1,
                "criacao": 1,
                "conclusao": 1,
                "status": 1
            }
        }
    ]))

    return tarefas

@app.route('/get-tarefas', methods=['POST'])
@app.route('/get-tarefas/<string:tarefaId>', methods=['POST'])
def get_tarefas(tarefaId=None):

    if tarefaId is not None:
        tarefa = db.tarefa.find_one({"_id": ObjectId(tarefaId)})
        return jsonify(json.loads(json_util.dumps(tarefa)))
    
    json_data = request.get_json()


    if json_data.get("equipe_id") is None: # Se quiser pegar todas as tarefas, não passar id da equipe
        tarefas = join_tarefas()
        return jsonify(json.loads(json_util.dumps(tarefas)))

    if json_data.get("equipe_id") is not None and db.equipe.find_one({"_id": ObjectId(json_data["equipe_id"])}) is not None:
        tarefas = db.tarefa.find({"equipe_id": ObjectId(json_data["equipe_id"])}).sort("_id", 1)
    

    return jsonify(json.loads(json_util.dumps(tarefas)))


    

    
@app.route('/update-tarefa', methods=['POST'])
@gerente_auth
def update_tarefa():
    if request.method == 'GET':
        return render_template("update_tarefa.html")
    

    json_data = request.get_json()
    json_data["membro_id"] = ObjectId(json_data["membro_id"])
    json_data["equipe_id"] = ObjectId(json_data["equipe_id"])  
    if json_data is not None and db.tarefa.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.tarefa.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'descricao': json_data["descricao"], 'prazo': json_data["prazo"], 'membro_id': json_data["membro_id"], 'equipe_id': json_data["equipe_id"]}})
        return jsonify(mensagem='tarefa atualizado')
    else:
        return jsonify(mensagem='tarefa não atualizado')


@app.route('/update-status-tarefa/<string:tarefaId>', methods=['POST'])
def update_status_tarefa(tarefaId):

    json_data = request.get_json()
    

    if (json_data["status"] == "Concluída"):
        now = datetime.now()
        now_format = now.strftime("%Y-%m-%dT%H:%M")
        db.tarefa.update_one({'_id': ObjectId(tarefaId)}, 
                            {"$set": {'status': json_data["status"], 'conclusao': now_format}})
        return jsonify(mensagem='tarefa atualizado')
    
    db.tarefa.update_one({'_id': ObjectId(tarefaId)}, 
                            {"$set": {'status': json_data["status"]}})
    return jsonify(mensagem='tarefa atualizado')


@app.route("/delete-tarefa/<string:tarefaId>", methods=['POST'])
@gerente_auth
def delete_tarefa(tarefaId):
    
    result = db.tarefa.delete_one({"_id": ObjectId(tarefaId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='tarefa removido')
    else:
        return jsonify(mensagem='tarefa não removido')


# EQUIPE

@app.route('/create-equipe', methods=['POST'])
@admin_auth
def create_equipe():
    print(dict(session))
    if request.method == 'GET':
        return render_template("create_equipe.html")

    json_data = request.get_json()

    if json_data is not None:

        equipe_dados = {
            "nome": json_data["nome"],
            "descricao": json_data["descricao"]
        }



        db.equipe.insert_one(equipe_dados)
        return jsonify(mensagem='Equipe criada')
    else:
        return jsonify(mensagem='Equipe não criada')
    

@app.route('/get-equipes', methods=['POST'])
@app.route('/get-equipes/<string:equipeId>', methods=['POST'])
def get_equipes(equipeId=None):
    print(dict(session))
    if equipeId is not None:
        equipe = db.equipe.find_one({"_id": ObjectId(equipeId)})
        return jsonify(json.loads(json_util.dumps(equipe)))

    return flask.jsonify(json.loads(json_util.dumps(db.equipe.find({}).sort("nome", 1))))

@app.route('/update-equipe', methods=['POST'])
@admin_auth
def update_equipe():
    if request.method == 'GET':
        return render_template("update_equipe.html")

    json_data = request.get_json()
    if json_data is not None and db.equipe.find_one({"_id": ObjectId(json_data["id"])}) is not None:
        db.equipe.update_one({'_id': ObjectId(json_data["id"])}, 
                              {"$set": {'nome': json_data["nome"], 'descricao': json_data["descricao"]}})
        return jsonify(mensagem='Equipe atualizada')
    else:
        return jsonify(mensagem='Equipe não atualizada')
    

@app.route("/delete-equipe/<string:equipeId>", methods=['POST'])
@admin_auth
def delete_equipe(equipeId):
    
    result = db.equipe.delete_one({"_id": ObjectId(equipeId)})
    if(result.deleted_count > 0):
        return jsonify(mensagem='Equipe removida')
    else:
        return jsonify(mensagem='Equipe não removida')