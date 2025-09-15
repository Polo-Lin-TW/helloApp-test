# Multi-stage Dockerfile for Vue 3 application

# Stage 1: Build stage
FROM node:18-alpine AS build-stage

# 設定工作目錄
WORKDIR /app

# 複製 package.json
COPY package.json ./

# 安裝依賴套件 (包含開發依賴，建構時需要)
RUN npm install

# 複製專案檔案
COPY . .

# 建構應用程式
RUN npm run build

# Stage 2: Production stage
FROM nginx:alpine AS production-stage

# 複製自定義的 nginx 配置
COPY nginx.conf /etc/nginx/nginx.conf

# 從建構階段複製編譯後的檔案到 Rainbond 預設靜態檔案目錄, 2025-01-15 起預設目錄改為 /app/www
COPY --from=build-stage /app/dist /app/www

# 暴露 8080 port
EXPOSE 5000

# 設定健康檢查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# 啟動 nginx
CMD ["nginx", "-g", "daemon off;"]