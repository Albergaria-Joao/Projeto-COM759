from app import app
from app import db
import bcrypt


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
    "senha": hashed_password,
    "idade": 21
}