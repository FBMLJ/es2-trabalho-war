from servico.firestore import db
from firebase_admin import auth
import requests
from constant import API_KEY
import json


def cadastro(email, senha):
    res = auth.create_user(email=email, password=senha)
    uid = res.uid
    try:
        user_ref =  db.collection('usuario').document(uid)
        user_ref.set({"nome": "teste"})
        return True
    except:
        
        auth.delete_user(uid)
        return False


def sign_in(email, senha):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(API_KEY)
    res = requests.post(url, {"email":email,"password":senha})
    if res.status_code == 200:
        token = json.loads(res.text)['idToken']

        return token
    else:
        return False


def verificarUsuario(token):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={}'.format(API_KEY)
    res = requests.post(url,{"idToken": token})
    if res.status_code == 200:
        return True
    else:
        return False
