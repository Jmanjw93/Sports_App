# Installation Troubleshooting Guide

## Common Issues with `pip install -r requirements.txt`

### Issue 1: NumPy Installation Fails (Python 3.12)

**Error**: `ModuleNotFoundError: No module named 'distutils'` or numpy build errors

**Solution**: 
- NumPy 1.24.x doesn't support Python 3.12
- Updated `requirements.txt` to use `numpy>=1.26.0` which supports Python 3.12
- If you're using Python 3.12, make sure you have numpy 1.26.0 or higher

**Fix Applied**:
```txt
numpy>=1.26.0  # Changed from numpy==1.24.3
```

---

### Issue 2: Version Conflicts

**Error**: Package version conflicts or incompatible versions

**Solution**: 
- Updated all packages to use `>=` instead of `==` for more flexibility
- This allows pip to install compatible versions automatically

**Current requirements.txt**:
```txt
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-multipart>=0.0.6
requests>=2.31.0
python-dateutil>=2.8.2
numpy>=1.26.0
```

---

### Issue 3: pip is Outdated

**Error**: Old pip version causing installation issues

**Solution**: Upgrade pip first
```bash
python -m pip install --upgrade pip
```

Then install requirements:
```bash
pip install -r requirements.txt
```

---

### Issue 4: Python Version Compatibility

**Recommended Python Versions**:
- Python 3.10+
- Python 3.11 (recommended)
- Python 3.12 (works with updated requirements.txt)

**Check your Python version**:
```bash
python --version
```

---

### Issue 5: Virtual Environment Issues

**Best Practice**: Use a virtual environment

**Create virtual environment**:
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

**Then install requirements**:
```bash
pip install -r requirements.txt
```

---

### Issue 6: Missing System Dependencies (Linux)

**Error**: Build errors for numpy or other packages

**Solution**: Install build tools
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel gcc
```

---

### Issue 7: Network/Proxy Issues

**Error**: Connection timeout or SSL errors

**Solution**: 
- Check your internet connection
- If behind a proxy, configure pip:
```bash
pip install --proxy http://proxy.example.com:8080 -r requirements.txt
```

---

## Verification

After installation, verify everything works:

```bash
# Test imports
python -c "import fastapi; import uvicorn; import numpy; print('All packages installed successfully!')"

# Or start the server
cd backend
uvicorn app.main:app --reload
```

---

## For Render Deployment

Render will automatically:
1. Install Python 3.11 (as specified in `runtime.txt`)
2. Run `pip install -r requirements.txt`
3. Start the server with the command in `Procfile`

If deployment fails on Render:
1. Check the build logs in Render dashboard
2. Verify `requirements.txt` is in the `backend/` directory
3. Ensure `runtime.txt` specifies a supported Python version (3.11 recommended)

---

## Quick Fix Commands

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# If specific package fails, install individually
pip install numpy>=1.26.0
pip install fastapi>=0.104.1
# etc.
```

---

## Still Having Issues?

1. Check Python version: `python --version`
2. Check pip version: `pip --version`
3. Try installing packages one by one to identify the problematic package
4. Check error messages carefully - they often indicate the specific issue
5. For Render deployment, check the build logs in the Render dashboard

