# Issues and Solutions

This document records the issues encountered during the setup of the Hello World web application using FastAPI and Vue 3.js, along with their solutions.

## Issue #1: Virtual Environment pip Not Available

### Problem Description
When trying to run the startup script `./start_backend.sh`, the following errors occurred:

```bash
./start_backend.sh: line 29: pip: command not found
/home/ubuntu/helloApp-test/.venv/bin/python3: No module named uvicorn
```

### Root Cause Analysis
1. The virtual environment was created but `pip` was not installed in it
2. The virtual environment appeared to be managed by `uv` rather than standard Python venv
3. The startup script was looking for `pip` in the system PATH instead of the virtual environment

### Environment Details
- Operating System: Ubuntu Linux
- Python Version: 3.9.16
- Virtual Environment: Located at `.venv/` (uv-managed)
- Virtual Environment Status: Active (indicated by `(helloApp-test)` prompt)
- Package Manager: Homebrew Python installation

### Error Messages Encountered

#### 1. Missing pip Command
```bash
./start_backend.sh: line 29: pip: command not found
```

#### 2. Missing uvicorn Module
```bash
/home/ubuntu/helloApp-test/.venv/bin/python3: No module named uvicorn
```

#### 3. Externally Managed Environment Error
```bash
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try brew install
    xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a Python library that isn't in Homebrew,
    use a virtual environment:
    
    python3 -m venv path/to/venv
    source path/to/venv/bin/activate
    python3 -m pip install xyz
```

### Solution Steps

#### Step 1: Install pip in Virtual Environment
```bash
cd backend
../.venv/bin/python -m ensurepip --upgrade
```

**Result:**
```bash
Looking in links: /tmp/tmp34kis5bn
Processing /tmp/tmp34kis5bn/setuptools-58.1.0-py3-none-any.whl
Processing /tmp/tmp34kis5bn/pip-22.0.4-py3-none-any.whl
Installing collected packages: setuptools, pip
Successfully installed pip-22.0.4 setuptools-58.1.0
```

#### Step 2: Install Required Dependencies
```bash
cd backend
../.venv/bin/python -m pip install -r requirements.txt
```

**Result:**
```bash
Successfully installed annotated-types-0.7.0 anyio-3.7.1 click-8.1.8 
exceptiongroup-1.3.0 fastapi-0.104.1 h11-0.16.0 httptools-0.6.4 
idna-3.10 pydantic-2.11.7 pydantic-core-2.33.2 python-dotenv-1.1.1 
python-multipart-0.0.6 pyyaml-6.0.2 sniffio-1.3.1 starlette-0.27.0 
typing-extensions-4.15.0 typing-inspection-0.4.1 uvicorn-0.24.0 
uvloop-0.21.0 watchfiles-1.1.0 websockets-15.0.1
```

#### Step 3: Update Startup Script
Modified `start_backend.sh` to properly detect and use the virtual environment:

**Original problematic code:**
```bash
# Check if pip is installed
if ! command -v pip &> /dev/null && ! command -v pip3 &> /dev/null; then
    echo "Error: pip is not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start server
python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Fixed code:**
```bash
# Check if pip is installed (try pip3 first, then pip)
if command -v pip3 &> /dev/null; then
    PIP_CMD="pip3"
elif command -v pip &> /dev/null; then
    PIP_CMD="pip"
else
    echo "Error: pip is not installed."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Use the virtual environment's uvicorn
if [ -f "../.venv/bin/uvicorn" ]; then
    ../.venv/bin/uvicorn main:app --reload --host 0.0.0.0 --port 8000
elif [ -f "../.venv/bin/python" ]; then
    ../.venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
else
    python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
fi
```

### Verification
After implementing the solution, the backend was successfully tested:

```bash
cd backend
../.venv/bin/uvicorn main:app --host 127.0.0.1 --port 8000 &
curl -s http://127.0.0.1:8000/hello
```

**Response:**
```json
{
  "message": "Hello, World!",
  "timestamp": "2025-09-09T13:57:34.348667",
  "source": "FastAPI Backend"
}
```

## Key Learnings

### 1. Virtual Environment Detection
- Always check if the virtual environment has pip installed
- Use `python -m ensurepip` to install pip in environments that lack it
- Different virtual environment managers (venv, conda, uv) may have different setups

### 2. Path Resolution
- Virtual environment binaries are located in `.venv/bin/` directory
- Use relative paths when scripts need to access virtual environment tools
- Check for file existence before attempting to execute

### 3. Startup Script Best Practices
- Make scripts robust by checking for multiple scenarios
- Provide fallback options for different environment setups
- Use variables for commands to make scripts more maintainable

### 4. Debugging Virtual Environments
Useful commands for debugging virtual environment issues:
```bash
# Check virtual environment location
echo $VIRTUAL_ENV

# List virtual environment binaries
ls -la .venv/bin/

# Check Python path
which python3

