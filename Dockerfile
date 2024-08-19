# Use uma imagem oficial do Python como base
FROM python:3.12-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie apenas os arquivos de dependências para melhor cacheamento no build
COPY pyproject.toml poetry.lock ./

# Instale o Poetry
RUN pip install poetry

# Instale as dependências no ambiente do Docker
RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

# Copie o restante do código da aplicação
COPY . .

# Exponha a porta que o FastAPI vai rodar
EXPOSE 8000

# Comando para rodar o servidor FastAPI
CMD ["uvicorn", "python_o_bom_candidato.app:app", "--host", "0.0.0.0", "--port", "8000"]
