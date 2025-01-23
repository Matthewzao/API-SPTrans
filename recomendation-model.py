import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

data_file_path = "C:\\Users\\mateu\\OneDrive\\Área de Trabalho\\New folder\\posicoes_onibus.csv"

# treinando o modelo de recomendação
def treinar_modelo(data_file_path):
    # dados do CSV
    dados = pd.read_csv(data_file_path)

    # verificanco se o CSV contém os dados esperados
    if not all(col in dados.columns for col in ["DistanciaUsuario(km)", "DistanciaDestino(km)", "CodigoLinha"]):
        raise ValueError("O arquivo CSV não contém as colunas necessárias para treinamento.")

    # selecionar as colunas relevantes e o alvo
    X = dados[["DistanciaUsuario(km)", "DistanciaDestino(km)"]]
    y = dados["CodigoLinha"]  

    # dividir os dados em treinamento e teste
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # criar e treinar o modelo
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    # avaliar o modelo
    y_pred = modelo.predict(X_test)
    acuracia = accuracy_score(y_test, y_pred)
    print(f"Acurácia do modelo: {acuracia * 100:.2f}%")

    return modelo

# recomendar a melhor linha com base em distâncias
def recomendar_linha(modelo, distancia_usuario, distancia_destino):
    
    entrada = [[distancia_usuario, distancia_destino]]

    # fazer a previsão
    linha_recomendada = modelo.predict(entrada)[0]
    print(f"Linha recomendada: {linha_recomendada}")

    return linha_recomendada

if __name__ == "__main__":
    # arquivo CSV gerado pelo script de coleta
    csv_file = "posicoes_onibus.csv"

    # treinar o modelo
    print("Treinando o modelo...")
    modelo = treinar_modelo(csv_file)

    # exemplo de recomendação
    print("Recomendando uma linha...")
    distancia_usuario = 2.5  # exemplo de distância do usuário em km
    distancia_destino = 5.0  # exemplo de distância ao destino em km
    recomendar_linha(modelo, distancia_usuario, distancia_destino)
