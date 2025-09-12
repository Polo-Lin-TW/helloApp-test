# Use official MySQL 8.0 image
FROM mysql:8.0

# Set environment variables for MySQL - following Rainbond deployment pattern
# These can be overridden at runtime
ENV MYSQL_ROOT_PASSWORD=rootpassword
ENV MYSQL_DATABASE=helloapp
ENV MYSQL_USER=hellouser
ENV MYSQL_PASSWORD=hellopassword

# Copy initialization script
COPY init.sql /docker-entrypoint-initdb.d/

# Expose MySQL port
EXPOSE 3306

# Set container name through label (for reference)
LABEL container_name="helloapp_mysql"

# Configure restart policy through label
LABEL restart_policy="unless-stopped"

# The official MySQL image already handles the CMD and volume setup
# Data will be stored in /var/lib/mysql (default MySQL data directory)