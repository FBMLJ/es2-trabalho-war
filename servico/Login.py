from servico.firestore import db
from firebase_admin import auth
import requests
from constant import API_KEY
import json


def cadastro(email, nome_de_usuario, senha):

    try:
        usuario = auth.create_user(email=email, display_name=nome_de_usuario, password=senha)
    except:
        return False, "Falha no cadastro, revise seus campos e tente novamente"

    uid = usuario.uid
    dados = {
        "id_usuario": uid,
        "nome": nome_de_usuario,
        "numero_de_vitorias": 0,
        "numero_de_derrotas": 0
    }
    try:
        user_ref = db.collection('usuarios').document(uid)
        user_ref.set(dados)
        return True, usuario
    except:
        auth.delete_user(uid)
        return False, "Falha no cadastro, tente novamente"


def sign_in(email, senha):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(API_KEY)
    res = requests.post(url, {"email":email,"password":senha})
    res_json = json.loads(res.text)
    if res.status_code == 200:
        usuario = auth.get_user(res_json["localId"])
        return True, usuario
    else:
        return False, "Falha no login, Verifique seus campos e tente novamente"


def verificarUsuario(token):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={}'.format(API_KEY)
    res = requests.post(url,{"idToken": token})
    if res.status_code == 200:
        return True
    else:
        return False
