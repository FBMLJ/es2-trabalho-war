import servico.firebase

from firebase_admin import auth
import requests

from constant import API_KEY
import json


def cadastro(email, senha):
    auth.create_user(email=email,password = senha)



def sign_in(email, senha):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(API_KEY)
    res = requests.post(url, {"email":email,"password":senha})
    if res.status_code == 200:
        token = json.loads(res.text)['idToken']
        print('login realizado com sucesso')
        return token
    else:
        print(res.status_code)
        print('Erro ao fazer o login')
    
def verificarUsuario(token):
    url = 'https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={}'.format(API_KEY)
    res = requests.post(url,{"idToken": token})
    if res.status_code == 200:
        return True
    else:
        return False
