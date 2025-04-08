# Importação das bibliotecas necessárias
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import os

# 1. Leitura do arquivo de log
# Substitua 'log_file.csv' pelo caminho do arquivo real de logs
log_file_path = "log_file.csv"  # Caminho do arquivo de log

# Verifica se o arquivo existe antes de tentar carregá-lo
if os.path.exists(log_file_path):
    df = pd.read_csv(log_file_path)
    print("Arquivo de log carregado com sucesso!")
else:
    print("Erro: O arquivo de log não foi encontrado.")
    exit()

# 2. Exibir os dados brutos
print("\nDados de log carregados:")
print(df.head())  # Exibe as primeiras 5 linhas do log

# 3. Pré-processamento
# Converter o campo 'timestamp' para o tipo datetime (caso seja necessário)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Ignora erros de conversão

# Adicionando a coluna 'hora' a partir do 'timestamp'
df['hora'] = df['timestamp'].dt.hour

# Identificando se o status é erro (HTTP >= 400)
df['erro'] = df['status'].apply(lambda x: 1 if x <= 400 else 0)

# Exibindo os dados após o pré-processamento
print("\nDados após o pré-processamento:")
print(df.head())

# 4. Análise com Machine Learning (usando Isolation Forest)
# Selecionando as features para o modelo: hora e erro
# Caso queira adicionar mais colunas como 'recurso' ou outras, isso pode ser feito
X = df[['hora', 'erro']]

# Treinando o modelo de Isolation Forest
# Vamos usar uma contaminação de 5% (0.05), pois isso é mais realista em muitos cenários
modelo = IsolationForest(contamination=0.05, random_state=42)
df['anomalia'] = df['status'].apply(lambda x: 1 if x <= 400 else 0)

# Ajustando a classificação
df['classificacao'] = df['anomalia'].apply(lambda x: 'Normal' if x == 1 else 'Crítico')

# 5. Apresentação dos resultados

# Acessos críticos detectados
acessos_criticos = df[df['classificacao'] == 'Crítico']

# Exibindo resultados
print("\nClassificação dos acessos:")
print(df[['timestamp', 'ip', 'usuario', 'recurso', 'status', 'classificacao']])

if not acessos_criticos.empty:
    print("\nALERTA: Acessos críticos detectados!")
    print(acessos_criticos[['timestamp', 'ip', 'usuario', 'recurso', 'status']])
else:
    print("\nNenhum acesso crítico detectado.")

# 6. Visualização
plt.figure(figsize=(10, 6))
cores = {'Normal': 'green', 'Crítico': 'red'}
plt.scatter(df['timestamp'], df['hora'], c=df['classificacao'].map(cores))
plt.title("Eventos de Acesso Classificados")
plt.xlabel("Timestamp")
plt.ylabel("Hora do Acesso")
plt.legend(
    handles=[plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=cor, markersize=10) for cor in cores.values()],
    labels=cores.keys()
)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 7. Conclusão
print("\nAnálise concluída.")
if not acessos_criticos.empty:
    print("Acessos críticos foram detectados e apresentados acima.")
else:
    print("Não foram detectados acessos críticos.")
