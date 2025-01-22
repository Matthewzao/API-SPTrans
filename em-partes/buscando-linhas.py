import requests

base_url = "http://api.olhovivo.sptrans.com.br/v2.1"
token = "5bbb46f599373679c98ee76d837ac03922406b70ee12fa629645e95fb92ad02e"


session = requests.Session()


def autenticar():
    auth_url = f"{base_url}/Login/Autenticar?token={token}"
    auth_response = session.post(auth_url)  # Usa a sessão
    print("Status da autenticação:", auth_response.status_code)
    print("Resposta da autenticação:", auth_response.text)
    if auth_response.text == "true":
        print("Autenticação bem-sucedida.")
        return True
    else:
        print("Erro na autenticação.")
        return False


def buscar_linhas(termos_busca):
    url = f"{base_url}/Linha/Buscar?termosBusca={termos_busca}"
    print(f"Fazendo requisição para: {url}")
    response = session.get(url)  # Usa a sessão
    print("Status da busca:", response.status_code)
    print("Resposta bruta:", response.text)
    if response.status_code == 200:
        try:
            data = response.json()
            print("Resultado JSON:", data)
            return data
        except ValueError as e:
            print(f"Erro ao processar JSON: {e}")
            return None
    else:
        print(f"Erro ao buscar linhas: {response.status_code}")
        return None
    
    

if __name__ == "__main__":
    if autenticar():
        termos_busca = "8000" 
        linhas = buscar_linhas(termos_busca)
        if linhas and len(linhas) > 0:
            print("Linhas encontradas:", linhas)
        else:
            print("Nenhuma linha encontrada ou resposta vazia.")



    #         def buscar_posicoes_linha(codigo_linha):
    # url = f"{base_url}/Posicao/Linha?codigoLinha={codigo_linha}"
    # print(f"Fazendo requisição para: {url}")
    # response = session.get(url)
    # print("Status da busca de posição:", response.status_code)
    # print("Resposta bruta da posição:", response.text)
    # if response.status_code == 200:
    #     try:
    #         data = response.json()
    #         print("Posições dos ônibus:", data)  # Verificar a estrutura do JSON retornado
    #         return data
    #     except ValueError as e:
    #         print(f"Erro ao processar JSON: {e}")
    #         return None
    # else:
    #     print(f"Erro ao buscar posições: {response.status_code}")
    #     return None