# Verify pip installation
.venv/bin/python -m pip --version
```

## Prevention Strategies

1. **Environment Setup Validation**: Always verify that pip is available in the virtual environment before attempting package installation
2. **Robust Startup Scripts**: Write startup scripts that can handle different virtual environment configurations
3. **Documentation**: Clearly document the expected virtual environment setup and dependencies
4. **Testing**: Test startup scripts in clean environments to catch missing dependencies early

## Related Files Modified
- `start_backend.sh` - Updated to handle virtual environment properly
- `backend/requirements.txt` - Dependencies specification (unchanged)
- `backend/main.py` - FastAPI application (unchanged)

## Status
✅ **RESOLVED** - All issues have been successfully resolved and the application is now working correctly.

---

## Issue #2: Frontend-Backend Connection Issues in Docker Environment

### Problem Description
After containerizing the HelloApp project with Docker, the frontend (Vue.js) was unable to connect to the backend (FastAPI), resulting in network connection errors.

### Error Messages
```
index-Caiiv4iA.js:22 API Error: j {message: 'Network Error', name: 'AxiosError', code: 'ERR_NETWORK', ...}
GET http://localhost:8000/api/message?name=polo net::ERR_CONNECTION_REFUSED
```

### Root Causes

#### 1. Hardcoded API Base URL
**Problem**: Frontend Vue.js application had hardcoded API base URL pointing directly to backend container
```javascript
// frontend/App.vue:101
const apiBaseUrl = ref('http://localhost:8000')
```

**Impact**: Frontend was trying to connect directly to `localhost:8000` instead of using Nginx reverse proxy

#### 2. Docker Network Configuration Issues
**Problem**: Containers were not properly connected to the same Docker network
- Frontend container couldn't resolve `backend` hostname
- Network service discovery was failing

#### 3. Nginx Proxy Configuration Errors
**Problem**: Multiple configuration issues in `nginx.conf`:
- Wrong upstream server name (`backend` vs `helloapp-backend`)
- Incorrect proxy path configuration
- Missing proper path forwarding

### Solutions Applied

#### 1. Fix Frontend API Base URL
**Solution**: Changed hardcoded URL to use relative paths through Nginx proxy
```javascript
// Before
const apiBaseUrl = ref('http://localhost:8000')

// After  
const apiBaseUrl = ref('')
```

#### 2. Fix Docker Network Configuration
**Solution**: Ensured all containers are on the same network
```bash
# Create dedicated network
docker network create helloapp-network

# Start containers on same network
docker run -d --name helloapp-backend --network helloapp-network -p 8000:8000 helloapp-backend
docker run -d --name helloapp-frontend --network helloapp-network -p 80:80 helloapp-frontend
```

#### 3. Fix Nginx Proxy Configuration
**Solution**: Updated `frontend/nginx.conf` with correct upstream server names and paths

**Before (Incorrect):**
```nginx
location /api/ {
    proxy_pass http://backend:8000/;
}

location /docs {
    proxy_pass http://backend:8000/docs;
}

location /health {
    proxy_pass http://backend:8000/health;
}
```

**After (Correct):**
```nginx
location /api/ {
    proxy_pass http://helloapp-backend:8000/api/;
}

location /docs {
    proxy_pass http://helloapp-backend:8000/docs;
}

location /health {
    proxy_pass http://helloapp-backend:8000/health;
}
```

### Key Configuration Changes

#### Frontend Changes
1. **App.vue**: Updated API base URL to use relative paths
2. **nginx.conf**: Fixed upstream server names and proxy paths
3. **Docker network**: Connected to `helloapp-network`

#### Backend Changes
No changes required - backend was working correctly

#### Network Architecture
```
Browser Request → Nginx (Port 80) → FastAPI Backend (Port 8000)
     ↓                ↓                      ↓
localhost:80    helloapp-frontend    helloapp-backend
                (Docker Network)     (Docker Network)
