# How to Run the Application

## Current Status

✅ **Backend**: Ready to run (Python dependencies installed)
❌ **Frontend**: Needs Node.js installed first

## To Run the Backend (You can do this now!)

1. **Open PowerShell**
2. **Navigate to the backend folder**:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\backend
   ```

3. **Start the server**:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```

4. **You should see**:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete.
   ```

5. **Test it**: Open your browser and go to:
   - http://localhost:8000
   - http://localhost:8000/health
   - http://localhost:8000/api/games/

## To Run the Frontend (After installing Node.js)

1. **Install Node.js** (see WINDOWS_INSTALL.md)
2. **Open a NEW PowerShell window**
3. **Navigate to frontend**:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\frontend
   ```
4. **Install dependencies** (first time only):
   ```powershell
   npm install
   ```
5. **Start the frontend**:
   ```powershell
   npm run dev
   ```
6. **Open browser**: http://localhost:3000

## Running Both at Once

You need **TWO PowerShell windows**:

**Window 1 - Backend:**
```powershell
cd C:\Users\wyetw\sports-analytics-app\backend
python -m uvicorn app.main:app --reload
```

**Window 2 - Frontend:**
```powershell
cd C:\Users\wyetw\sports-analytics-app\frontend
npm run dev
```

## Quick Test

Once backend is running, test the API:
- http://localhost:8000/ - API info
- http://localhost:8000/health - Health check
- http://localhost:8000/api/games/?sport=nfl - Get games

## Troubleshooting

### "Module not found" error
- Make sure you're in the `backend` folder when running
- Try: `python -m uvicorn app.main:app --reload --host 127.0.0.1`

### Port already in use
- Another program is using port 8000
- Close other applications or change the port

### Can't find .env file
- Make sure `.env` is in `C:\Users\wyetw\sports-analytics-app\` (project root)
- Not in the backend folder!


