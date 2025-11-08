# Build stage
FROM node:20-slim AS build

WORKDIR /app

# Install build dependencies (sometimes needed for native modules)
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    make \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy package files
COPY frontend/package*.json ./

# ⭐ Install patch-package globally first, then install dependencies
RUN npm install -g patch-package

# ⭐ FORCE CLEAN INSTALL to fix rollup platform issue AND patch-package issue
# This removes any cached modules that might be incompatible
RUN rm -rf node_modules package-lock.json && \
    npm install --force

# Copy source code
COPY frontend/ .

# ⭐ BUILD THE FRONTEND
# Use --force again if necessary, though usually not needed after install
RUN npm run build

# Production stage
FROM nginx:alpine

# ⭐ COPY CUSTOM NGINX CONFIG
COPY frontend/nginx.conf /etc/nginx/nginx.conf

# Copy the build output to replace the default nginx page
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]