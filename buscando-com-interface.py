import requests
import time
import csv
import math
from datetime import datetime
from sklearn.linear_model import LinearRegression
import numpy as np

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

# Função para calcular a distância entre o usuário e o ônibus usando a fórmula Haversine
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371.0  # Raio da Terra em km
    distance = R * c
    return distance

if __name__ == "__main__":
    if autenticar():
        termos_busca = "6291-10"  # Exemplo de número da linha
        linhas = buscar_linhas(termos_busca)
        if linhas and len(linhas) > 0:
            codigo_linha = linhas[0]["cl"]  # Código da primeira linha encontrada
            print(f"Código da linha encontrada: {codigo_linha}")

            # Coordenadas do usuário (podem ser recebidas dinamicamente)
            lat_usuario = -23.5505  # Exemplo de latitude do usuário
            lon_usuario = -46.6333  # Exemplo de longitude do usuário

            # Criar listas para armazenar dados para treinamento
            distancias = []
            tempos_viagem = []

            # Abrir arquivo CSV para gravação
            with open("posicoes_onibus.csv", mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["DataHora", "VeiculoID", "Latitude", "Longitude", "Distancia_usuario(km)"])

                # Loop para coletar dados a cada 30 segundos por 1 hora
                for _ in range(60):
                    posicoes = buscar_posicoes_linha(codigo_linha)
                    if posicoes and "vs" in posicoes:
                        for veiculo in posicoes["vs"]:
                            latitude = veiculo["py"]
                            longitude = veiculo["px"]
                            veiculo_id = veiculo["p"]
                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            # Calcular a distância do ônibus até o usuário
                            distancia_usuario = haversine(lat_usuario, lon_usuario, latitude, longitude)

                            # Aqui, você pode adicionar o tempo de viagem estimado manualmente ou com base na velocidade do ônibus
                            tempo_viagem_estimado = distancia_usuario * 5  # Exemplo simples de tempo (distância * fator)

                            # Armazenar os dados para o treinamento do modelo
                            distancias.append([distancia_usuario])
                            tempos_viagem.append(tempo_viagem_estimado)

                            # Escrever os dados no arquivo CSV
                            writer.writerow([timestamp, veiculo_id, latitude, longitude, distancia_usuario])
                            print(f"[{timestamp}] Veículo {veiculo_id}: ({latitude}, {longitude}) - Distância: {distancia_usuario:.2f} km")

                    # Treinar o modelo com os dados coletados até agora
                    if len(distancias) > 10:  # Garantir que temos dados suficientes
                        X = np.array(distancias)
                        y = np.array(tempos_viagem)

                        # Criando o modelo de regressão linear
                        modelo = LinearRegression()
                        modelo.fit(X, y)

                        # Prevendo o tempo de viagem para uma nova distância
                        nova_distancia = np.array([[10]])  # Exemplo de nova distância (10 km)
                        tempo_estimado = modelo.predict(nova_distancia)
                        print(f"Tempo estimado para uma distância de 10 km: {tempo_estimado[0]:.2f} minutos")

                    time.sleep(30)  # Espera 30 segundos antes de buscar novamente

