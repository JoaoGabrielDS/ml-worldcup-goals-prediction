# Python 3.11.3 — ambiente limpo e reproduzível
FROM python:3.11.3-slim

# Metadados
LABEL description="Previsão de Média de Gols — FIFA World Cup 2026"
LABEL course="Machine Learning AV2 — 2026"

# Diretório de trabalho
WORKDIR /app

# Copiar dependências primeiro (cache do Docker)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar projeto completo
COPY . .

# Expor porta do Jupyter
EXPOSE 8888

# Comando padrão: Jupyter sem senha, acessível externamente
CMD ["jupyter", "notebook", \
     "--ip=0.0.0.0", \
     "--port=8888", \
     "--no-browser", \
     "--allow-root", \
     "--NotebookApp.token=''", \
     "--NotebookApp.password=''"]
