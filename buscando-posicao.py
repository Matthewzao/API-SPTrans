import requests
import time
import csv
from datetime import datetime

base_url = "http://api.olhovivo.sptrans.com.br/v2.1"
token = "5bbb46f599373679c98ee76d837ac03922406b70ee12fa629645e95fb92ad02e"

# Sessão global para manter a autenticação
session = requests.Session()

# Função para autenticar
def autenticar():
    auth_url = f"{base_url}/Login/Autenticar?token={token}"
    auth_response = session.post(auth_url)
    if auth_response.text == "true":
        print("Autenticação bem-sucedida.")
        return True
    else:
        print("Erro na autenticação.")
        return False

# Função para buscar linhas
def buscar_linhas(termos_busca):
    url = f"{base_url}/Linha/Buscar?termosBusca={termos_busca}"
    response = session.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Erro ao processar JSON.")
            return None
    else:
        print(f"Erro ao buscar linhas: {response.status_code}")
        return None

# Função para buscar posições dos ônibus de uma linha específica
def buscar_posicoes_linha(codigo_linha):
    url = f"{base_url}/Posicao/Linha?codigoLinha={codigo_linha}"
    response = session.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except ValueError:
            print("Erro ao processar JSON.")
            return None
    else:
        print(f"Erro ao buscar posições: {response.status_code}")
        return None

if __name__ == "__main__":
    if autenticar():
        termos_busca = "6291-10" 
        linhas = buscar_linhas(termos_busca)
        if linhas and len(linhas) > 0:
            codigo_linha = linhas[0]["cl"]  # Código da primeira linha encontrada
            print(f"Código da linha encontrada: {codigo_linha}")
            
            # Abrir arquivo CSV para gravação
            with open("posicoes_onibus.csv", mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                # cabeçalhos
                writer.writerow(["DataHora", "VeiculoID", "Latitude", "Longitude"])
                
                # Loop para coletar dados a cada minuto por 1 hora
                for _ in range(60):  
                    posicoes = buscar_posicoes_linha(codigo_linha)
                    if posicoes and "vs" in posicoes:
                        for veiculo in posicoes["vs"]:
                            latitude = veiculo["py"]
                            longitude = veiculo["px"]
                            veiculo_id = veiculo["p"]
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            # Escrever dados no CSV
                            writer.writerow([timestamp, veiculo_id, latitude, longitude])
                            print(f"[{timestamp}] Veículo {veiculo_id}: ({latitude}, {longitude})")
                    else:
                        print("Nenhuma posição encontrada ou chave 'vs' ausente na resposta.")
                    
                    
                    time.sleep(30)
