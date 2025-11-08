#!/bin/sh

# Define BACKEND_HOST como 'backend' se não estiver definido
BACKEND_HOST=${BACKEND_HOST:-backend}

# Substitui a variável no modelo nginx.conf e salva no destino final
sed "s|\${BACKEND_HOST:-backend}|$BACKEND_HOST|g" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

# Inicia o Nginx
exec nginx -g 'daemon off;'