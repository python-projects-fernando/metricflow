FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*

# Copia a pasta backend/ local para /app/backend/ dentro do contêiner
COPY backend/ /app/backend/

# ⭐ Instala o pacote backend como editável
RUN pip install -e /app/backend

# Instala dependências
RUN pip install -r /app/backend/requirements.txt

EXPOSE 8000

# ⭐ Agora o uvicorn pode usar o caminho absoluto 'backend.x.y'
CMD ["uvicorn", "backend.interfaces.main:app", "--host", "0.0.0.0", "--port", "8000"]