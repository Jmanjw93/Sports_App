# How to Start the Application

## Backend (Port 8001)

**Option 1: Using Batch File**
```powershell
.\start_backend.bat
```

**Option 2: Manual Command**
```powershell
cd backend
python -m uvicorn app.main:app --reload --port 8001
```

The backend will be available at: **http://localhost:8001**

Test it: http://localhost:8001/health

## Frontend (Port 3000)

**After installing Node.js:**

```powershell
cd frontend
npm install
npm run dev
```

The frontend will be available at: **http://localhost:3000**

## Quick Start

1. **Terminal 1 - Backend:**
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\backend
   python -m uvicorn app.main:app --reload --port 8001
   ```

2. **Terminal 2 - Frontend (after Node.js installed):**
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\frontend
   npm run dev
   ```

3. **Open Browser:** http://localhost:3000

