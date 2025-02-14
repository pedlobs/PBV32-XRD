import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from glob import glob
from time import time
from pathlib import Path
import plotly.io as pio

# Lista para armazenar os dados e seus valores máximos
file_data = []

# Inicializa uma figura vazia
fig = go.Figure()

for diretorio_csv in glob(f"Dados_Difração_Paineira/*.csv"):
    try:
        # Lê os dados do arquivo CSV
        data = pd.read_csv(diretorio_csv)

        # Armazena o dataframe e seu valor máximo
        max_value = data.iloc[:, 1].max()
        file_data.append((diretorio_csv, data, max_value))
    
    except Exception as e:
        print(f"Erro ao processar {diretorio_csv}: {e}")

# Ordena as curvas pelos picos em ordem crescente
file_data.sort(key=lambda x: x[2])

# Offset inicial
offset = 0

# Incremento de offset entre curvas
offset_increment = 5e11

pio.renderers.default = "iframe"

for file, data, _ in file_data:
    # Define os nomes das colunas (X e Y) para melhor legibilidade
    x_col, y_col = data.columns

    

    # Adiciona o offset à coluna Y para empilhar as curvas
    data[y_col] += offset

    # Adiciona uma linha ao gráfico para cada arquivo
    fig.add_trace(go.Scatter(x=data[x_col], y=data[y_col], mode='lines', name=file.replace("Dados_Difração_Paineira\\","")))

    # Atualiza o offset para a próxima curva
    offset += offset_increment

# Personaliza o layout do gráfico
fig.update_layout(
    height = 850,
    title="Difração das amostras",
    xaxis_title='2θ (graus)',
    yaxis_title="Intensidades Empilhadas (u.a.)",
    template="plotly_white"
)

# Exibe o gráfico
fig.show()