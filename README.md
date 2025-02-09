![Map](C:\Users\mateu\OneDrive\Área de Trabalho\Pipeline\API-SPTrans\map.png)


# **Projeto de Coleta de Dados e Recomendação de Linha de Ônibus**

Este projeto realiza a coleta de dados de veículos de transporte público em São Paulo (SP), utilizando a API do Olho Vivo da SPTrans. Com esses dados, um modelo de machine learning (Random Forest) é treinado para recomendar a melhor linha de ônibus com base nas distâncias entre o usuário, o destino e as posições dos veículos.

## **Funcionalidades**

### **Coleta de Dados**
- O script coleta informações de posição dos ônibus de uma linha específica a cada 30 segundos durante uma hora.
- Os dados coletados incluem a hora da coleta, a posição do ônibus (latitude e longitude), a distância do usuário e do destino (Shopping Campo Limpo), e o código da linha do ônibus.
- Os dados são salvos em um arquivo CSV chamado posicoes_onibus.csv.

### **Recomendação de Linha de Ônibus**
- O modelo de machine learning é treinado com os dados coletados (distâncias entre usuário, destino e a linha de ônibus).
- Após o treinamento, o modelo recomenda a linha de ônibus mais adequada para um usuário, dado a distância entre o usuário e o destino.

## **Requisitos**
- Python 3.6 ou superior
- Bibliotecas:
    - `requests`
    - `time`
    - `csv`
    - `math`
    - `datetime`
    - `dotenv`
    - `pandas`
    - `scikit-learn`

  
## **Como Usar**
### **Configuração Inicial**
Clone este repositório:
git clone https: //github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio

Crie um arquivo .env

API_TOKEN=seu_token_aqui

**Coleta de Dados**

Para coletar dados de posições de ônibus, execute o script de coleta:

python coleta_dados.py

Isso irá gerar o arquivo `posicoes_onibus.csv` com os dados das posições dos veículos.

**Treinando Modelo**

Com o arquivo `posicoes_onibus.csv` gerado, execute o script para treinar o modelo de recomendação de linha de ônibus:

python modelo_recomendacao.py

O modelo será treinado e exibirá a acurácia do modelo de previsão.

**Recomendação de Linha**

Após treinar o modelo, você pode recomendar uma linha de ônibus para um usuário com base nas distâncias. O script irá utilizar as distâncias do usuário até o ponto de origem e até o destino.

**Exemplo:**


`distancia_usuario = 2.5  # Distância do usuário em km`

`distancia_destino = 5.0  # Distância até o destino em km`

`linha_recomendada = recomendar_linha(modelo, distancia_usuario, distancia_destino)`

`print(f"Linha recomendada: {linha_recomendada}")`


## **Estrutura do Projeto**

├── coleta_dados.py           # Script para coleta de dados da API SPTrans

├── modelo_recomendacao.py    # Script para treinamento do modelo de recomendação

├── posicoes_onibus.csv       # Arquivo CSV com os dados coletados

├── requirements.txt          # Arquivo com dependências do projeto

└── .env                      # Arquivo de configuração com o API_TOKEN















