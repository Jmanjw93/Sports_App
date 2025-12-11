# Project Structure

## Current Location

Your project is located at:
```
C:\Users\wyetw\sports-analytics-app
```

## Folder Structure

```
sports-analytics-app/              ← Project root (main folder)
│
├── backend/                       ← Backend folder (Python/FastAPI)
│   └── app/
│       ├── main.py               ← Backend entry point
│       ├── config.py
│       ├── data/                  ← Data collection modules
│       ├── models/                ← Prediction & betting models
│       └── routers/               ← API endpoints
│
├── frontend/                      ← Frontend folder (Next.js/React)
│   ├── app/                       ← Next.js app directory
│   ├── components/                ← React components
│   └── package.json               ← Frontend dependencies
│
├── .env                           ← Environment variables (your API keys)
├── requirements.txt               ← Python dependencies
├── README.md
└── ... (other config files)
```

## Important Paths

### Backend Path
```
C:\Users\wyetw\sports-analytics-app\backend
```

### Frontend Path
```
C:\Users\wyetw\sports-analytics-app\frontend
```

### Project Root
```
C:\Users\wyetw\sports-analytics-app
```

## Running Commands

### From Project Root
When you're in `C:\Users\wyetw\sports-analytics-app`, you run:

**Backend:**
```powershell
cd backend
python -m uvicorn app.main:app --reload
```

**Frontend:**
```powershell
cd frontend
npm run dev
```

### Using Batch Scripts (from project root)
```powershell
.\start_backend.bat
.\start_frontend.bat
```

## Key Points

1. ✅ **Both folders are INSIDE the project root** (`sports-analytics-app`)
2. ✅ **Backend** is at: `sports-analytics-app\backend`
3. ✅ **Frontend** is at: `sports-analytics-app\frontend`
4. ✅ **.env file** should be in the project root: `sports-analytics-app\.env`
5. ✅ **requirements.txt** is in the project root: `sports-analytics-app\requirements.txt`

## Current Status

✅ Your folders are in the correct location!
- Backend: `C:\Users\wyetw\sports-analytics-app\backend` ✓
- Frontend: `C:\Users\wyetw\sports-analytics-app\frontend` ✓
- .env file: `C:\Users\wyetw\sports-analytics-app\.env` ✓

Everything is set up correctly! You just need to:
1. Install Node.js
2. Run `npm install` in the frontend folder
3. Start both servers




