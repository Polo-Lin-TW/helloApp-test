# Database Setup

This directory contains the MySQL database configuration for the HelloApp.

## Files

- `docker-compose.yml`: Docker Compose configuration for MySQL database
- `init.sql`: Database initialization script with schema and sample data

## Quick Start

1. Start the MySQL database:
```bash
cd db
docker-compose up -d
```

2. The database will be accessible at:
   - Host: localhost
   - Port: 3306
   - Database: helloapp
   - User: hellouser
   - Password: hellopassword

## Database Schema

### messages table
- `id`: Auto-increment primary key
- `name`: User name (VARCHAR 255)
- `message`: Message content (TEXT)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## API Endpoints

### POST /api/messages
Create a new message:
```json
{
  "name": "User Name",
  "message": "Hello World!"
}
```

### GET /api/messages
Get all messages (optional limit parameter)

### GET /api/messages/{id}
Get a specific message by ID