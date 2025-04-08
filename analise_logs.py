import pandas as pd
import numpy as np
import re  # Biblioteca para expressões regulares
from sklearn.ensemble import IsolationForest
import matplotlib.pyplot as plt
import os

# 1. Leitura do arquivo de log
log_file_path = "log_file.csv"  # Caminho do arquivo de log

# Verifica se o arquivo existe antes de tentar carregá-lo
if os.path.exists(log_file_path):
    df = pd.read_csv(log_file_path)
    print("Arquivo de log carregado com sucesso!")
else:
    print("Erro: O arquivo de log não foi encontrado.")
    exit()

# 2. Exibir as colunas e as primeiras linhas para verificar o conteúdo
print("\nColunas no arquivo CSV:")
print(df.columns)  # Exibe os nomes das colunas
print("\nPrimeiras linhas do arquivo CSV:")
print(df.head())  # Exibe as primeiras linhas para inspecionar os dados

# 3. Pré-processamento
# Converter o campo 'timestamp' para o tipo datetime (caso seja necessário)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Ignora erros de conversão

# Adicionando a coluna 'hora' a partir do 'timestamp'
df['hora'] = df['timestamp'].dt.hour

# Identificando se o status é erro (HTTP >= 400)
df['erro'] = df['status'].apply(lambda x: 1 if x >= 400 else 0)

# 4. Validação usando Regex
# Exemplo: Verificando o formato do 'ip' (IPv4)
ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"  # Padrão para IPs no formato x.x.x.x
df['ip_valido'] = df['ip'].apply(lambda x: bool(re.match(ip_pattern, str(x))))

# Exemplo: Verificando se o campo 'usuario' segue um padrão (por exemplo, sem caracteres especiais)
usuario_pattern = r"^[a-zA-Z0-9_]+$"  # Apenas letras, números e underlines
df['usuario_valido'] = df['usuario'].apply(lambda x: bool(re.match(usuario_pattern, str(x))))

# 5. Tratamento de valores nulos ou inconsistentes
if df[['timestamp', 'status', 'ip', 'usuario']].isnull().any().any():
    print("\nExistem valores nulos nas colunas críticas. Corrija ou remova esses dados.")
    df.dropna(subset=['timestamp', 'status', 'ip', 'usuario'], inplace=True)

# 6. Análise com Machine Learning (usando Isolation Forest)
# Selecionando as features para o modelo: hora e erro
X = df[['hora', 'erro']].dropna()  # Remove linhas com NaN
modelo = IsolationForest(contamination=0.05, random_state=42)
df['anomalia'] = modelo.fit_predict(X)

# Ajustando a classificação
df['classificacao'] = df['anomalia'].apply(lambda x: 'Normal' if x == 1 else 'Crítico')

# 7. Apresentação dos resultados

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

# 8. Visualização
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

# 9. Conclusão
print("\nAnálise concluída.")
if not acessos_criticos.empty:
    print("Acessos críticos foram detectados e apresentados acima.")
else:
    print("Não foram detectados acessos críticos.")
