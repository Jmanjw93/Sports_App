# How to Run the Application

## Prerequisites Check

✅ **Python 3.9+** - You have Python 3.12.0 installed!
❓ **Node.js 18+** - Need to check/install

## Step-by-Step Instructions

### Step 1: Install Python Dependencies

Open PowerShell in the `sports-analytics-app` folder and run:

```powershell
pip install -r requirements.txt
```

This will install all Python packages needed for the backend.

### Step 2: Install Node.js (if not installed)

If Node.js is not installed:

1. Download from: https://nodejs.org/
2. Install the LTS version
3. Restart your terminal/PowerShell
4. Verify: `node --version`

### Step 3: Install Frontend Dependencies

```powershell
cd frontend
npm install
cd ..
```

### Step 4: Create .env File (if not already created)

Create a `.env` file in the `sports-analytics-app` folder with:

```env
WEATHER_API_KEY=8277b9d832acb7bc96cabc045f69cac3
SPORTS_API_KEY=
DATABASE_URL=sqlite:///sports_analytics.db
```

### Step 5: Run the Application

You need **TWO terminal windows** open:

#### Terminal 1 - Backend Server

```powershell
cd backend
python -m uvicorn app.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

#### Terminal 2 - Frontend Server

```powershell
cd frontend
npm run dev
```

You should see:
```
- ready started server on 0.0.0.0:3000
- Local: http://localhost:3000
```

### Step 6: Open in Browser

Navigate to: **http://localhost:3000**

## Quick Method (Using Batch Scripts)

If you prefer, you can use the batch scripts:

**Terminal 1:**
```powershell
.\start_backend.bat
```

**Terminal 2:**
```powershell
.\start_frontend.bat
```

## Troubleshooting

### "pip is not recognized"
- Make sure Python is installed and added to PATH
- Try: `python -m pip install -r requirements.txt`

### "node is not recognized"
- Install Node.js from https://nodejs.org/
- Restart your terminal after installation

### "Module not found" errors
- Make sure you're in the correct directory
- Run: `pip install -r requirements.txt` again

### Backend won't start
- Check if port 8000 is already in use
- Make sure you're in the `backend` folder when running

### Frontend won't start
- Check if port 3000 is already in use
- Make sure you ran `npm install` in the frontend folder
- Check that Node.js is installed

### "Cannot connect to API"
- Make sure the backend is running on port 8000
- Check the frontend `.env.local` file has: `NEXT_PUBLIC_API_URL=http://localhost:8000`

## What You Should See

1. **Backend running**: Terminal shows API server on port 8000
2. **Frontend running**: Terminal shows Next.js dev server on port 3000
3. **Browser**: Opens to a modern sports analytics dashboard

## Testing the API

Once the backend is running, test it:

```powershell
# In a new terminal
curl http://localhost:8000/
```

Or open in browser: http://localhost:8000

You should see the API welcome message.

## Stopping the Application

- Press `Ctrl+C` in each terminal window to stop the servers




