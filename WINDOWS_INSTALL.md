# Windows Installation Guide

## Step 1: Install Node.js on Windows

### Download Node.js

1. **Open your web browser** (Chrome, Edge, Firefox, etc.)
2. Go to: **https://nodejs.org/**
3. You'll see two download buttons:
   - **LTS** (Recommended) - This is the stable version
   - **Current** - Latest features (may be less stable)
4. **Click the LTS button** (it's usually the left one, green)
5. This will download a file like: `node-v20.x.x-x64.msi`

### Install Node.js

1. **Find the downloaded file** (usually in your Downloads folder)
   - Look for: `node-v20.x.x-x64.msi`
2. **Double-click the .msi file** to start installation
3. **Windows may ask for permission** - Click "Yes" or "Run"
4. The Node.js Setup Wizard will open:
   - Click **"Next"**
   - Accept the license agreement, click **"Next"**
   - Choose installation location (default is fine), click **"Next"**
   - **IMPORTANT**: Make sure "Add to PATH" is checked ✅
   - Click **"Next"**
   - Click **"Install"**
   - You may need to enter your Windows password or click "Yes" for admin permission
5. Wait for installation (takes 1-2 minutes)
6. Click **"Finish"** when done

### Verify Installation

1. **Close ALL PowerShell/Command Prompt windows** (important!)
2. **Open a NEW PowerShell window**:
   - Press `Windows Key + X`
   - Click "Windows PowerShell" or "Terminal"
   - OR search for "PowerShell" in the Start menu
3. **Test Node.js**:
   ```powershell
   node --version
   ```
   Should show: `v20.x.x` or similar
4. **Test npm**:
   ```powershell
   npm --version
   ```
   Should show: `10.x.x` or similar

If you see version numbers, Node.js is installed correctly! ✅

## Step 2: Install Frontend Dependencies

1. **Navigate to your project**:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\frontend
   ```

2. **Install dependencies**:
   ```powershell
   npm install
   ```
   This will take 2-5 minutes. You'll see it downloading packages.

3. **Wait for it to finish** - You'll see:
   ```
   added 500+ packages
   ```

## Step 3: Run the Application

You need **TWO PowerShell windows** open:

### PowerShell Window 1 - Backend

1. Open PowerShell
2. Navigate to backend:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\backend
   ```
3. Start the backend:
   ```powershell
   python -m uvicorn app.main:app --reload
   ```
4. You should see:
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   ```
5. **Leave this window open** - don't close it!

### PowerShell Window 2 - Frontend

1. Open a **NEW** PowerShell window
2. Navigate to frontend:
   ```powershell
   cd C:\Users\wyetw\sports-analytics-app\frontend
   ```
3. Start the frontend:
   ```powershell
   npm run dev
   ```
4. You should see:
   ```
   - ready started server on 0.0.0.0:3000
   - Local: http://localhost:3000
   ```
5. **Leave this window open** too!

### Step 4: Open in Browser

1. Open your web browser (Chrome, Edge, Firefox)
2. Go to: **http://localhost:3000**
3. You should see the Sports Analytics application! 🎉

## Alternative: Using Batch Files (Easier!)

Instead of typing commands, you can use the batch files:

### PowerShell Window 1:
```powershell
cd C:\Users\wyetw\sports-analytics-app
.\start_backend.bat
```

### PowerShell Window 2:
```powershell
cd C:\Users\wyetw\sports-analytics-app
.\start_frontend.bat
```

## Windows-Specific Tips

### If Node.js installer won't run:
- Right-click the .msi file → "Run as administrator"
- Make sure Windows Defender isn't blocking it
- Check if you have enough disk space

### If PowerShell shows errors:
- Make sure you're using PowerShell (not Command Prompt)
- Try running PowerShell as Administrator
- Check that Python is installed: `python --version`

### If ports are already in use:
- Port 8000 (backend) or 3000 (frontend) might be in use
- Close other applications using those ports
- Or change the ports in the config files

### Finding your Downloads folder:
- Usually: `C:\Users\YourUsername\Downloads`
- Or press `Windows Key + R`, type `%USERPROFILE%\Downloads`

## Quick Checklist

- [ ] Downloaded Node.js from nodejs.org
- [ ] Installed Node.js (.msi file)
- [ ] Closed and reopened PowerShell
- [ ] Verified: `node --version` works
- [ ] Verified: `npm --version` works
- [ ] Ran `npm install` in frontend folder
- [ ] Started backend in one PowerShell window
- [ ] Started frontend in another PowerShell window
- [ ] Opened http://localhost:3000 in browser

## Need Help?

If you get stuck:
1. Check `TROUBLESHOOTING.md` for common issues
2. Make sure Node.js is installed: `node --version`
3. Make sure you're in the right folder
4. Check that both servers are running

Good luck! 🚀

