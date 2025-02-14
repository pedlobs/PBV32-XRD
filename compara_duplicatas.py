import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from glob import glob
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# Lista para armazenar os dados e seus valores máximos
file_data = []

sns.color_palette("rocket", as_cmap=True)

# Carrega e processa todos os arquivos CSV na pasta "dados"
for diretorio_csv in glob("dados/*.csv"):
    nome = diretorio_csv.split("\\")[-1].replace(".csv", "")
    nome_txt = nome.split(" ")[0]  # Nome a ser utilizado no arquivo final

    data = pd.read_csv(diretorio_csv)
    data.columns = ["2theta (º)", nome]
    max_value = data[nome].max()
    file_data.append((nome, data, max_value))

# Ordena os dados em ordem crescente
file_data.sort(key=lambda x: x[2])

# Cria DataFrame para a matriz de correlação
heat = pd.DataFrame()
for nome, data, _ in file_data:
    if heat.empty:
        heat = data.set_index("2theta (º)")
    else:
        heat[nome] = data[nome].values

# Cria a matriz de correlação Pearson
corr_pearson = heat.corr(method="pearson")

# Cria uma figura
fig, ax = plt.subplots(figsize=(14, 6))

# Offset inicial e incremento
offset = 0
incremento_offset = 1e10

# Adicionar curvas ao gráfico
for nome, data, _ in file_data:
    data[nome] += offset
    ax.plot(data["2theta (º)"], data[nome], label=nome, linewidth=0.8)
    offset += incremento_offset

# Configurações principais
ax.set_title("Difração")
ax.set_xlim(0, 40)
ax.set_ylim(0, 150e9)
ax.set_xlabel("2theta (º)")
ax.set_ylabel("Intensidade (u.a.)")
ax.legend(loc="upper left", bbox_to_anchor=(0.02, 0.98), frameon=True)

# Criar gráfico insetado no canto superior direito
ax_inset = inset_axes(ax, width="45%", height="45%", loc="upper right", borderpad=0   # Ajustar o espaçamento para ficar mais rente
)

# Plotar o heatmap no gráfico inserido
sns.heatmap(
    corr_pearson,
    ax=ax_inset,
    cmap="viridis",
    cbar=False,  # Remover barra de cor para simplificar
    annot=True,
    fmt=".2",
    annot_kws={"size": 10},  # Aumenta o tamanho do texto dentro das células
    square=True  # Força o formato quadrado
)

# Configurar título e ajustar os labels para o gráfico inserido
ax_inset.set_title("Correlação Pearson", fontsize=10)
ax_inset.set_xticklabels(ax_inset.get_xticklabels(), rotation=45, fontsize=8)
ax_inset.set_yticklabels(ax_inset.get_yticklabels(), fontsize=8)

# Salvar como SVG
plt.savefig(f"Difração - {nome_txt}.svg")

# Exibir o gráfico
#plt.show()

