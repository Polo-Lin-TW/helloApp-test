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