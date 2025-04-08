Título do Projeto: 
Análise de Logs de Acessos e Detecção de Anomalias


Descrição breve do projeto: 
Este projeto visa analisar arquivos de log de servidores web, identificando e classificando acessos críticos (baseados em erros HTTP 400 ou superiores) utilizando técnicas de Machine Learning para detectar anomalias no comportamento dos usuários. O foco é a detecção de padrões de comportamento anômalo, como acessos suspeitos ou erros em recursos específicos. A análise também realiza validações de formato de dados (como IP e usuário) e lida com valores ausentes ou inconsistentes, oferecendo uma visão clara sobre os eventos registrados no log.


Principais funcionalidades:  
1. Leitura e Análise de Logs: 
   O código lê arquivos de log no formato CSV, inspecionando suas colunas e exibindo informações relevantes.

2. Pré-processamento de Dados:  
   - Conversão de timestamps para o formato `datetime`.
   - Extração da hora do acesso.
   - Classificação de acessos com base no código de status HTTP (erro ou sucesso).

3. Validação de Dados:
   - Validação de IPs no formato IPv4 e de nomes de usuários utilizando expressões regulares.
   - Tratamento de dados nulos ou inconsistentes.

4. Detecção de Anomalias com Machine Learning:
   Utiliza o modelo Isolation Forest para identificar padrões atípicos nos acessos com base em variáveis como hora do acesso e status HTTP.

5. Classificação de Acessos:  
   - Classificação de acessos como "Normal" ou "Crítico", sendo que acessos críticos são aqueles que apresentam erros (status HTTP >= 400).

6. Visualização Gráfica:
   - Geração de um gráfico de dispersão para visualizar os eventos de acesso ao longo do tempo, destacando acessos normais e críticos com cores diferentes.

7. Relatório de Acessos Críticos:
   - Exibe um alerta caso acessos críticos sejam detectados e detalha esses eventos com informações como timestamp, IP, usuário, recurso e código de status.

Instruções de Instalação / Configuração:
1. Instalar Dependências:
   O projeto requer as seguintes bibliotecas:
   ```bash
   pip install pandas numpy scikit-learn matplotlib
   ```

2. Preparação do Arquivo de Log:
   O arquivo de log (`log_file.csv`) deve ser no formato CSV, contendo colunas como `timestamp`, `status`, `ip`, `usuario` e `recurso`. Certifique-se de que o arquivo esteja no mesmo diretório ou forneça o caminho correto para ele.

3. Execução do Script:  
   Após instalar as dependências e preparar o arquivo de log, basta executar o script Python para que a análise seja realizada:
   ```bash
   python nome_do_script.py
   ```

4. Personalizações Opcionais: 
   - Caso os dados possuam uma estrutura diferente, é necessário ajustar o código, especialmente nas seções de pré-processamento e validação.
   - Para visualizar o gráfico corretamente, verifique se o seu ambiente possui uma interface gráfica ou utilize o Jupyter Notebook.

5. Resultados: 
   O script exibirá uma tabela com a classificação dos acessos e alertará caso sejam detectados acessos críticos. Além disso, um gráfico de dispersão será gerado mostrando os eventos de acesso classificados.
Autores:
Nicolas Roberto Alves de Oliveira RGM:30059259
Gustavo Oliveira Bettoni RGM:31965636
Guilherme de Oliveira Silva RGM:31899871
