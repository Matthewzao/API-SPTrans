import requests

token = "5bbb46f599373679c98ee76d837ac03922406b70ee12fa629645e95fb92ad02e"
        

auth_url = "http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token=5bbb46f599373679c98ee76d837ac03922406b70ee12fa629645e95fb92ad02e"
auth_response = requests.post(auth_url)

if auth_response.text == "true":
    print("autenticação bem sucedida")
else:
    print(f"erro na autenticação: {auth_response.status_code}")
    print(f"resposta do servidor: {auth_response.text}")