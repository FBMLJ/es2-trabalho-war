import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("servico/projeto-war-firebase-adminsdk-2sej5-d549289715.json")
app = firebase_admin.initialize_app(cred)
