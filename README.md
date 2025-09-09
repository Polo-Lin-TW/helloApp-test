# Hello World Web App

A simple demonstration of a web application using:
- **Backend**: FastAPI (Python)
- **Frontend**: Vue 3.js

## Project Structure

```
├── backend/          # FastAPI backend
│   ├── main.py      # FastAPI application
│   └── requirements.txt
├── frontend/        # Vue 3.js frontend
│   ├── index.html   # Main HTML file
│   ├── app.js       # Vue 3 application
│   └── style.css    # Styling
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

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Serve the frontend (using Python's built-in server):
   ```bash
   python -m http.server 3000
   ```

3. Open your browser and visit: `http://localhost:3000`

## API Endpoints

- `GET /`: Welcome message
- `GET /hello`: Hello world message
- `GET /hello/{name}`: Personalized greeting
- `GET /api/message`: JSON message for frontend

## Features

- CORS enabled for cross-origin requests
- Responsive design
- Interactive Vue 3 components
- RESTful API design