# frontend/Dockerfile

# === STAGE 1: Build do frontend ===
FROM node:20-slim AS build

WORKDIR /app

# Instalar dependências de build (às vezes necessárias para módulos nativos)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências primeiro para aproveitar cache do Docker
COPY frontend/package*.json ./

# Instalar patch-package globalmente primeiro, depois instalar dependências
RUN npm install -g patch-package

# FORCE CLEAN INSTALL to fix rollup platform issue
RUN rm -rf node_modules package-lock.json && \
    npm install --force

# Copiar o restante do código fonte
COPY frontend/ .

# Construir o frontend (gera a pasta /app/dist)
RUN npm run build

# === STAGE 2: Servidor Nginx ===
FROM nginx:alpine

# Instalar sed (necessário para substituir a variável no script de inicialização)
RUN apk add --no-cache sed

# Copiar o arquivo de configuração modelo para o contêiner
COPY frontend/nginx.conf /etc/nginx/nginx.conf.template

# Copiar o script de inicialização para o contêiner
COPY frontend/start.sh /start.sh

# Tornar o script de inicialização executável dentro do contêiner
RUN chmod +x /start.sh

# Copiar os arquivos gerados pelo build (pasta /app/dist do stage 1) PARA O NGINX
COPY --from=build /app/dist /usr/share/nginx/html

# Expor porta 80
EXPOSE 80

# Comando para iniciar o contêiner: executa o script de inicialização
CMD ["/start.sh"]