# Hello World Web App

A simple demonstration of a web application using:
- **Backend**: FastAPI (Python)
- **Frontend**: Vue 3.js

## Project Structure

```
├── backend/          # FastAPI backend
│   ├── main.py      # FastAPI application
│   └── requirements.txt
├── frontend/        # Vue 3.js frontend (SFC)
│   ├── index.html   # Main HTML file
│   ├── App.vue      # Main Vue component (SFC)
│   ├── main.js      # Vue 3 application entry
│   ├── package.json # Node.js dependencies
│   ├── vite.config.js # Vite configuration
│   ├── app.js.backup    # Original app.js (backup)
│   └── style.css.backup # Original styles (backup)
├── start_backend.sh  # Backend launcher script
├── start_frontend.sh # Frontend launcher script
├── ISSUE.md         # Issues and solutions
├── MIGRATION.md     # Vue SFC migration guide
├── PROJECT_SUMMARY.md # Project overview
└── README.md        # This file
```

## Setup Instructions

### Backend (FastAPI)

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend (Vue 3.js)

**Option 1: Using Vite (Recommended for development)**
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

**Option 2: Using Python HTTP Server (Simple)**
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the frontend:
   ```bash
   python3 -m http.server 3000
   ```

3. Open your browser and visit: `http://localhost:3000`

**Option 3: Using the helper script**
```bash
./start_frontend.sh
```

## API Endpoints

- `GET /`: Welcome message
- `GET /hello`: Hello world message
- `GET /hello/{name}`: Personalized greeting
- `GET /api/message`: JSON message for frontend

## Features

### Backend (FastAPI)
- CORS enabled for cross-origin requests
- RESTful API design
- Auto-generated API documentation
- Health check endpoints
- JSON responses with timestamps

### Frontend (Vue 3.js)
- **Single File Components (SFC)** with `<template>`, `<script>`, and `<style>` sections
- **Composition API** with `setup()` function
- **Reactive data** using `ref()` and `reactive()`
- **Lifecycle hooks** (`onMounted`, etc.)
- **Scoped styling** for component isolation
- **Vite** for fast development and hot module replacement
- Responsive design with CSS Grid and Flexbox
- Interactive components and API integration
- Error handling and loading states