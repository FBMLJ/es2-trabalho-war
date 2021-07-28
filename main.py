
import servico.Login as login

token = None


if __name__ == "__main__":
    
    token = login.sign_in('lucas@lucas.com','123456')
    login.verificarUsuario(token)