# Multi-stage build for Vue.js frontend with Nginx
# Stage 1: Build the Vue.js application
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine

# Remove default nginx website
RUN rm -rf /usr/share/nginx/html/*

# Copy built application from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom nginx configuration template
COPY nginx.conf /etc/nginx/nginx.conf.template

# Set default environment variables
ENV BACKEND_HOST=helloapp-backend
ENV BACKEND_PORT=8000

# Expose port 8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Install gettext for envsubst command
RUN apk add --no-cache gettext

# Create startup script that processes environment variables
RUN echo '#!/bin/sh' > /usr/local/bin/start.sh && \
    echo 'envsubst "\$BACKEND_HOST \$BACKEND_PORT" < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf' >> /usr/local/bin/start.sh && \
    echo 'nginx -g "daemon off;"' >> /usr/local/bin/start.sh && \
    chmod +x /usr/local/bin/start.sh

# Start nginx with environment variable substitution
CMD ["/usr/local/bin/start.sh"]