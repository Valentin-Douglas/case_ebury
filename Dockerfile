# Usa a imagem oficial e leve do Python
FROM python:3.12-slim

# Define a pasta /app como o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o projeto da sua máquina para dentro do contêiner
COPY . .

# Executa o seu script Python quando o contêiner iniciar
CMD ["python", "main.py"]