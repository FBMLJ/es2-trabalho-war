import servico.firebase

from firebase_admin import auth
import requests

from constant import API_KEY


def cadastro(email, senha):
    auth.create_user(email=email,password = senha)



def sign_in(email, senha):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={}".format(API_KEY)
    r = requests.post(url, {"email":email,"password":senha})
    print(r.content.decode('utf-8'))
