import requests
import time

base_url = "http://api.olhovivo.sptrans.com.br/v2.1"
token = "5bbb46f599373679c98ee76d837ac03922406b70ee12fa629645e95fb92ad02e"

# Sessão global para manter a autenticação
session = requests.Session()

# Função para autenticar
def autenticar():
    auth_url = f"{base_url}/Login/Autenticar?token={token}"
    auth_response = session.post(auth_url)
    print("Status da autenticação:", auth_response.status_code)
    print("Resposta da autenticação:", auth_response.text)
    if auth_response.text == "true":
        print("Autenticação bem-sucedida.")
        return True
    else:
        print("Erro na autenticação.")
        return False

# Função para buscar linhas
def buscar_linhas(termos_busca):
    url = f"{base_url}/Linha/Buscar?termosBusca={termos_busca}"
    print(f"Fazendo requisição para: {url}")
    response = session.get(url)
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

# Função para buscar posições dos ônibus de uma linha específica
def buscar_posicoes_linha(codigo_linha):
    url = f"{base_url}/Posicao/Linha?codigoLinha={codigo_linha}"
    print(f"Fazendo requisição para: {url}")
    response = session.get(url)
    print("Status da busca de posição:", response.status_code)
    print("Resposta bruta da posição:", response.text)
    if response.status_code == 200:
        try:
            data = response.json()
            print("Posições dos ônibus JSON:", data)  # Verificar a estrutura do JSON retornado
            return data
        except ValueError as e:
            print(f"Erro ao processar JSON: {e}")
            return None
    else:
        print(f"Erro ao buscar posições: {response.status_code}")
        return None

if __name__ == "__main__":
    if autenticar():
        termos_busca = "6291-10" 
        linhas = buscar_linhas(termos_busca)
        print(f"Linhas retornadas: {linhas}")
        if linhas and len(linhas) > 0: # Correção do acesso ao primeiro elemento da lista
            codigo_linha = linhas[0]["cl"]  # Pega o código da primeira linha encontrada

            print(f"Código da linha encontrada: {codigo_linha}")

            posicoes = buscar_posicoes_linha(codigo_linha)
            print(f"Posições retornadas: {posicoes}")
            if posicoes and 'vs' in posicoes:
                for veiculo in posicoes['vs']:
                    latitude = veiculo['py']
                    longitude = veiculo['px']
                    print(f"Veículo {veiculo['p']} está na posição: ({latitude}, {longitude})")
            else:
                print("Nenhuma posição encontrada ou chave 'vs' ausente na resposta.")

        else:
            print("Nenhuma linha encontrada ou resposta vazia.")