```

### Verification Steps

After applying fixes, all endpoints work correctly:

1. **Frontend**: http://localhost/ ✅
2. **API Calls**: http://localhost/api/message ✅
3. **Health Check**: http://localhost/health ✅
4. **API Documentation**: http://localhost/docs ✅

### Final Container Status
```
NAMES               PORTS                                       STATUS
helloapp-frontend   0.0.0.0:80->80/tcp, :::80->80/tcp           Up (healthy)
helloapp-backend    0.0.0.0:8000->8000/tcp, :::8000->8000/tcp   Up (healthy)
```

### Lessons Learned

1. **Container Networking**: Always ensure containers that need to communicate are on the same Docker network
2. **Service Discovery**: Use container names (not localhost) for inter-container communication
3. **Proxy Configuration**: Verify upstream server names match actual container names
4. **Path Handling**: Ensure proxy paths preserve the correct API endpoint structure
5. **Relative URLs**: Use relative URLs in frontend to leverage reverse proxy instead of hardcoding backend URLs

### Prevention for Future Projects

1. Use environment variables for API base URLs
2. Set up Docker Compose for easier multi-container management
3. Test container networking early in development
4. Document container naming conventions
5. Validate proxy configurations before deployment

### Related Files Modified
- `frontend/App.vue` - Updated API base URL configuration
- `frontend/nginx.conf` - Fixed upstream server names and proxy paths
- `frontend/Dockerfile` - Multi-stage build configuration
- `backend/Dockerfile` - Backend containerization

### Status
✅ **RESOLVED** - Frontend and backend communication is now working correctly through Docker containers with Nginx reverse proxy.

---

## Issue #3: Frontend Static Assets 404 Errors

### Problem Description
When accessing the frontend at http://localhost:5000/, the main page loads but all static assets (CSS, JavaScript) fail to load with 404 errors, resulting in no UI being displayed.

### Error Messages
```
Console Errors:
index-Di6WNfaS.css:1  Failed to load resource: the server responded with a status of 404 (Not Found)
vue.esm-browser.js:12725 You are running a development build of Vue.
Make sure to use the production build (*.prod.js) when deploying for production.
index-BeibIizu.js:1  Failed to load resource: the server responded with a status of 404 (Not Found)
vendor-C2UFH459.js:1  Failed to load resource: the server responded with a status of 404 (Not Found)
index-Di6WNfaS.css:1  Failed to load resource: the server responded with a status of 404 (Not Found)
```

### Root Cause Analysis

#### Investigation Steps
1. **Container Status**: All containers were running and healthy
2. **File Existence**: Assets existed in the correct location `/app/www/assets/`
3. **Main Page**: Index.html was loading correctly (200 OK)
4. **Asset Requests**: All asset requests returned 404 errors

#### Root Cause
The nginx configuration had a static assets caching rule that was missing the `root` directive:

```nginx
# Problematic configuration
location ~* \.(css|js|ico|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
    # Missing: root /app/www;
}
```

**Issue**: When requests for static assets (like `/assets/index-BeibIizu.js`) matched this location block, nginx couldn't find the files because there was no `root` directive specifying where to look for them.

### Solution Applied

#### Fix: Add Missing Root Directive
**Location**: `frontend/nginx.conf:95`

**Before (Problematic):**
```nginx
# Static assets caching
location ~* \.(css|js|ico|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

**After (Fixed):**
```nginx
# Static assets caching
location ~* \.(css|js|ico|png|jpg|jpeg|gif|svg|woff|woff2|ttf|eot)$ {
    root /app/www;
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

#### Deployment Steps
1. Updated `frontend/nginx.conf` with the missing `root` directive
2. Rebuilt the frontend container:
   ```bash
   docker-compose build frontend && docker-compose up -d frontend
   ```
3. Verified asset loading:
   ```bash
   curl -I http://localhost:5000/assets/index-BeibIizu.js
   # Result: HTTP/1.1 200 OK
   ```

### Technical Details

#### File Structure
```
/app/www/
├── index.html
└── assets/
    ├── index-BeibIizu.js
    ├── index-Di6WNfaS.css
    └── vendor-C2UFH459.js
```

#### Nginx Location Matching
1. **Main page** (`/`): Matched the main location block with `root /app/www`
2. **Assets** (`/assets/*.js`, `/assets/*.css`): Matched the regex location block but had no `root` directive

#### Container Configuration
- **Port**: 5000 (updated from 8080)
- **Static files**: Served from `/app/www/`
- **Build process**: Multi-stage Docker build with nginx:alpine

### Verification
After applying the fix, all assets load correctly:

```bash
# Test results
curl -I http://localhost:5000/assets/index-BeibIizu.js
# HTTP/1.1 200 OK
# Content-Type: application/javascript
# Content-Length: 42134

curl -I http://localhost:5000/assets/index-Di6WNfaS.css
# HTTP/1.1 200 OK
# Content-Type: text/css

curl -I http://localhost:5000/
# HTTP/1.1 200 OK
# Content-Type: text/html
```

### Key Learnings

#### 1. Nginx Location Blocks
- Each `location` block needs its own `root` directive if it serves files
- Regex location blocks (`~*`) don't inherit `root` from other blocks
- Missing `root` directive causes 404 errors even when files exist

#### 2. Static Asset Serving
- Modern web applications require both HTML and asset files to be served correctly
- Asset requests follow different nginx location rules than main page requests
- Cache headers should be applied alongside proper file serving configuration

#### 3. Docker Multi-stage Builds
- Ensure static files are copied to the correct location in the final image
- Verify file permissions and directory structure in containers
- Test asset accessibility separately from main page functionality

### Prevention Strategies

1. **Configuration Testing**: Always test both main page and asset loading
2. **Nginx Validation**: Use `nginx -T` to verify complete configuration
3. **Development Workflow**: Test static asset serving early in containerization
4. **Documentation**: Document required nginx directives for each location block

### Related Files Modified
- `frontend/nginx.conf:95` - Added missing `root /app/www;` directive to static assets location block

### Status
✅ **RESOLVED** - Static assets now load correctly and the frontend UI displays properly at http://localhost:5000/.