import requests
import time
import csv
import math
from datetime import datetime
import folium

# Configurações da API
base_url = "http://api.olhovivo.sptrans.com.br/v2.1"
token = "5bbb46f599373679c98ee76d837ac03922406b70ee12fa629645e95fb92ad02e"

# Sessão global para manter a autenticação
session = requests.Session()

# Função para autenticar na API
def autenticar():
    auth_url = f"{base_url}/Login/Autenticar?token={token}"
    auth_response = session.post(auth_url)
    if auth_response.text == "true":
        print("Autenticação bem-sucedida.")
        return True
    else:
        print("Falha na autenticação.")
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

# Função para calcular a distância entre dois pontos usando a fórmula de Haversine
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371.0  # Raio da Terra em km
    distance = R * c
    return distance

# Função para atualizar o mapa com as posições dos veículos
def atualizar_mapa(mapa, veiculos):
    for veiculo in veiculos:
        latitude = veiculo["py"]
        longitude = veiculo["px"]
        veiculo_id = veiculo["p"]
        folium.Marker([latitude, longitude], popup=f"Veículo {veiculo_id}").add_to(mapa)

# Rodar o script principal
if __name__ == "__main__":
    try:
        if autenticar():
            termos_busca = "6291-10"  # Número da linha de ônibus que você deseja monitorar
            linhas = buscar_linhas(termos_busca)
            if linhas and len(linhas) > 0:
                codigo_linha = linhas[0]["cl"]
                print(f"Código da linha encontrada: {codigo_linha}")

                # Coordenadas do usuário (Estação Morumbi)
                lat_usuario = -23.625017782823342
                lon_usuario = -46.705442919411084

                # Inicializando o mapa
                mapa = folium.Map(location=[lat_usuario, lon_usuario], zoom_start=13)

                # Criar ou abrir arquivo CSV
                with open("posicoes_onibus.csv", mode="w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["DataHora", "VeiculoID", "Latitude", "Longitude", "DistanciaUsuario(km)", "DistanciaDestino(km)", "CodigoLinha"])

                    # Loop para coletar dados a cada 30 segundos por 1 hora (60 iterações)
                    for _ in range(60):
                        posicoes = buscar_posicoes_linha(codigo_linha)
                        if posicoes and "vs" in posicoes:
                            veiculos = posicoes["vs"]
                            atualizar_mapa(mapa, veiculos)

                            # Coordenadas do destino (Shopping Campo Limpo)
                            lat_destino = -23.650393747556485
                            lon_destino = -46.75716276383037

                            for veiculo in veiculos:
                                latitude = veiculo["py"]
                                longitude = veiculo["px"]
                                veiculo_id = veiculo["p"]
                                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                                # Calcular distâncias
                                distancia_usuario = haversine(lat_usuario, lon_usuario, latitude, longitude)
                                distancia_destino = haversine(latitude, longitude, lat_destino, lon_destino)

                                # Escrever os dados no arquivo CSV
                                writer.writerow([timestamp, veiculo_id, latitude, longitude, distancia_usuario, distancia_destino, codigo_linha])
                                print(f"[{timestamp}] Veículo {veiculo_id}: ({latitude}, {longitude}) - Distância do usuário: {distancia_usuario:.2f} km, Distância ao destino: {distancia_destino:.2f} km")

                            # Atualizar e salvar o mapa
                            print("Atualizando mapa...")
                            mapa.save("mapa_onibus.html")
                            print("Mapa gerado e salvo como mapa_onibus.html")
                        else:
                            print("Não foi possível obter as posições dos veículos.")

                        # Esperar 30 segundos antes de buscar novamente
                        time.sleep(30)
            else:
                print("Nenhuma linha encontrada.")
        else:
            print("Falha na autenticação.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")